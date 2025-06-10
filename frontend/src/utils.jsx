

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
// src/utils.js
export function generateGridCells(geometry, step = 0.05) {
  const bbox = turf.bbox(geometry);
  const [minLng, minLat, maxLng, maxLat] = bbox;
  const cells = [];
  for (let lat = Math.ceil(minLat / step) * step; lat < maxLat; lat += step) {
    for (let lng = Math.ceil(minLng / step) * step; lng < maxLng; lng += step) {
      // Rectangle (polygon, closed)
      const cell = [
        [lat, lng],
        [lat, lng + step],
        [lat + step, lng + step],
        [lat + step, lng],
        [lat, lng] // closing
      ];
      // Convert for Turf [lng, lat]
      const cellLngLat = cell.map(([a, b]) => [b, a]);
      const cellPoly = turf.polygon([cellLngLat]);
      if (turf.booleanIntersects(cellPoly, geometry)) {
        cells.push(cell);
      }
    }
  }
  return cells;
}
