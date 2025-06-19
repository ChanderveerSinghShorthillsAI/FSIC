import geopandas as gpd
import pandas as pd
import shapely.geometry

# --- Parameters ---
geojson_path = 'districts.geojson'  # Path to your Rajasthan/district GeoJSON
output_csv = 'rajasthan_grid_cells.csv'
grid_step = 0.05  # degrees, same as frontend

# --- Load Rajasthan Geometry (combine all districts if needed) ---
gdf = gpd.read_file(geojson_path)
if "NAME_1" in gdf.columns:
    raj_gdf = gdf[gdf["NAME_1"].str.lower().str.contains("rajasthan")]
else:
    raj_gdf = gdf
# Combine all features (if more than one) to get state-wide boundary
rajasthan_poly = raj_gdf.unary_union

# --- Compute bounding box ---
minx, miny, maxx, maxy = rajasthan_poly.bounds

# --- Generate grid ---
cells = []
lat = miny
while lat < maxy:
    lng = minx
    while lng < maxx:
        cell_poly = shapely.geometry.box(lng, lat, lng+grid_step, lat+grid_step)
        # Only include cells that intersect Rajasthan
        if cell_poly.intersects(rajasthan_poly):
            cells.append({
                "min_lng": lng,
                "min_lat": lat,
                "max_lng": lng+grid_step,
                "max_lat": lat+grid_step
            })
        lng += grid_step
    lat += grid_step

# --- Save to CSV ---
df = pd.DataFrame(cells)
df.to_csv(output_csv, index=False)
print(f"Saved {len(cells)} grid cells to {output_csv}")
