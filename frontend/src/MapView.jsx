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

// const rajasthanCenter = [27.0238, 74.2179];

// export default function MapView() {
//   const [districts, setDistricts] = useState(null); // State to hold district boundaries
//   const [selectedDistrict, setSelectedDistrict] = useState(null); // State to hold the currently selected district
//   const [gridLines, setGridLines] = useState(null); // State to hold grid lines for the selected district
//   const [gridCells, setGridCells] = useState(null); //
//   const [soilData, setSoilData] = useState(null);

//   // Load districts only
//   useEffect(() => {
//     fetch(process.env.PUBLIC_URL + "/districts.geojson") // Fetch districts GeoJSON
//       .then((res) => res.json()) // Parse the response as JSON
//       .then(setDistricts); // Set the districts state with the fetched data
//   }, []);

//   const onDistrictClick = (e) => {
//     const feature = e.target.feature; // Get the clicked district feature
//     setSelectedDistrict(feature); // Set the selected district state

//     // Generate grid lines for clicked district
//     setGridLines(generateGridLines(feature.geometry, 0.05)); // Generate grid lines with a step of 0.05 degrees
//     setGridCells(generateGridCells(feature.geometry, 0.05));
//   };

//   const backToAll = () => {
//     // Reset the selected district and grid lines
//     setSelectedDistrict(null);
//     setGridLines(null);
//   };

//   const onCellClick = async (cell) => {
//     const centerLat = (cell[0][0] + cell[2][0]) / 2;
//     const centerLng = (cell[0][1] + cell[2][1]) / 2;
//     const city =
//       selectedDistrict?.properties?.NAME_2 ||
//       selectedDistrict?.properties?.district ||
//       selectedDistrict?.properties?.name ||
//       "";

//     try {
//       const response = await fetch(
//         "http://127.0.0.1:8000/api/soil_properties/",
//         {
//           method: "POST",
//           headers: {
//             "Content-Type": "application/json",
//           },
//           body: JSON.stringify({ lat: centerLat, lng: centerLng, city }),
//         }
//       );

//       if (!response.ok) {
//         throw new Error("Failed to fetch soil data");
//       }

//       const data = await response.json();

//       const soilStr = Object.entries(data.soil_data)
//         .map(([key, value]) => `${key}: ${value}`)
//         .join("\n");
//       const climateStr =
//         data.climate_data && Object.keys(data.climate_data).length
//           ? Object.entries(data.climate_data)
//               .map(([k, v]) => `${k}: ${v}`)
//               .join("\n")
//           : "No climate data found.";
//       // const forestStr =
//       //   data.forest_population_data &&
//       //   Object.keys(data.forest_population_data).length
//       //     ? Object.entries(data.forest_population_data)
//       //         .map(([k, v]) => `${k}: ${v}`)
//       //         .join("\n")
//       //     : "No forest/population data found.";
//       console.log("Forest Data:", data.forest_population_data);

//       const forestStr =
//         data.forest_population_data &&
//         Object.keys(data.forest_population_data).length
//           ? Object.entries(data.forest_population_data)
//               .map(([k, v]) => `${k}: ${v}`)
//               .join("\n")
//           : "No forest/population data found.";

//       alert(
//         "Soil Data:\n" +
//           soilStr +
//           "\n\nClimate Data:\n" +
//           climateStr +
//           "\n\nForest/Population Data:\n" +
//           forestStr
//       );
//       setSoilData(data.soil_data);
//     } catch (error) {
//       alert("Error fetching soil data: " + error.message);
//     }
//   };

//   if (!districts) return <div>Loading Map...</div>;

//   return (
//     <div style={{ height: "100vh", width: "100vw" }}>
//       <MapContainer
//         center={rajasthanCenter}
//         zoom={6.5}
//         style={{ height: "100vh", width: "100vw" }}
//       >
//         <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
//         {/* Show all districts for selection */}
//         {selectedDistrict === null ? (
//           <GeoJSON
//             data={districts}
//             style={{
//               fillColor: "#1976d2",
//               color: "white",
//               weight: 1,
//               fillOpacity: 0.5,
//               cursor: "pointer",
//             }}
//             onEachFeature={(feature, layer) => {
//               layer.on({
//                 click: onDistrictClick,
//               });
//             }}
//           />
//         ) : (
//           <>
//             {/* Only show selected district */}
//             <GeoJSON
//               data={selectedDistrict}
//               style={{
//                 fillColor: "#43a047",
//                 color: "#1b5e20",
//                 weight: 2,
//                 fillOpacity: 0.7,
//               }}
//             />
//             {/* Draw the grid lines */}
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
//               gridCells.map((cell, idx) => (
//                 <Polygon
//                   key={idx}
//                   positions={cell}
//                   pathOptions={{
//                     color: "orange",
//                     weight: 1,
//                     fillOpacity: 0.08,
//                   }}
//                   eventHandlers={{
//                     click: () => onCellClick(cell),
//                   }}
//                 />
//               ))}

//             {/* Back button */}
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

const rajasthanCenter = [27.0238, 74.2179];

export default function MapView() {
  const [districts, setDistricts] = useState(null);
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [gridLines, setGridLines] = useState(null);
  const [gridCells, setGridCells] = useState(null);
  const [soilData, setSoilData] = useState(null);

  useEffect(() => {
    fetch(process.env.PUBLIC_URL + "/districts.geojson")
      .then((res) => res.json())
      .then(setDistricts);
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
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ lat: centerLat, lng: centerLng, city }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch soil data");
      }

      const data = await response.json();
      setSoilData({
        soil: data.soil_data,
        climate: data.climate_data,
        forest: data.forest_population_data,
      });
    } catch (error) {
      alert("Error fetching soil data: " + error.message);
    }
  };

  if (!districts) return <div>Loading Map...</div>;

  return (
    <div style={{ height: "100vh", width: "100vw" }}>
      <MapContainer
        center={rajasthanCenter}
        zoom={6.5}
        style={{ height: "100vh", width: "100vw" }}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {selectedDistrict === null ? (
          <GeoJSON
            data={districts}
            style={{
              fillColor: "#1976d2",
              color: "white",
              weight: 1,
              fillOpacity: 0.5,
              cursor: "pointer",
            }}
            onEachFeature={(feature, layer) => {
              layer.on({
                click: onDistrictClick,
              });
            }}
          />
        ) : (
          <>
            <GeoJSON
              data={selectedDistrict}
              style={{
                fillColor: "#43a047",
                color: "#1b5e20",
                weight: 2,
                fillOpacity: 0.7,
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
              gridCells.map((cell, idx) => (
                <Polygon
                  key={idx}
                  positions={cell}
                  pathOptions={{
                    color: "orange",
                    weight: 1,
                    fillOpacity: 0.08,
                  }}
                  eventHandlers={{
                    click: () => onCellClick(cell),
                  }}
                />
              ))}

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
