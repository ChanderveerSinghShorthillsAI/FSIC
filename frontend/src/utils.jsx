

// src/utils.js
import * as turf from "@turf/turf";

// Given a district geometry, returns arrays of polylines (as latlng arrays)
export function generateGridLines(geometry, step = 0.05) {
  const bbox = turf.bbox(geometry); // [minLng, minLat, maxLng, maxLat]
  const [minLng, minLat, maxLng, maxLat] = bbox;
  const hLines = [];
  const vLines = [];

  // Horizontal lines (latitude)
  for (let lat = Math.ceil(minLat / step) * step; lat <= maxLat; lat += step) {
    hLines.push([
      [lat, minLng],
      [lat, maxLng]
    ]);
  }
  // Vertical lines (longitude)
  for (let lng = Math.ceil(minLng / step) * step; lng <= maxLng; lng += step) {
    vLines.push([
      [minLat, lng],
      [maxLat, lng]
    ]);
  }
  return { hLines, vLines };
}
