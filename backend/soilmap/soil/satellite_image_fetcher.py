# # # You need to pip install sentinelhub
# # # pip install sentinelhub

# # from sentinelhub import SHConfig, MimeType, CRS, BBox, SentinelHubRequest, DataCollection, bbox_to_dimensions

# # INSTANCE_ID = 'c675c71a-a3e2-461b-829b-28281bec0b85'  # Copied from your SentinelHub dashboard
# # CLIENT_ID = '82c6ea8b-525e-415a-8ffc-6a2df72dc7b1'
# # CLIENT_SECRET = '4tQ5X8LmCcqbwT9BZzJ6vzIeu4iWV9Fv'

# # config = SHConfig()
# # config.instance_id = INSTANCE_ID
# # config.sh_client_id = CLIENT_ID
# # config.sh_client_secret = CLIENT_SECRET

# # # ---- STEP 2: Choose a grid cell ----
# # # Jaipur center, grid of ~500m x 500m
# # bbox = BBox(bbox=[75.785, 26.910, 75.790, 26.915], crs=CRS.WGS84)  
# # size = bbox_to_dimensions(bbox, resolution=10)  # 10m per pixel (about 50x50 px)

# # # ---- STEP 3: Sentinel-2 L1C RGB image ----
# # request = SentinelHubRequest(
# #     data_folder='.',
# #     evalscript="""
# #     // Simple true color RGB
# #     function setup() {return {input: ["B04", "B03", "B02"], output: {bands: 3}};}
# #     function evaluatePixel(sample) {return [sample.B04, sample.B03, sample.B02];}
# #     """,
# #     input_data=[SentinelHubRequest.input_data(DataCollection.SENTINEL2_L1C)],
# #     responses=[SentinelHubRequest.output_response('default', MimeType.PNG)],
# #     bbox=bbox,
# #     size=size,
# #     config=config
# # )

# # img = request.get_data(save_data=True)
# # print("Image fetched and saved to current directory.")

# from sentinelhub import SHConfig, MimeType, CRS, BBox, SentinelHubRequest , DataCollection

# INSTANCE_ID = 'c675c71a-a3e2-461b-829b-28281bec0b85'
# CLIENT_ID = '82c6ea8b-525e-415a-8ffc-6a2df72dc7b1'
# CLIENT_SECRET = '4tQ5X8LmCcqbwT9BZzJ6vzIeu4iWV9Fv'

# config = SHConfig()
# config.instance_id = INSTANCE_ID
# config.sh_client_id = CLIENT_ID
# config.sh_client_secret = CLIENT_SECRET

# # Jaipur center, ~500m x 500m area
# bbox = BBox(bbox=[73.678, 24.576, 73.683, 24.581], crs=CRS.WGS84)

# size = (2448, 2448)  # Set image size to match YOLO training data

# request = SentinelHubRequest(
#     data_folder='.',
#     evalscript="""
#     function setup() {return {input: ["B04", "B03", "B02"], output: {bands: 3}};}
#     function evaluatePixel(sample) {return [sample.B04, sample.B03, sample.B02];}
#     """,
#     input_data=[SentinelHubRequest.input_data(DataCollection.SENTINEL2_L1C)],
#     responses=[SentinelHubRequest.output_response('default', MimeType.PNG)],
#     bbox=bbox,
#     size=size,
#     config=config
# )

# img = request.get_data(save_data=True)
# print("Image fetched and saved to current directory.")

# import os
# import csv
# from sentinelhub import SHConfig, MimeType, CRS, BBox, SentinelHubRequest, DataCollection, bbox_to_dimensions

# # ==== SentinelHub Credentials ====
# INSTANCE_ID = 'c675c71a-a3e2-461b-829b-28281bec0b85'
# CLIENT_ID = '82c6ea8b-525e-415a-8ffc-6a2df72dc7b1'
# CLIENT_SECRET = '4tQ5X8LmCcqbwT9BZzJ6vzIeu4iWV9Fv'

# config = SHConfig()
# config.instance_id = INSTANCE_ID
# config.sh_client_id = CLIENT_ID
# config.sh_client_secret = CLIENT_SECRET

# # ==== Input: CSV of grid cells ====
# GRID_CSV = "rajasthan_grid_cells.csv"  # Change path if needed

# # ==== Output Folder ====
# OUT_DIR = "sat_images"
# os.makedirs(OUT_DIR, exist_ok=True)

# # ==== SentinelHub Evalscript (RGB) ====
# EVALSCRIPT = """
# //VERSION=3
# function setup() {
#   return {
#     input: ["B04", "B03", "B02"],
#     output: { bands: 3 }
#   };
# }
# function evaluatePixel(sample) {
#   return [sample.B04, sample.B03, sample.B02];
# }
# """
# def fetch_sat_image(min_lng, min_lat, max_lng, max_lat, out_path):
#     bbox = BBox(bbox=[min_lng, min_lat, max_lng, max_lat], crs=CRS.WGS84)
#     size = bbox_to_dimensions(bbox, resolution=10)  # 10 meters per pixel (high-res)

#     request = SentinelHubRequest(
#         evalscript=EVALSCRIPT,
#         input_data=[
#             SentinelHubRequest.input_data(
#                 data_collection=DataCollection.SENTINEL2_L1C,
#                 time_interval=('2023-01-01', '2023-12-31'),
#             )
#         ],
#         responses=[SentinelHubRequest.output_response('default', MimeType.PNG)],
#         bbox=bbox,
#         size=size,
#         config=config,
#         data_folder=OUT_DIR   # <--- ADD THIS LINE!
#     )
#     data = request.get_data(save_data=True)
#     # Data is a list, [image] (numpy array), but request.save_data=True saves to OUT_DIR
#     saved = request.get_filename_list()[0]
#     os.rename(saved, out_path)
#     print(f"Downloaded: {out_path}")

# def fetch_sat_image(min_lng, min_lat, max_lng, max_lat, out_path):
#     bbox = BBox(bbox=[min_lng, min_lat, max_lng, max_lat], crs=CRS.WGS84)
#     size = bbox_to_dimensions(bbox, resolution=10)  # 10 meters per pixel (high-res)

#     request = SentinelHubRequest(
#         evalscript=EVALSCRIPT,
#         input_data=[
#             SentinelHubRequest.input_data(
#                 data_collection=DataCollection.SENTINEL2_L1C,
#                 time_interval=('2023-01-01', '2023-12-31'),
#             )
#         ],
#         responses=[SentinelHubRequest.output_response('default', MimeType.PNG)],
#         bbox=bbox,
#         size=size,
#         config=config,
#         data_folder=OUT_DIR   # <--- THIS IS GOOD
#     )
#     data = request.get_data(save_data=True)
#     # THIS IS THE FIX: get the correct full path
#     saved_rel = request.get_filename_list()[0]
#     saved = os.path.join(OUT_DIR, saved_rel)
#     os.rename(saved, out_path)
#     # Optionally: remove empty temp folder
#     temp_folder = os.path.dirname(saved)
#     if os.path.exists(temp_folder) and not os.listdir(temp_folder):
#         os.rmdir(temp_folder)
#     print(f"Downloaded: {out_path}")


# # ==== Main: Download images for all grid cells ====
# with open(GRID_CSV, newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         min_lng = float(row["min_lng"])
#         min_lat = float(row["min_lat"])
#         max_lng = float(row["max_lng"])
#         max_lat = float(row["max_lat"])
#         # Use grid center for filename
#         center_lat = (min_lat + max_lat) / 2
#         center_lng = (min_lng + max_lng) / 2
#         out_path = os.path.join(OUT_DIR, f"grid_{center_lat:.5f}_{center_lng:.5f}.png")
#         # Avoid redownload
#         if os.path.exists(out_path):
#             print(f"Already exists: {out_path}")
#             continue
#         try:
#             fetch_sat_image(min_lng, min_lat, max_lng, max_lat, out_path)
#         except Exception as e:
#             print(f"Error for bbox {min_lng},{min_lat},{max_lng},{max_lat}: {e}")

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
    bbox = BBox(bbox=[min_lng, min_lat, max_lng, max_lat], crs=CRS.WGS84)
    size = bbox_to_dimensions(bbox, resolution=10)  # 10 meters per pixel

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
    data = request.get_data(save_data=True)
    saved_rel = request.get_filename_list()[0]
    saved = os.path.join(OUT_DIR, saved_rel)
    os.rename(saved, out_path)
    temp_folder = os.path.dirname(saved)
    if os.path.exists(temp_folder) and not os.listdir(temp_folder):
        os.rmdir(temp_folder)
    print(f"Downloaded: {out_path}")

# ==== Main: Download images for all grid cells ====
with open(GRID_CSV, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        min_lng = float(row["min_lng"])
        min_lat = float(row["min_lat"])
        max_lng = float(row["max_lng"])
        max_lat = float(row["max_lat"])
        center_lat = (min_lat + max_lat) / 2
        center_lng = (min_lng + max_lng) / 2
        out_path = os.path.join(OUT_DIR, f"grid_{center_lat:.5f}_{center_lng:.5f}.png")
        if os.path.exists(out_path):
            print(f"Already exists: {out_path}")
            continue
        try:
            fetch_sat_image(min_lng, min_lat, max_lng, max_lat, out_path)
        except Exception as e:
            print(f"Error for bbox {min_lng},{min_lat},{max_lng},{max_lat}: {e}")


