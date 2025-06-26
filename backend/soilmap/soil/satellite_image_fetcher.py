
import os
import csv
from sentinelhub import SHConfig, MimeType, CRS, BBox, SentinelHubRequest, DataCollection, bbox_to_dimensions

# ==== SentinelHub Credentials ====
INSTANCE_ID = 'c675c71a-a3e2-461b-829b-28281bec0b85'
CLIENT_ID = '82c6ea8b-525e-415a-8ffc-6a2df72dc7b1'
CLIENT_SECRET = '4tQ5X8LmCcqbwT9BZzJ6vzIeu4iWV9Fv'

config = SHConfig()
config.instance_id = INSTANCE_ID
config.sh_client_id = CLIENT_ID
config.sh_client_secret = CLIENT_SECRET

# ==== Input: CSV of grid cells ====
GRID_CSV = "rajasthan_grid_cells.csv"  # Change path if needed

# ==== Output Folder ====
OUT_DIR = "sat_images"
os.makedirs(OUT_DIR, exist_ok=True)

# ==== SentinelHub Evalscript (RGB with brightness correction) ====
# Brightness scaling is done by multiplying reflectance values
EVALSCRIPT = """
//VERSION=3
function setup() {
  return {
    input: ["B04", "B03", "B02"],
    output: { bands: 3 }
  };
}

function evaluatePixel(sample) {
  // Boost brightness by scaling (you can change 2.5 to 3.0 or more if still too dark)
  return [sample.B04 * 2.5, sample.B03 * 2.5, sample.B02 * 2.5];
}
"""

def fetch_sat_image(min_lng, min_lat, max_lng, max_lat, out_path):
    bbox = BBox(bbox=[min_lng, min_lat, max_lng, max_lat], crs=CRS.WGS84) # Define the bounding box for the area of interest
    size = bbox_to_dimensions(bbox, resolution=10) # 10 meters per pixel (high-res)

    request = SentinelHubRequest(
        evalscript=EVALSCRIPT,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=('2023-01-01', '2023-12-31'),
            )
        ],
        responses=[SentinelHubRequest.output_response('default', MimeType.PNG)],
        bbox=bbox,
        size=size,
        config=config,
        data_folder=OUT_DIR
    )
    data = request.get_data(save_data=True) # Fetch the data and save it to the specified folder
    saved_rel = request.get_filename_list()[0] # Get the relative path of the saved image
    saved = os.path.join(OUT_DIR, saved_rel) # Construct the full path to the saved image
    os.rename(saved, out_path)
    temp_folder = os.path.dirname(saved)
    if os.path.exists(temp_folder) and not os.listdir(temp_folder):
        os.rmdir(temp_folder)
    print(f"Downloaded: {out_path}")

# ==== Main: Download images for all grid cells ====
with open(GRID_CSV, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        min_lng = float(row["min_lng"]) # Convert string to float
        min_lat = float(row["min_lat"])
        max_lng = float(row["max_lng"])
        max_lat = float(row["max_lat"])
        center_lat = (min_lat + max_lat) / 2 # Calculate the center latitude
        center_lng = (min_lng + max_lng) / 2 # Calculate the center longitude
        out_path = os.path.join(OUT_DIR, f"grid_{center_lat:.5f}_{center_lng:.5f}.png")
        if os.path.exists(out_path):
            print(f"Already exists: {out_path}")
            continue
        try:
            fetch_sat_image(min_lng, min_lat, max_lng, max_lat, out_path)
        except Exception as e:
            print(f"Error for bbox {min_lng},{min_lat},{max_lng},{max_lat}: {e}")


