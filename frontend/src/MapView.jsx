// // src/MapView.js
// import React, { useEffect, useState } from "react";
// import {
//   MapContainer,
//   TileLayer,
//   GeoJSON,
//   Polyline,
//   Polygon,
// } from "react-leaflet";
// import { generateGridLines, generateGridCells } from "./utils";

// const rajasthanCenter = [27.0238, 74.2179]; // Center of Rajasthan

// // Color blending for heatmap (yellow -> green)
// function getDistrictColor(districtName, carbonStock, districts) {
//   const value = carbonStock[districtName] || 0;
//   const values = Object.values(carbonStock).filter((v) => v > 0);
//   if (values.length === 0) return "#eee";
//   const min = Math.min(...values);
//   const max = Math.max(...values);
//   const norm = (value - min) / (max - min + 1e-6);

//   function lerp(a, b, t) {
//     return Math.round(a + (b - a) * t);
//   }
//   function hex2rgb(hex) {
//     hex = hex.replace("#", "");
//     if (hex.length === 3) hex = hex.split("").map((c) => c + c).join("");
//     const int = parseInt(hex, 16);
//     return [(int >> 16) & 255, (int >> 8) & 255, int & 255];
//   }
//   function blend(hex1, hex2, t) {
//     const rgb1 = hex2rgb(hex1);
//     const rgb2 = hex2rgb(hex2);
//     const rgb = rgb1.map((c, i) => lerp(c, rgb2[i], t));
//     return `rgb(${rgb.join(",")})`;
//   }
//   return blend("#fffbe6", "#47bb55", norm);
// }


// export default function MapView() {
//   const [districts, setDistricts] = useState(null); // State to hold district GeoJSON data
//   const [selectedDistrict, setSelectedDistrict] = useState(null); // State to hold the selected district
//   const [gridLines, setGridLines] = useState(null); // State to hold grid lines
//   const [gridCells, setGridCells] = useState(null); // State to hold grid cells
//   const [soilData, setSoilData] = useState(null); // State to hold soil data
//   const [cultivableMap, setCultivableMap] = useState({}); // State to hold cultivable map data
//   const [carbonStock, setCarbonStock] = useState({}); 


//   useEffect(() => {
//     // Fetch district GeoJSON data
//     fetch(process.env.PUBLIC_URL + "/districts.geojson")
//       .then((res) => res.json())
//       .then(setDistricts);
//   }, []);
//   useEffect(() => {
//     // Log when districts are loaded
//     fetch("http://127.0.0.1:8000/api/cultivable_grids/")
//       .then((res) => res.json())
//       .then(setCultivableMap);
//   }, []);
//   useEffect(() => {
//     // Log when cultivableMap is loaded
//     console.log("cultivableMap loaded:", cultivableMap);
//   }, [cultivableMap]);

//   useEffect(() => {
//     fetch("http://127.0.0.1:8000/api/district_carbon_heatmap/")
//       .then((res) => res.json())
//       .then(setCarbonStock);
//   }, []);

//   const onDistrictClick = (e) => {
//     // Handle district click event
//     const feature = e.target.feature;
//     setSelectedDistrict(feature); // Set the selected district
//     setGridLines(generateGridLines(feature.geometry, 0.05)); // Generate grid lines for the selected district
//     setGridCells(generateGridCells(feature.geometry, 0.05)); // Generate grid cells for the selected district
//   };

//   const backToAll = () => {
//     // Handle back button click to reset state
//     setSelectedDistrict(null);
//     setGridLines(null);
//     setSoilData(null);
//   };

//   const onCellClick = async (cell) => {
//     // Handle cell click event to fetch soil data
//     const centerLat = (cell[0][0] + cell[2][0]) / 2; // Calculate center latitude of the cell
//     const centerLng = (cell[0][1] + cell[2][1]) / 2; // Calculate center longitude of the cell
//     const city = // Get the city name from the selected district
//       selectedDistrict?.properties?.NAME_2 || // Fallback to district name
//       selectedDistrict?.properties?.district || // Fallback to district property
//       selectedDistrict?.properties?.name || // Fallback to name property
//       "";

//     try {
//       const response = await fetch(
//         // Fetch soil data from the API
//         "http://127.0.0.1:8000/api/soil_properties/",
//         {
//           method: "POST",
//           headers: {
//             "Content-Type": "application/json",
//           },
//           body: JSON.stringify({ lat: centerLat, lng: centerLng, city }), // Send latitude, longitude, and city in the request body
//         }
//       );

//       if (!response.ok) {
//         throw new Error("Failed to fetch soil data");
//       }

//       const data = await response.json(); // Parse the JSON response

//       // uncomment below and comment above to fetch data from csv instead of databases 
//       // setSoilData({ // Set the soil data state with the fetched data
//       //   soil: data.soil_data,
//       //   climate: data.climate_data,
//       //   forest: data.forest_population_data,
//       //   river: data.river_data,
//       //   estimatedArea: data.estimated_area_data,
//       //   rainfall: data.rainfall_data,
//       //   wellDepth: data.well_depth_data,
//       //   waterUsage: data.water_usage_data,
//       //   soilAnalysis: data.soil_analysis_data,
//       //   cropProduction: data.crop_production_data,
//       //   cropPrice: data.crop_price_data, // <--- NEW!
//       // });
//       setSoilData(data);
//     } catch (error) {
//       alert("Error fetching soil data: " + error.message); // Show error message if fetch fails
//     }
//   };

//   useEffect(() => {
//     // Log the cultivableMap keys when it changes
//     console.log(
//       "First 10 cultivableMap keys:",
//       Object.keys(cultivableMap).slice(0, 10)
//     );
//   }, [cultivableMap]);

//   function findClosestCultivable(centerLat, centerLng, cultivableMap) {
//     const EPSILON = 0.00012; // slightly more than 0.0001 for 5 decimal places
//     let foundKey = null;
//     for (const k of Object.keys(cultivableMap)) {
//       const [lat, lng] = k.split(",").map(Number);
//       if (
//         Math.abs(lat - centerLat) < EPSILON &&
//         Math.abs(lng - centerLng) < EPSILON
//       ) {
//         foundKey = k;
//         break;
//       }
//     }
//     return foundKey ? cultivableMap[foundKey] : undefined;
//   }

//   if (!districts) return <div>Loading Map...</div>;

//   return (
//     <div style={{ height: "100vh", width: "100vw" }}>
//       <MapContainer // Main map container
//         center={rajasthanCenter}
//         zoom={6.5}
//         style={{ height: "100vh", width: "100vw" }}
//       >
//         {/* <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" /> */}
//         <TileLayer // Tile layer for the map background
//           url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
//           attribution="Tiles © Esri"
//         />

//         {selectedDistrict === null ? ( // If no district is selected, show all districts
//           // <GeoJSON
//           //   data={districts}
//           //   style={{
//           //     fillColor: "#1976d2",
//           //     color: "white",
//           //     weight: 1,
//           //     fillOpacity: 0.5,
//           //     cursor: "pointer",
//           //   }}
//           //   onEachFeature={(feature, layer) => {
//           //     layer.on({
//           //       click: onDistrictClick,
//           //     });
//           //   }}
//           // />
//           <GeoJSON // Main GeoJSON layer for districts
//             data={districts} // Use the districts GeoJSON data
//             style={() => ({
//               // Style for each district
//               fillColor: "#88c0f7",
//               color: "white",
//               weight: 1,
//               fillOpacity: 0.6,
//               cursor: "pointer",
//             })}
//             onEachFeature={(feature, layer) => {
//               layer.bindTooltip(
//                 feature.properties.NAME_2 ||
//                   feature.properties.district ||
//                   feature.properties.name,
//                 {
//                   permanent: true,
//                   direction: "center",
//                   className: "district-label",
//                 }
//               );

//               layer.on({
//                 mouseover: (e) => {
//                   e.target.setStyle({
//                     fillOpacity: 0.9,
//                     weight: 2,
//                   });
//                 },
//                 mouseout: (e) => {
//                   e.target.setStyle({
//                     fillOpacity: 0.6,
//                     weight: 1,
//                   });
//                 },
//                 click: onDistrictClick,
//               });
//             }}
//           />
//         ) : (
//           <>
//             {/* <GeoJSON
//               data={selectedDistrict}
//               style={{
//                 fillColor: "#43a047",
//                 color: "#1b5e20",
//                 weight: 2,
//                 fillOpacity: 0.7,
//               }}
//             /> */}
//             <GeoJSON
//               data={selectedDistrict}
//               style={{
//                 fillColor: "#6dd47e", // More vivid green
//                 color: "#2f855a", // Dark green boundary
//                 weight: 3,
//                 fillOpacity: 0.8,
//               }}
//             />

//             {gridLines && (
//               <>
//                 {gridLines.hLines.map((line, i) => (
//                   <Polyline
//                     key={"h" + i}
//                     positions={line.map(([lat, lng]) => [lat, lng])}
//                     pathOptions={{ color: "red", weight: 1, opacity: 0.5 }}
//                   />
//                 ))}
//                 {gridLines.vLines.map((line, i) => (
//                   <Polyline
//                     key={"v" + i}
//                     positions={line.map(([lat, lng]) => [lat, lng])}
//                     pathOptions={{ color: "red", weight: 1, opacity: 0.5 }}
//                   />
//                 ))}
//               </>
//             )}

//             {gridCells &&
//               gridCells.map(({ cell, index }) => {
//                 const cultivable = cultivableMap[index] !== 0; // index-based lookup
//                 return (
//                   <Polygon
//                     key={index}
//                     positions={cell}
//                     pathOptions={{
//                       color: cultivable ? "orange" : "#222",
//                       weight: 1,
//                       fillOpacity: cultivable ? 0.08 : 0.7,
//                       fillColor: cultivable ? "#fffbe6" : "#222",
//                       dashArray: cultivable ? null : "4 4",
//                       opacity: 1,
//                     }}
//                     eventHandlers={
//                       cultivable ? { click: () => onCellClick(cell) } : {}
//                     }
//                   />
//                 );
//               })}

//             <div
//               style={{
//                 position: "absolute",
//                 top: 10,
//                 left: 10,
//                 zIndex: 1000,
//               }}
//             >
//               <button
//                 onClick={backToAll}
//                 style={{
//                   padding: "8px 18px",
//                   fontWeight: "bold",
//                   background: "#fff",
//                   borderRadius: "6px",
//                   border: "1px solid #888",
//                 }}
//               >
//                 ⬅ Back to All Districts
//               </button>
//             </div>
//           </>
//         )}

//         {/* Floating Sidebar for Data */}
//         {/* unomment below to fetch data from csv  */}
//         {/* {soilData && (
//           <div
//             style={{
//               position: "absolute",
//               top: 60,
//               right: 25,
//               zIndex: 2000,
//               background: "#fff",
//               padding: 22,
//               borderRadius: 14,
//               minWidth: 350,
//               maxWidth: 400,
//               boxShadow: "0 2px 10px #0002",
//               maxHeight: "80vh",
//               overflowY: "auto",
//             }}
//           >
//             <h3 style={{ margin: "0 0 12px 0", color: "#1976d2" }}>
//               Location Data
//             </h3>
//             <h4 style={{ marginBottom: 5 }}>Soil Data</h4>
//             <ul style={{ marginBottom: 16 }}>
//               {Object.entries(soilData.soil).map(([k, v]) => (
//                 <li key={k}>
//                   <b>{k}</b>: {v}
//                 </li>
//               ))}
//             </ul>
//             <h4 style={{ marginBottom: 5 }}>Climate Data</h4>
//             <ul style={{ marginBottom: 16 }}>
//               {Object.entries(soilData.climate).map(([k, v]) => (
//                 <li key={k}>
//                   <b>{k}</b>: {v}
//                 </li>
//               ))}
//             </ul>
//             <h4 style={{ marginBottom: 5 }}>Forest & Population Data</h4>
//             <ul style={{ marginBottom: 8 }}>
//               {Object.entries(soilData.forest).map(([k, v]) => (
//                 <li key={k}>
//                   <b>{k}</b>: {v}
//                 </li>
//               ))}
//             </ul>
//             <h4 style={{ marginBottom: 5 }}>Rivers in District</h4>
//             <ul style={{ marginBottom: 8 }}>
//               {soilData.river && soilData.river.length > 0 ? (
//                 soilData.river.map((r, i) => (
//                   <li key={i}>
//                     <b>{r["Name of River"]}</b> (Area: {r["Area in Ha."]} Ha)
//                   </li>
//                 ))
//               ) : (
//                 <li>No rivers found in this district.</li>
//               )}
//             </ul>
//             <h4 style={{ marginBottom: 5 }}>Estimated Area (Ha)</h4>
//             <div style={{ marginBottom: 12, fontWeight: 500 }}>
//               {soilData.estimatedArea
//                 ? soilData.estimatedArea
//                 : "Not available"}
//             </div>
//             <h4 style={{ marginBottom: 5 }}>Rainfall Data</h4>
//             {soilData.rainfall && Object.keys(soilData.rainfall).length > 0 ? (
//               <ul style={{ marginBottom: 12 }}>
//                 {Object.entries(soilData.rainfall).map(([k, v]) =>
//                   k !== "District" ? (
//                     <li key={k}>
//                       <b>{k}</b>: {v}
//                     </li>
//                   ) : null
//                 )}
//               </ul>
//             ) : (
//               <div style={{ marginBottom: 12 }}>
//                 No rainfall data available.
//               </div>
//             )}
//             <h4 style={{ marginBottom: 5 }}>Well Water Depth Analysis</h4>
//             {soilData.wellDepth &&
//             Object.keys(soilData.wellDepth).length > 0 ? (
//               <ul style={{ marginBottom: 12 }}>
//                 {Object.entries(soilData.wellDepth).map(([k, v]) =>
//                   k !== "District Name" && k !== "Sr. No." ? (
//                     <li key={k}>
//                       <b>{k}</b>: {v}
//                     </li>
//                   ) : null
//                 )}
//               </ul>
//             ) : (
//               <div style={{ marginBottom: 12 }}>
//                 No well depth data available.
//               </div>
//             )}
//             <h4 style={{ marginBottom: 5 }}>Water Usage Data</h4>
//             {soilData.waterUsage &&
//             Object.keys(soilData.waterUsage).length > 0 ? (
//               <ul style={{ marginBottom: 12 }}>
//                 {Object.entries(soilData.waterUsage).map(([k, v]) =>
//                   k !== "District" ? (
//                     <li key={k}>
//                       <b>{k}</b>: {v}
//                     </li>
//                   ) : null
//                 )}
//               </ul>
//             ) : (
//               <div style={{ marginBottom: 12 }}>
//                 No water usage data available.
//               </div>
//             )}

//             <h4 style={{ marginBottom: 5 }}>Soil Analysis Data</h4>
//             {Array.isArray(soilData.soilAnalysis) &&
//             soilData.soilAnalysis.length > 0 ? (
//               <ul
//                 style={{ marginBottom: 12, maxHeight: 200, overflowY: "auto" }}
//               >
//                 {soilData.soilAnalysis.map((row, idx) => (
//                   <li
//                     key={idx}
//                     style={{ marginBottom: 8, borderBottom: "1px solid #eee" }}
//                   >
//                     {Object.entries(row).map(([k, v]) =>
//                       k !== "District" ? (
//                         <div key={k}>
//                           <b>{k}</b>: {v}
//                         </div>
//                       ) : null
//                     )}
//                   </li>
//                 ))}
//               </ul>
//             ) : (
//               <div style={{ marginBottom: 12 }}>
//                 No soil analysis data available.
//               </div>
//             )}

//             <h4 style={{ marginBottom: 5 }}>Crop Production Data</h4>
//             {Array.isArray(soilData.cropProduction) &&
//             soilData.cropProduction.length > 0 ? (
//               <ul
//                 style={{ marginBottom: 12, maxHeight: 200, overflowY: "auto" }}
//               >
//                 {soilData.cropProduction.map((row, idx) => (
//                   <li
//                     key={idx}
//                     style={{ marginBottom: 8, borderBottom: "1px solid #eee" }}
//                   >
//                     {Object.entries(row).map(([k, v]) =>
//                       k !== "District" ? (
//                         <div key={k}>
//                           <b>{k}</b>: {v}
//                         </div>
//                       ) : null
//                     )}
//                   </li>
//                 ))}
//               </ul>
//             ) : (
//               <div style={{ marginBottom: 12 }}>
//                 No crop production data available.
//               </div>
//             )}

//             <h4 style={{ marginBottom: 5 }}>Crop Price Data</h4>
//             {Array.isArray(soilData.cropPrice) &&
//             soilData.cropPrice.length > 0 ? (
//               <ul
//                 style={{ marginBottom: 12, maxHeight: 200, overflowY: "auto" }}
//               >
//                 {soilData.cropPrice.map((row, idx) => (
//                   <li
//                     key={idx}
//                     style={{ marginBottom: 8, borderBottom: "1px solid #eee" }}
//                   >
//                     {Object.entries(row).map(([k, v]) =>
//                       k !== "District" ? (
//                         <div key={k}>
//                           <b>{k}</b>: {v}
//                         </div>
//                       ) : null
//                     )}
//                   </li>
//                 ))}
//               </ul>
//             ) : (
//               <div style={{ marginBottom: 12 }}>
//                 No crop price data available.
//               </div>
//             )}

//             <button
//               style={{
//                 marginTop: 12,
//                 padding: "7px 18px",
//                 borderRadius: 7,
//                 background: "#eee",
//                 border: "1px solid #888",
//                 cursor: "pointer",
//                 fontWeight: "bold",
//                 float: "right",
//               }}
//               onClick={() => setSoilData(null)}
//             >
//               Close
//             </button>
//           </div>
//         )} */}
//         {/* Floating Sidebar for Data */}
//         {/* this below code of soildata is used to fetch data from databases instead of csv  */}
//         {soilData && (
//           <div
//             style={{
//               position: "absolute",
//               top: 60,
//               right: 25,
//               zIndex: 2000,
//               background: "#fff",
//               padding: 22,
//               borderRadius: 14,
//               minWidth: 350,
//               maxWidth: 400,
//               boxShadow: "0 2px 10px #0002",
//               maxHeight: "80vh",
//               overflowY: "auto",
//             }}
//           >
//             <h3 style={{ margin: "0 0 12px 0", color: "#1976d2" }}>
//               Location Data
//             </h3>

//             {/* Top important sections */}
//             {soilData.soil_data && (
//               <>
//                 <h4>Soil Data</h4>
//                 <ul>
//                   {Object.entries(soilData.soil_data).map(([k, v]) => (
//                     <li key={k}>
//                       <b>{k}</b>: {v}
//                     </li>
//                   ))}
//                 </ul>
//               </>
//             )}

//             {soilData.climate_data && (
//               <>
//                 <h4>Climate Data</h4>
//                 <ul>
//                   {Object.entries(soilData.climate_data).map(([k, v]) => (
//                     <li key={k}>
//                       <b>{k}</b>: {v}
//                     </li>
//                   ))}
//                 </ul>
//               </>
//             )}

//             {/* ...do this for any other always-important fields you want... */}

//             {/* Render any OTHER fields that are present (dynamic): */}
//             {Object.entries(soilData)
//               .filter(([key]) => !["soil_data", "climate_data"].includes(key))
//               .map(([key, value]) => (
//                 <div key={key} style={{ marginBottom: 16 }}>
//                   <h4 style={{ marginBottom: 5 }}>
//                     {key
//                       .replace(/_/g, " ")
//                       .replace(/\b\w/g, (c) => c.toUpperCase())}
//                   </h4>
//                   {/* Array of objects */}
//                   {Array.isArray(value) ? (
//                     value.length > 0 ? (
//                       <ul style={{ maxHeight: 120, overflowY: "auto" }}>
//                         {value.map((item, i) =>
//                           typeof item === "object" ? (
//                             <li
//                               key={i}
//                               style={{
//                                 borderBottom: "1px solid #eee",
//                                 marginBottom: 6,
//                               }}
//                             >
//                               {Object.entries(item).map(([k, v]) => (
//                                 <div key={k}>
//                                   <b>{k}</b>: {String(v)}
//                                 </div>
//                               ))}
//                             </li>
//                           ) : (
//                             <li key={i}>{String(item)}</li>
//                           )
//                         )}
//                       </ul>
//                     ) : (
//                       <div>No data available.</div>
//                     )
//                   ) : typeof value === "object" && value !== null ? (
//                     <ul>
//                       {Object.entries(value).map(([k, v]) => (
//                         <li key={k}>
//                           <b>{k}</b>: {String(v)}
//                         </li>
//                       ))}
//                     </ul>
//                   ) : (
//                     <div>{String(value)}</div>
//                   )}
//                 </div>
//               ))}

//             <button
//               style={{
//                 marginTop: 12,
//                 padding: "7px 18px",
//                 borderRadius: 7,
//                 background: "#eee",
//                 border: "1px solid #888",
//                 cursor: "pointer",
//                 fontWeight: "bold",
//                 float: "right",
//               }}
//               onClick={() => setSoilData(null)}
//             >
//               Close
//             </button>
//           </div>
//         )}
//       </MapContainer>
//     </div>
//   );
// }



// src/MapView.js
import React, { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  GeoJSON,
  Polyline,
  Polygon,
} from "react-leaflet";
import { generateGridLines, generateGridCells } from "./utils";

const rajasthanCenter = [27.0238, 74.2179]; // Center of Rajasthan

// Color blending for heatmap (yellow -> green)
function getDistrictColor(districtName, carbonStock, districts) {
  const value = carbonStock[districtName] || 0;
  const values = Object.values(carbonStock).filter((v) => v > 0);
  if (values.length === 0) return "#eee";
  const min = Math.min(...values);
  const max = Math.max(...values);
  const norm = (value - min) / (max - min + 1e-6);

  function lerp(a, b, t) {
    return Math.round(a + (b - a) * t);
  }
  function hex2rgb(hex) {
    hex = hex.replace("#", "");
    if (hex.length === 3) hex = hex.split("").map((c) => c + c).join("");
    const int = parseInt(hex, 16);
    return [(int >> 16) & 255, (int >> 8) & 255, int & 255];
  }
  function blend(hex1, hex2, t) {
    const rgb1 = hex2rgb(hex1);
    const rgb2 = hex2rgb(hex2);
    const rgb = rgb1.map((c, i) => lerp(c, rgb2[i], t));
    return `rgb(${rgb.join(",")})`;
  }
  return blend("#fffbe6", "#47bb55", norm);
}

export default function MapView() {
  const [districts, setDistricts] = useState(null);
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [gridLines, setGridLines] = useState(null);
  const [gridCells, setGridCells] = useState(null);
  const [soilData, setSoilData] = useState(null);
  const [cultivableMap, setCultivableMap] = useState({});
  const [carbonStock, setCarbonStock] = useState({});

  useEffect(() => {
    fetch(process.env.PUBLIC_URL + "/districts.geojson")
      .then((res) => res.json())
      .then(setDistricts);
  }, []);
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/cultivable_grids/")
      .then((res) => res.json())
      .then(setCultivableMap);
  }, []);
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/district_carbon_heatmap/")
      .then((res) => res.json())
      .then(setCarbonStock);
  }, []);

  const onDistrictClick = (e) => {
    const feature = e.target.feature;
    setSelectedDistrict(feature);
    setGridLines(generateGridLines(feature.geometry, 0.05));
    setGridCells(generateGridCells(feature.geometry, 0.05));
  };

  const backToAll = () => {
    setSelectedDistrict(null);
    setGridLines(null);
    setSoilData(null);
  };

  const onCellClick = async (cell) => {
    const centerLat = (cell[0][0] + cell[2][0]) / 2;
    const centerLng = (cell[0][1] + cell[2][1]) / 2;
    const city =
      selectedDistrict?.properties?.NAME_2 ||
      selectedDistrict?.properties?.district ||
      selectedDistrict?.properties?.name ||
      "";

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/soil_properties/",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ lat: centerLat, lng: centerLng, city }),
        }
      );
      if (!response.ok) throw new Error("Failed to fetch soil data");
      const data = await response.json();
      setSoilData(data);
    } catch (error) {
      alert("Error fetching soil data: " + error.message);
    }
  };

  if (!districts) return <div>Loading Map...</div>;

  // Find carbon stock for the selected district (if any)
  const selectedDistrictName =
    selectedDistrict?.properties?.NAME_2 ||
    selectedDistrict?.properties?.district ||
    selectedDistrict?.properties?.name ||
    "";

  return (
    <div style={{ height: "100vh", width: "100vw" }}>
      <MapContainer
        center={rajasthanCenter}
        zoom={6.5}
        style={{ height: "100vh", width: "100vw" }}
      >
        <TileLayer
          url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
          attribution="Tiles © Esri"
        />

        {selectedDistrict === null ? (
          <GeoJSON
            data={districts}
            style={(feature) => ({
              fillColor: getDistrictColor(
                feature.properties.NAME_2 ||
                  feature.properties.district ||
                  feature.properties.name,
                carbonStock,
                districts
              ),
              color: "white",
              weight: 1,
              fillOpacity: 0.75,
              cursor: "pointer",
            })}
            onEachFeature={(feature, layer) => {
              const districtName =
                feature.properties.NAME_2 ||
                feature.properties.district ||
                feature.properties.name;
              const value = carbonStock[districtName] || 0;
              layer.bindTooltip(
                `${districtName}${
                  value
                    ? " (Carbon: " +
                      Math.round(value).toLocaleString() +
                      " kg CO₂e)"
                    : ""
                }`,
                {
                  permanent: true,
                  direction: "center",
                  className: "district-label",
                }
              );

              layer.on({
                mouseover: (e) => {
                  e.target.setStyle({ fillOpacity: 0.95, weight: 2 });
                },
                mouseout: (e) => {
                  e.target.setStyle({ fillOpacity: 0.75, weight: 1 });
                },
                click: onDistrictClick,
              });
            }}
          />
        ) : (
          <>
            <GeoJSON
              data={selectedDistrict}
              style={{
                fillColor: "#6dd47e",
                color: "#2f855a",
                weight: 3,
                fillOpacity: 0.8,
              }}
            />

            {gridLines && (
              <>
                {gridLines.hLines.map((line, i) => (
                  <Polyline
                    key={"h" + i}
                    positions={line.map(([lat, lng]) => [lat, lng])}
                    pathOptions={{ color: "red", weight: 1, opacity: 0.5 }}
                  />
                ))}
                {gridLines.vLines.map((line, i) => (
                  <Polyline
                    key={"v" + i}
                    positions={line.map(([lat, lng]) => [lat, lng])}
                    pathOptions={{ color: "red", weight: 1, opacity: 0.5 }}
                  />
                ))}
              </>
            )}

            {gridCells &&
              gridCells.map(({ cell, index }) => {
                const cultivable = cultivableMap[index] !== 0;
                return (
                  <Polygon
                    key={index}
                    positions={cell}
                    pathOptions={{
                      color: cultivable ? "orange" : "#222",
                      weight: 1,
                      fillOpacity: cultivable ? 0.08 : 0.7,
                      fillColor: cultivable ? "#fffbe6" : "#222",
                      dashArray: cultivable ? null : "4 4",
                      opacity: 1,
                    }}
                    eventHandlers={
                      cultivable ? { click: () => onCellClick(cell) } : {}
                    }
                  />
                );
              })}

            <div
              style={{
                position: "absolute",
                top: 10,
                left: 10,
                zIndex: 1000,
              }}
            >
              <button
                onClick={backToAll}
                style={{
                  padding: "8px 18px",
                  fontWeight: "bold",
                  background: "#fff",
                  borderRadius: "6px",
                  border: "1px solid #888",
                }}
              >
                ⬅ Back to All Districts
              </button>
            </div>
          </>
        )}

        {/* ---- LEGEND FOR CARBON HEATMAP ---- */}
        <div
          style={{
            position: "absolute",
            bottom: 20,
            left: 20,
            zIndex: 999,
            padding: 10,
            background: "#fff",
            borderRadius: 8,
            boxShadow: "0 2px 6px #0002",
            minWidth: 170,
          }}
        >
          <div style={{ fontWeight: 600, marginBottom: 4 }}>
            Carbon Stock (kg CO₂e)
          </div>
          <div style={{ display: "flex", alignItems: "center" }}>
            <div
              style={{
                width: 90,
                height: 16,
                background:
                  "linear-gradient(to right, #fffbe6 0%, #47bb55 100%)",
                borderRadius: 6,
                marginRight: 8,
              }}
            />
            <div style={{ fontSize: 13 }}>
              <span>
                {Math.round(
                  Math.min(...Object.values(carbonStock).filter((v) => v > 0) || [
                    0,
                  ])
                ).toLocaleString()}
              </span>
              {" - "}
              <span>
                {Math.round(
                  Math.max(...Object.values(carbonStock).filter((v) => v > 0) || [
                    0,
                  ])
                ).toLocaleString()}
              </span>
            </div>
          </div>
        </div>

        {/* ----- Floating Sidebar ----- */}
        {soilData && (
          <div
            style={{
              position: "absolute",
              top: 60,
              right: 25,
              zIndex: 2000,
              background: "#fff",
              padding: 22,
              borderRadius: 14,
              minWidth: 350,
              maxWidth: 400,
              boxShadow: "0 2px 10px #0002",
              maxHeight: "80vh",
              overflowY: "auto",
            }}
          >
            <h3 style={{ margin: "0 0 12px 0", color: "#1976d2" }}>
              Location Data
            </h3>

            {/* Carbon stock for selected district */}
            <h4 style={{ color: "#47bb55", marginBottom: 8 }}>
              Carbon Stock Estimate:
            </h4>
            <div style={{ fontWeight: 600, marginBottom: 15 }}>
              {carbonStock[selectedDistrictName]
                ? Math.round(carbonStock[selectedDistrictName]).toLocaleString() +
                  " kg CO₂e"
                : "No data"}
            </div>

            {/* Top important sections */}
            {soilData.soil_data && (
              <>
                <h4>Soil Data</h4>
                <ul>
                  {Object.entries(soilData.soil_data).map(([k, v]) => (
                    <li key={k}>
                      <b>{k}</b>: {v}
                    </li>
                  ))}
                </ul>
              </>
            )}

            {soilData.climate_data && (
              <>
                <h4>Climate Data</h4>
                <ul>
                  {Object.entries(soilData.climate_data).map(([k, v]) => (
                    <li key={k}>
                      <b>{k}</b>: {v}
                    </li>
                  ))}
                </ul>
              </>
            )}

            {/* Render other dynamic fields */}
            {Object.entries(soilData)
              .filter(([key]) => !["soil_data", "climate_data"].includes(key))
              .map(([key, value]) => (
                <div key={key} style={{ marginBottom: 16 }}>
                  <h4 style={{ marginBottom: 5 }}>
                    {key
                      .replace(/_/g, " ")
                      .replace(/\b\w/g, (c) => c.toUpperCase())}
                  </h4>
                  {Array.isArray(value) ? (
                    value.length > 0 ? (
                      <ul style={{ maxHeight: 120, overflowY: "auto" }}>
                        {value.map((item, i) =>
                          typeof item === "object" ? (
                            <li
                              key={i}
                              style={{
                                borderBottom: "1px solid #eee",
                                marginBottom: 6,
                              }}
                            >
                              {Object.entries(item).map(([k, v]) => (
                                <div key={k}>
                                  <b>{k}</b>: {String(v)}
                                </div>
                              ))}
                            </li>
                          ) : (
                            <li key={i}>{String(item)}</li>
                          )
                        )}
                      </ul>
                    ) : (
                      <div>No data available.</div>
                    )
                  ) : typeof value === "object" && value !== null ? (
                    <ul>
                      {Object.entries(value).map(([k, v]) => (
                        <li key={k}>
                          <b>{k}</b>: {String(v)}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <div>{String(value)}</div>
                  )}
                </div>
              ))}

            <button
              style={{
                marginTop: 12,
                padding: "7px 18px",
                borderRadius: 7,
                background: "#eee",
                border: "1px solid #888",
                cursor: "pointer",
                fontWeight: "bold",
                float: "right",
              }}
              onClick={() => setSoilData(null)}
            >
              Close
            </button>
          </div>
        )}

        {/* Show Carbon stock in sidebar even if no soilData */}
        {selectedDistrict && !soilData && (
          <div
            style={{
              position: "absolute",
              top: 60,
              right: 25,
              zIndex: 2000,
              background: "#fff",
              padding: 22,
              borderRadius: 14,
              minWidth: 350,
              maxWidth: 400,
              boxShadow: "0 2px 10px #0002",
              maxHeight: "80vh",
              overflowY: "auto",
            }}
          >
            <h3 style={{ margin: "0 0 12px 0", color: "#1976d2" }}>
              District Data
            </h3>
            <h4 style={{ color: "#47bb55", marginBottom: 8 }}>
              Carbon Stock Estimate:
            </h4>
            <div style={{ fontWeight: 600, marginBottom: 15 }}>
              {carbonStock[selectedDistrictName]
                ? Math.round(carbonStock[selectedDistrictName]).toLocaleString() +
                  " kg CO₂e"
                : "No data"}
            </div>
            <button
              style={{
                marginTop: 12,
                padding: "7px 18px",
                borderRadius: 7,
                background: "#eee",
                border: "1px solid #888",
                cursor: "pointer",
                fontWeight: "bold",
                float: "right",
              }}
              onClick={backToAll}
            >
              Close
            </button>
          </div>
        )}
      </MapContainer>
    </div>
  );
}
