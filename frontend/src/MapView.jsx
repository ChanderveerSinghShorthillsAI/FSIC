

// src/MapView.js
import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, GeoJSON, Polyline } from "react-leaflet";
import { generateGridLines } from "./utils";

const rajasthanCenter = [27.0238, 74.2179];

export default function MapView() {
  const [districts, setDistricts] = useState(null); // State to hold district boundaries
  const [selectedDistrict, setSelectedDistrict] = useState(null); // State to hold the currently selected district
  const [gridLines, setGridLines] = useState(null); // State to hold grid lines for the selected district

  // Load districts only
  useEffect(() => { 
    fetch(process.env.PUBLIC_URL + "/districts.geojson") // Fetch districts GeoJSON
      .then(res => res.json()) // Parse the response as JSON
      .then(setDistricts); // Set the districts state with the fetched data
  }, []);

  const onDistrictClick = (e) => { 
    const feature = e.target.feature; // Get the clicked district feature
    setSelectedDistrict(feature); // Set the selected district state

    // Generate grid lines for clicked district
    setGridLines(generateGridLines(feature.geometry, 0.03)); // Generate grid lines with a step of 0.05 degrees
  };

  const backToAll = () => { // Reset the selected district and grid lines
    setSelectedDistrict(null);
    setGridLines(null);
  };

  if (!districts) return <div>Loading Map...</div>;

  return (
    <div style={{ height: "100vh", width: "100vw" }}>
      <MapContainer center={rajasthanCenter} zoom={6.5} style={{ height: "100vh", width: "100vw" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {/* Show all districts for selection */}
        {selectedDistrict === null ? (
          <GeoJSON
            data={districts}
            style={{
              fillColor: "#1976d2",
              color: "white",
              weight: 1,
              fillOpacity: 0.5,
              cursor: "pointer"
            }}
            onEachFeature={(feature, layer) => {
              layer.on({
                click: onDistrictClick
              });
            }}
          />
        ) : (
          <>
            {/* Only show selected district */}
            <GeoJSON
              data={selectedDistrict}
              style={{
                fillColor: "#43a047",
                color: "#1b5e20",
                weight: 2,
                fillOpacity: 0.7
              }}
            />
            {/* Draw the grid lines */}
            {gridLines &&
              <>
                {gridLines.hLines.map((line, i) => (
                  <Polyline key={"h"+i} positions={line.map(([lat, lng]) => [lat, lng])} pathOptions={{ color: "red", weight: 1, opacity: 0.5 }} />
                ))}
                {gridLines.vLines.map((line, i) => (
                  <Polyline key={"v"+i} positions={line.map(([lat, lng]) => [lat, lng])} pathOptions={{ color: "red", weight: 1, opacity: 0.5 }} />
                ))}
              </>
            }
            {/* Back button */}
            <div style={{
              position: "absolute", top: 10, left: 10, zIndex: 1000
            }}>
              <button onClick={backToAll} style={{ padding: "8px 18px", fontWeight: "bold", background: "#fff", borderRadius: "6px", border: "1px solid #888" }}>
                ⬅ Back to All Districts
              </button>
            </div>
          </>
        )}
      </MapContainer>
    </div>
  );
}
