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
