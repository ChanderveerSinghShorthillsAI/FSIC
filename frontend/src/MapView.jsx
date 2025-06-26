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

export default function MapView() { 
  const [districts, setDistricts] = useState(null); // State to hold district GeoJSON data
  const [selectedDistrict, setSelectedDistrict] = useState(null); // State to hold the selected district
  const [gridLines, setGridLines] = useState(null);// State to hold grid lines
  const [gridCells, setGridCells] = useState(null); // State to hold grid cells
  const [soilData, setSoilData] = useState(null); // State to hold soil data
  const [cultivableMap, setCultivableMap] = useState({}); // State to hold cultivable map data

  useEffect(() => { // Fetch district GeoJSON data
    fetch(process.env.PUBLIC_URL + "/districts.geojson")
      .then((res) => res.json())
      .then(setDistricts);
  }, []);
  useEffect(() => { // Log when districts are loaded
    fetch("http://127.0.0.1:8000/api/cultivable_grids/")
      .then((res) => res.json())
      .then(setCultivableMap);
  }, []);
  useEffect(() => { // Log when cultivableMap is loaded
    console.log("cultivableMap loaded:", cultivableMap);
  }, [cultivableMap]);

  const onDistrictClick = (e) => { // Handle district click event
    const feature = e.target.feature;
    setSelectedDistrict(feature); // Set the selected district
    setGridLines(generateGridLines(feature.geometry, 0.05)); // Generate grid lines for the selected district
    setGridCells(generateGridCells(feature.geometry, 0.05)); // Generate grid cells for the selected district
  };

  const backToAll = () => { // Handle back button click to reset state
    setSelectedDistrict(null);
    setGridLines(null);
    setSoilData(null);
  };

  const onCellClick = async (cell) => { // Handle cell click event to fetch soil data
    const centerLat = (cell[0][0] + cell[2][0]) / 2; // Calculate center latitude of the cell
    const centerLng = (cell[0][1] + cell[2][1]) / 2; // Calculate center longitude of the cell
    const city = // Get the city name from the selected district
      selectedDistrict?.properties?.NAME_2 || // Fallback to district name
      selectedDistrict?.properties?.district || // Fallback to district property
      selectedDistrict?.properties?.name || // Fallback to name property
      "";

    try {
      const response = await fetch( // Fetch soil data from the API
        "http://127.0.0.1:8000/api/soil_properties/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ lat: centerLat, lng: centerLng, city }), // Send latitude, longitude, and city in the request body
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch soil data");
      }

      const data = await response.json(); // Parse the JSON response
      setSoilData({ // Set the soil data state with the fetched data
        soil: data.soil_data,
        climate: data.climate_data,
        forest: data.forest_population_data,
        river: data.river_data,
        estimatedArea: data.estimated_area_data,
        rainfall: data.rainfall_data,
        wellDepth: data.well_depth_data,
        waterUsage: data.water_usage_data,
        soilAnalysis: data.soil_analysis_data,
        cropProduction: data.crop_production_data,
        cropPrice: data.crop_price_data, // <--- NEW!
      });
    } catch (error) {
      alert("Error fetching soil data: " + error.message); // Show error message if fetch fails
    }
  };

  useEffect(() => { // Log the cultivableMap keys when it changes
    console.log(
      "First 10 cultivableMap keys:",
      Object.keys(cultivableMap).slice(0, 10)
    );
  }, [cultivableMap]);

  function findClosestCultivable(centerLat, centerLng, cultivableMap) {
    const EPSILON = 0.00012; // slightly more than 0.0001 for 5 decimal places
    let foundKey = null;
    for (const k of Object.keys(cultivableMap)) {
      const [lat, lng] = k.split(",").map(Number);
      if (
        Math.abs(lat - centerLat) < EPSILON &&
        Math.abs(lng - centerLng) < EPSILON
      ) {
        foundKey = k;
        break;
      }
    }
    return foundKey ? cultivableMap[foundKey] : undefined;
  }

  if (!districts) return <div>Loading Map...</div>;

  return (
    <div style={{ height: "100vh", width: "100vw" }}>
      <MapContainer // Main map container
        center={rajasthanCenter}
        zoom={6.5}
        style={{ height: "100vh", width: "100vw" }}
      >
        {/* <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" /> */}
        <TileLayer // Tile layer for the map background
          url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
          attribution="Tiles © Esri"
        />

        {selectedDistrict === null ? ( // If no district is selected, show all districts
          // <GeoJSON
          //   data={districts}
          //   style={{
          //     fillColor: "#1976d2",
          //     color: "white",
          //     weight: 1,
          //     fillOpacity: 0.5,
          //     cursor: "pointer",
          //   }}
          //   onEachFeature={(feature, layer) => {
          //     layer.on({
          //       click: onDistrictClick,
          //     });
          //   }}
          // />
          <GeoJSON // Main GeoJSON layer for districts
            data={districts} // Use the districts GeoJSON data
            style={() => ({ // Style for each district
              fillColor: "#88c0f7", 
              color: "white",
              weight: 1,
              fillOpacity: 0.6,
              cursor: "pointer",
            })}
            onEachFeature={(feature, layer) => {
              layer.bindTooltip(
                feature.properties.NAME_2 ||
                  feature.properties.district ||
                  feature.properties.name,
                {
                  permanent: true,
                  direction: "center",
                  className: "district-label",
                }
              );

              layer.on({
                mouseover: (e) => {
                  e.target.setStyle({
                    fillOpacity: 0.9,
                    weight: 2,
                  });
                },
                mouseout: (e) => {
                  e.target.setStyle({
                    fillOpacity: 0.6,
                    weight: 1,
                  });
                },
                click: onDistrictClick,
              });
            }}
          />
        ) : (
          <>
            {/* <GeoJSON
              data={selectedDistrict}
              style={{
                fillColor: "#43a047",
                color: "#1b5e20",
                weight: 2,
                fillOpacity: 0.7,
              }}
            /> */}
            <GeoJSON
              data={selectedDistrict}
              style={{
                fillColor: "#6dd47e", // More vivid green
                color: "#2f855a", // Dark green boundary
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
                const cultivable = cultivableMap[index] !== 0; // index-based lookup
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

        {/* Floating Sidebar for Data */}
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
            <h4 style={{ marginBottom: 5 }}>Soil Data</h4>
            <ul style={{ marginBottom: 16 }}>
              {Object.entries(soilData.soil).map(([k, v]) => (
                <li key={k}>
                  <b>{k}</b>: {v}
                </li>
              ))}
            </ul>
            <h4 style={{ marginBottom: 5 }}>Climate Data</h4>
            <ul style={{ marginBottom: 16 }}>
              {Object.entries(soilData.climate).map(([k, v]) => (
                <li key={k}>
                  <b>{k}</b>: {v}
                </li>
              ))}
            </ul>
            <h4 style={{ marginBottom: 5 }}>Forest & Population Data</h4>
            <ul style={{ marginBottom: 8 }}>
              {Object.entries(soilData.forest).map(([k, v]) => (
                <li key={k}>
                  <b>{k}</b>: {v}
                </li>
              ))}
            </ul>
            <h4 style={{ marginBottom: 5 }}>Rivers in District</h4>
            <ul style={{ marginBottom: 8 }}>
              {soilData.river && soilData.river.length > 0 ? (
                soilData.river.map((r, i) => (
                  <li key={i}>
                    <b>{r["Name of River"]}</b> (Area: {r["Area in Ha."]} Ha)
                  </li>
                ))
              ) : (
                <li>No rivers found in this district.</li>
              )}
            </ul>
            <h4 style={{ marginBottom: 5 }}>Estimated Area (Ha)</h4>
            <div style={{ marginBottom: 12, fontWeight: 500 }}>
              {soilData.estimatedArea
                ? soilData.estimatedArea
                : "Not available"}
            </div>
            <h4 style={{ marginBottom: 5 }}>Rainfall Data</h4>
            {soilData.rainfall && Object.keys(soilData.rainfall).length > 0 ? (
              <ul style={{ marginBottom: 12 }}>
                {Object.entries(soilData.rainfall).map(([k, v]) =>
                  k !== "District" ? (
                    <li key={k}>
                      <b>{k}</b>: {v}
                    </li>
                  ) : null
                )}
              </ul>
            ) : (
              <div style={{ marginBottom: 12 }}>
                No rainfall data available.
              </div>
            )}
            <h4 style={{ marginBottom: 5 }}>Well Water Depth Analysis</h4>
            {soilData.wellDepth &&
            Object.keys(soilData.wellDepth).length > 0 ? (
              <ul style={{ marginBottom: 12 }}>
                {Object.entries(soilData.wellDepth).map(([k, v]) =>
                  k !== "District Name" && k !== "Sr. No." ? (
                    <li key={k}>
                      <b>{k}</b>: {v}
                    </li>
                  ) : null
                )}
              </ul>
            ) : (
              <div style={{ marginBottom: 12 }}>
                No well depth data available.
              </div>
            )}
            <h4 style={{ marginBottom: 5 }}>Water Usage Data</h4>
            {soilData.waterUsage &&
            Object.keys(soilData.waterUsage).length > 0 ? (
              <ul style={{ marginBottom: 12 }}>
                {Object.entries(soilData.waterUsage).map(([k, v]) =>
                  k !== "District" ? (
                    <li key={k}>
                      <b>{k}</b>: {v}
                    </li>
                  ) : null
                )}
              </ul>
            ) : (
              <div style={{ marginBottom: 12 }}>
                No water usage data available.
              </div>
            )}

            <h4 style={{ marginBottom: 5 }}>Soil Analysis Data</h4>
            {Array.isArray(soilData.soilAnalysis) &&
            soilData.soilAnalysis.length > 0 ? (
              <ul
                style={{ marginBottom: 12, maxHeight: 200, overflowY: "auto" }}
              >
                {soilData.soilAnalysis.map((row, idx) => (
                  <li
                    key={idx}
                    style={{ marginBottom: 8, borderBottom: "1px solid #eee" }}
                  >
                    {Object.entries(row).map(([k, v]) =>
                      k !== "District" ? (
                        <div key={k}>
                          <b>{k}</b>: {v}
                        </div>
                      ) : null
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <div style={{ marginBottom: 12 }}>
                No soil analysis data available.
              </div>
            )}

            <h4 style={{ marginBottom: 5 }}>Crop Production Data</h4>
            {Array.isArray(soilData.cropProduction) &&
            soilData.cropProduction.length > 0 ? (
              <ul
                style={{ marginBottom: 12, maxHeight: 200, overflowY: "auto" }}
              >
                {soilData.cropProduction.map((row, idx) => (
                  <li
                    key={idx}
                    style={{ marginBottom: 8, borderBottom: "1px solid #eee" }}
                  >
                    {Object.entries(row).map(([k, v]) =>
                      k !== "District" ? (
                        <div key={k}>
                          <b>{k}</b>: {v}
                        </div>
                      ) : null
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <div style={{ marginBottom: 12 }}>
                No crop production data available.
              </div>
            )}

            <h4 style={{ marginBottom: 5 }}>Crop Price Data</h4>
            {Array.isArray(soilData.cropPrice) &&
            soilData.cropPrice.length > 0 ? (
              <ul
                style={{ marginBottom: 12, maxHeight: 200, overflowY: "auto" }}
              >
                {soilData.cropPrice.map((row, idx) => (
                  <li
                    key={idx}
                    style={{ marginBottom: 8, borderBottom: "1px solid #eee" }}
                  >
                    {Object.entries(row).map(([k, v]) =>
                      k !== "District" ? (
                        <div key={k}>
                          <b>{k}</b>: {v}
                        </div>
                      ) : null
                    )}
                  </li>
                ))}
              </ul>
            ) : (
              <div style={{ marginBottom: 12 }}>
                No crop price data available.
              </div>
            )}

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
      </MapContainer>
    </div>
  );
}

// import React, { useEffect, useState } from "react";
// import {
//   MapContainer,
//   TileLayer,
//   GeoJSON,
//   Polyline,
//   Polygon,
// } from "react-leaflet";
// import "leaflet/dist/leaflet.css"; // Import Leaflet CSS for proper styling
// import { generateGridLines, generateGridCells } from "./utils";

// const rajasthanCenter = [27.0238, 74.2179]; // Center of Rajasthan

// export default function MapView() {
//   const [districts, setDistricts] = useState(null); // State to hold district GeoJSON data
//   const [selectedDistrict, setSelectedDistrict] = useState(null); // State to hold the selected district
//   const [gridLines, setGridLines] = useState(null); // State to hold grid lines
//   const [gridCells, setGridCells] = useState(null); // State to hold grid cells
//   const [soilData, setSoilData] = useState(null); // State to hold all fetched data
//   const [cultivableMap, setCultivableMap] = useState({}); // State to hold cultivable map data
//   const [loading, setLoading] = useState(false); // State to handle loading status
//   const [error, setError] = useState(null); // State to handle errors

//   // Fetch district GeoJSON data
//   useEffect(() => {
//     fetch(process.env.PUBLIC_URL + "/districts.geojson")
//       .then((res) => res.json())
//       .then(setDistricts)
//       .catch((err) => setError("Failed to load district data: " + err.message));
//   }, []);

//   // Fetch cultivable grid data
//   useEffect(() => {
//     setLoading(true);
//     fetch("http://127.0.0.1:8000/api/cultivable_grids/")
//       .then((res) => {
//         if (!res.ok) throw new Error("Failed to fetch cultivable grid data");
//         return res.json();
//       })
//       .then(setCultivableMap)
//       .catch((err) => setError(err.message))
//       .finally(() => setLoading(false));
//   }, []);

//   // Log cultivableMap keys for debugging
//   useEffect(() => {
//     console.log("First 10 cultivableMap keys:", Object.keys(cultivableMap).slice(0, 10));
//   }, [cultivableMap]);

//   // Handle district click event
//   const onDistrictClick = (e) => {
//     const feature = e.target.feature;
//     setSelectedDistrict(feature);
//     setGridLines(generateGridLines(feature.geometry, 0.05));
//     setGridCells(generateGridCells(feature.geometry, 0.05));
//     setSoilData(null); // Reset soil data when selecting a new district
//   };

//   // Handle back button click to reset state
//   const backToAll = () => {
//     setSelectedDistrict(null);
//     setGridLines(null);
//     setGridCells(null);
//     setSoilData(null);
//     setError(null);
//   };

//   // Handle cell click event to fetch all data
//   const onCellClick = async (cell) => {
//     const centerLat = (cell[0][0] + cell[2][0]) / 2;
//     const centerLng = (cell[0][1] + cell[2][1]) / 2;
//     const city =
//       selectedDistrict?.properties?.NAME_2 ||
//       selectedDistrict?.properties?.district ||
//       selectedDistrict?.properties?.name ||
//       "";

//     setLoading(true);
//     setError(null);
//     try {
//       const response = await fetch("http://127.0.0.1:8000/api/soil_properties/", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({ lat: centerLat, lng: centerLng, city }),
//       });

//       if (!response.ok) {
//         throw new Error(`Failed to fetch data: ${response.statusText}`);
//       }

//       const data = await response.json();
//       setSoilData({
//         soil: data.soil_data || {},
//         climate: data.climate_data || {},
//         forest: data.forest_population_data || {},
//         river: data.river_data || [],
//         estimatedArea: data.estimated_area_data || "Not available",
//         rainfall: data.rainfall_data || {},
//         wellDepth: data.well_depth_data || {},
//         waterUsage: data.water_usage_data || {},
//         soilAnalysis: data.soil_analysis_data || [],
//         cropProduction: data.crop_production_data || [],
//         cropPrice: data.crop_price_data || [],
//       });
//     } catch (error) {
//       setError("Error fetching data: " + error.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   // Find closest cultivable status
//   function findClosestCultivable(centerLat, centerLng, cultivableMap) {
//     const EPSILON = 0.00012; // Slightly more than 0.0001 for 5 decimal places
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

//   // Render loading or error states
//   if (loading && !soilData) return <div style={{ padding: 20 }}>Loading Map...</div>;
//   if (error && !districts) return <div style={{ color: "red", padding: 20 }}>{error}</div>;
//   if (!districts) return <div style={{ padding: 20 }}>Loading Map...</div>;

//   return (
//     <div style={{ height: "100vh", width: "100vw", position: "relative" }}>
//       <MapContainer
//         center={rajasthanCenter}
//         zoom={6.5}
//         style={{ height: "100vh", width: "100vw" }}
//       >
//         <TileLayer
//           url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
//           attribution="Tiles © Esri"
//         />

//         {selectedDistrict === null ? (
//           <GeoJSON
//             data={districts}
//             style={() => ({
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
//                   feature.properties.name ||
//                   "Unknown",
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
//             <GeoJSON
//               data={selectedDistrict}
//               style={{
//                 fillColor: "#6dd47e",
//                 color: "#2f855a",
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
//                 const cultivable = cultivableMap[index] !== 0;
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
//           </>
//         )}
//       </MapContainer>

//       {/* Back Button */}
//       {selectedDistrict && (
//         <div
//           style={{
//             position: "absolute",
//             top: 10,
//             left: 10,
//             zIndex: 1000,
//           }}
//         >
//           <button
//             onClick={backToAll}
//             style={{
//               padding: "8px 18px",
//               fontWeight: "bold",
//               background: "#fff",
//               borderRadius: "6px",
//               border: "1px solid #888",
//               cursor: "pointer",
//               fontSize: "14px",
//             }}
//           >
//             ⬅ Back to All Districts
//           </button>
//         </div>
//       )}

//       {/* Floating Sidebar for Data */}
//       {soilData && (
//         <div
//           style={{
//             position: "absolute",
//             top: 60,
//             right: 25,
//             zIndex: 2000,
//             background: "#fff",
//             padding: "20px",
//             borderRadius: "12px",
//             minWidth: "350px",
//             maxWidth: "450px",
//             boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
//             maxHeight: "80vh",
//             overflowY: "auto",
//             fontFamily: "'Arial', sans-serif",
//             fontSize: "14px",
//             lineHeight: "1.5",
//           }}
//         >
//           <h3 style={{ margin: "0 0 15px 0", color: "#1976d2", fontSize: "18px" }}>
//             Location Data
//           </h3>

//           {loading ? (
//             <div style={{ color: "#666", padding: "10px" }}>Loading data...</div>
//           ) : error ? (
//             <div style={{ color: "red", padding: "10px" }}>{error}</div>
//           ) : (
//             <>
//               {/* Soil Data */}
//               <h4 style={{ margin: "0 0 8px 0", color: "#333", fontSize: "16px" }}>
//                 Soil Properties
//               </h4>
//               {Object.keys(soilData.soil).length > 0 ? (
//                 <ul style={{ margin: "0 0 20px 20px", padding: 0, listStyle: "none" }}>
//                   {Object.entries(soilData.soil).map(([key, value]) => (
//                     <li key={key} style={{ marginBottom: "6px" }}>
//                       <strong>{key.replace(/_/g, " ")}:</strong> {value}
//                     </li>
//                   ))}
//                 </ul>
//               ) : (
//                 <p style={{ color: "#666", margin: "0 0 20px 0" }}>
//                   No soil properties available.
//                 </p>
//               )}

//               {/* Climate Data */}
//               <h4 style={{ margin: "0 0 8px 0", color: "#333", fontSize: "16px" }}>
//                 Climate Data
//               </h4>
//               {Object.keys(soilData.climate).length > 0 ? (
//                 <ul style={{ margin: "0 0 20px 20px", padding: 0, listStyle: "none" }}>
//                   {Object.entries(soilData.climate).map(([key, value]) =>
//                     key !== "City" ? (
//                       <li key={key} style={{ marginBottom: "6px" }}>
//                         <strong>{key.replace(/_/g, " ")}:</strong> {value}
//                       </li>
//                     ) : null
//                   )}
//                 </ul>
//               ) : (
//                 <p style={{ color: "#666", margin: "0 0 20px 0" }}>
//                   No climate data available.
//                 </p>
//               )}

//               {/* Forest & Population Data */}
//               <h4 style={{ margin: "0 0 8px 0", color: "#333", fontSize: "16px" }}>
//                 Forest & Population Data
//               </h4>
//               {Object.keys(soilData.forest).length > 0 ? (
//                 <ul style={{ margin: "0 0 20px 20px", padding: 0, listStyle: "none" }}>
//                   {Object.entries(soilData.forest).map(([key, value]) =>
//                     key !== "Name of District" ? (
//                       <li key={key} style={{ marginBottom: "6px" }}>
//                         <strong>{key.replace(/_/g, " ")}:</strong> {value}
//                       </li>
//                     ) : null
//                   )}
//                 </ul>
//               ) : (
//                 <p style={{ color: "#666", margin: "0 0 20px 0" }}>
//                   No forest or population data available.
//                 </p>
//               )}

//               {/* River Data */}
//               <h4 style={{ margin: "0 0 8px 0", color: "#333", fontSize: "16px" }}>
//                 Rivers in District
//               </h4>
//               {soilData.river && soilData.river.length > 0 ? (
//                 <ul style={{ margin: "0 0 20px 20px", padding: 0, listStyle: "none" }}>
//                   {soilData.river.map((river, index) => (
//                     <li key={index} style={{ marginBottom: "6px" }}>
//                       <strong>{river["Name of River"]}</strong> (Area: {river["Area in Ha."]} Ha)
//                     </li>
//                   ))}
//                 </ul>
//               ) : (
//                 <p style={{ color: "#666", margin: "0 0 20px 0" }}>
//                   No river data available.
//                 </p>
//               )}

//               {/* Estimated Area */}
//               <h4 style={{ margin: "0 0 8px 0", color: "#333", fontSize: "16px" }}>
//                 Estimated Ravine Area
//               </h4>
//               <p style={{ margin: "0 0 20px 0", color: "#333" }}>
//                 {soilData.estimatedArea || "Not available"}
//               </p>

//               {/* Rainfall Data */}
//               <h4 style={{ margin: "0 0 8px 0", color: "#333", fontSize: "16px" }}>
//                 Rainfall Data
//               </h4>
//               {Object.keys(soilData.rainfall).length > 0 ? (
//                 <ul style={{ margin: "0 0 20px 20px", padding: 0, listStyle: "none" }}>
//                   {Object.entries(soilData.rainfall).map(([key, value]) =>
//                     key !== "District" ? (
//                       <li key={key} style={{ marginBottom: "6px" }}>
//                         <strong>{key.replace(/_/g, " ")}:</strong> {value}
//                       </li>
//                     ) : null
//                   )}
//                 </ul>
//               ) : (
//                 <p style={{ color: "#666", margin: "0 0 20px 0" }}>
//                   No rainfall data available.
//                 </p>
//               )}

//               {/* Well Depth Data */}
//               <h4 style={{ margin: "0 0 8px 0", color: "#333", fontSize: "16px" }}>
//                 Well Water Depth
//               </h4>
//               {Object.keys(soilData.wellDepth).length > 0 ? (
//                 <ul style={{ margin: "0 0 20px 20px", padding: 0, listStyle: "none" }}>
//                   {Object.entries(soilData.wellDepth).map(([key, value]) =>
//                     key !== "District Name" && key !== "Sr. No." ? (
//                       <li key={key} style={{ marginBottom: "6px" }}>
//                         <strong>{key.replace(/_/g, " ")}:</strong> {value}
//                       </li>
//                     ) : null
//                   )}
//                 </ul>
//               ) : (
//                 <p style={{ color: "#666", margin: "0 0 20px 0" }}>
//                   No well depth data available.
//                 </p>
//               )}

//               {/* Water Usage Data */}
//               <h4 style={{ margin: "0 0 8px 0", color: "#333", fontSize: "16px" }}>
//                 Water Usage
//               </h4>
//               {Object.keys(soilData.waterUsage).length > 0 ? (
//                 <ul style={{ margin: "0 0 20px 20px", padding: 0, listStyle: "none" }}>
//                   {Object.entries(soilData.waterUsage).map(([key, value]) =>
//                     key !== "District" ? (
//                       <li key={key} style={{ marginBottom: "6px" }}>
//                         <strong>{key.replace(/_/g, " ")}:</strong> {value}
//                       </li>
//                     ) : null
//                   )}
//                 </ul>
//               ) : (
//                 <p style={{ color: "#666", margin: "0 0 20px 0" }}>
//                   No water usage data available.
//                 </p>
//               )}

//               {/* Soil Analysis Data */}
//               <h4 style={{ margin: "0 0 8px 0", color: "#333", fontSize: "16px" }}>
//                 Soil Analysis
//               </h4>
//               {Array.isArray(soilData.soilAnalysis) && soilData.soilAnalysis.length > 0 ? (
//                 <div style={{ margin: "0 0 20px 0", maxHeight: "200px", overflowY: "auto" }}>
//                   {soilData.soilAnalysis.map((row, index) => (
//                     <div
//                       key={index}
//                       style={{
//                         marginBottom: "10px",
//                         padding: "10px",
//                         border: "1px solid #eee",
//                         borderRadius: "4px",
//                       }}
//                     >
//                       <strong>Record {index + 1}</strong>
//                       <ul style={{ margin: "5px 0 0 20px", padding: 0, listStyle: "none" }}>
//                         {Object.entries(row).map(([key, value]) =>
//                           key !== "District" ? (
//                             <li key={key} style={{ marginBottom: "4px" }}>
//                               <strong>{key.replace(/_/g, " ")}:</strong> {value}
//                             </li>
//                           ) : null
//                         )}
//                       </ul>
//                     </div>
//                   ))}
//                 </div>
//               ) : (
//                 <p style={{ color: "#666", margin: "0 0 20px 0" }}>
//                   No soil analysis data available.
//                 </p>
//               )}

//               {/* Crop Production Data */}
//               <h4 style={{ margin: "0 0 8px 0", color: "#333", fontSize: "16px" }}>
//                 Crop Production
//               </h4>
//               {Array.isArray(soilData.cropProduction) && soilData.cropProduction.length > 0 ? (
//                 <div style={{ margin: "0 0 20px 0", maxHeight: "200px", overflowY: "auto" }}>
//                   {soilData.cropProduction.map((row, index) => (
//                     <div
//                       key={index}
//                       style={{
//                         marginBottom: "10px",
//                         padding: "10px",
//                         border: "1px solid #eee",
//                         borderRadius: "4px",
//                       }}
//                     >
//                       <strong>Record {index + 1}</strong>
//                       <ul style={{ margin: "5px 0 0 20px", padding: 0, listStyle: "none" }}>
//                         {Object.entries(row).map(([key, value]) =>
//                           key !== "District" ? (
//                             <li key={key} style={{ marginBottom: "4px" }}>
//                               <strong>{key.replace(/_/g, " ")}:</strong> {value}
//                             </li>
//                           ) : null
//                         )}
//                       </ul>
//                     </div>
//                   ))}
//                 </div>
//               ) : (
//                 <p style={{ color: "#666", margin: "0 0 20px 0" }}>
//                   No crop production data available.
//                 </p>
//               )}

//               {/* Crop Price Data */}
//               <h4 style={{ margin: "0 0 8px 0", color: "#333", fontSize: "16px" }}>
//                 Crop Prices
//               </h4>
//               {Array.isArray(soilData.cropPrice) && soilData.cropPrice.length > 0 ? (
//                 <div style={{ margin: "0 0 20px 0", maxHeight: "200px", overflowY: "auto" }}>
//                   {soilData.cropPrice.map((row, index) => (
//                     <div
//                       key={index}
//                       style={{
//                         marginBottom: "10px",
//                         padding: "10px",
//                         border: "1px solid #eee",
//                         borderRadius: "4px",
//                       }}
//                     >
//                       <strong>Record {index + 1}</strong>
//                       <ul style={{ margin: "5px 0 0 20px", padding: 0, listStyle: "none" }}>
//                         {Object.entries(row).map(([key, value]) =>
//                           key !== "District" ? (
//                             <li key={key} style={{ marginBottom: "4px" }}>
//                               <strong>{key.replace(/_/g, " ")}:</strong> {value}
//                             </li>
//                           ) : null
//                         )}
//                       </ul>
//                     </div>
//                   ))}
//                 </div>
//               ) : (
//                 <p style={{ color: "#666", margin: "0 0 20px 0" }}>
//                   No crop price data available.
//                 </p>
//               )}

//               <button
//                 style={{
//                   marginTop: "15px",
//                   padding: "8px 20px",
//                   borderRadius: "6px",
//                   background: "#f5f5f5",
//                   border: "1px solid #888",
//                   cursor: "pointer",
//                   fontWeight: "bold",
//                   fontSize: "14px",
//                   float: "right",
//                 }}
//                 onClick={() => setSoilData(null)}
//               >
//                 Close
//               </button>
//             </>
//           )}
//         </div>
//       )}
//     </div>
//   );
// }