from rest_framework.views import APIView
from rest_framework.response import Response
from PIL import Image
from collections import Counter
import csv
import os

# Set your soil image paths and legend mappings here

# Load climate data once at startup
CLIMATE_DATA = {}
climate_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/rajasthan_city_climate_split.csv"
if os.path.exists(climate_csv_path):
    with open(climate_csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            city = row["City"].strip().lower()
            CLIMATE_DATA[city] = row

# --- Forest/Population Data ---

FOREST_POP_DATA = {}
forest_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/rajasthan_district_forest_stats.csv"
if os.path.exists(forest_csv_path):
    with open(forest_csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Use lower-case and strip for matching
            district = row["Name of District"].strip().lower()
            FOREST_POP_DATA[district] = row


# --- River Data ---
RIVER_DATA = {}
river_csv_path = (
    "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/rajasthan_river_data.csv"
)
if os.path.exists(river_csv_path):
    with open(river_csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            district = row["District"].strip().lower()
            entry = {
                "Name of River": row["Name of River"],
                "Area in Ha.": row["Area in Ha."],
            }
            if district not in RIVER_DATA:
                RIVER_DATA[district] = []
            RIVER_DATA[district].append(entry)

# Estimated Area Data
ESTIMATED_AREA_DATA = {}
est_area_csv_path = (
    "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/rajasthan_ravine_area.csv"
)
if os.path.exists(est_area_csv_path):
    with open(est_area_csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            district = row["District"].strip().lower()
            ESTIMATED_AREA_DATA[district] = row["Estimated Area in Ha."]

# --- Rainfall Data ---
RAINFALL_DATA = {}
rainfall_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/rajasthan_rainfall_distribution_june2025.csv"
if os.path.exists(rainfall_csv_path):
    with open(rainfall_csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Key on lowercased district for consistency
            district = row["District"].strip().lower()
            print(f"Loading rainfall for district: '{district}'")  # DEBUG
            RAINFALL_DATA[district] = row
    print("Loaded RAINFALL_DATA keys:", list(RAINFALL_DATA.keys()))  # DEBUG
else:
    print("Rainfall CSV path not found:", rainfall_csv_path)  # DEBUG

# --- Well Water Depth Data ---
WELL_DEPTH_DATA = {}
well_depth_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/rajasthan_groundwater_wells.csv"
if os.path.exists(well_depth_csv_path):
    with open(well_depth_csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Key on lowercased, stripped District Name for consistency
            district = row["District Name"].strip().lower()
            WELL_DEPTH_DATA[district] = row

# --- Water Usage Data ---
WATER_USAGE_DATA = {}
water_usage_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/water_usage_data.csv"  # Update the path if you move the file
if os.path.exists(water_usage_csv_path):
    with open(water_usage_csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Key on lowercased district name for lookup consistency
            district = row["District"].strip().lower()
            WATER_USAGE_DATA[district] = row

# --- Soil Analysis Data (Multiple Rows Per District) ---
SOIL_ANALYSIS_DATA = {}
soil_analysis_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/soil_analysis_data.csv"  # Update path if needed
if os.path.exists(soil_analysis_csv_path):
    with open(soil_analysis_csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            district = row["District"].strip().lower()
            if district not in SOIL_ANALYSIS_DATA:
                SOIL_ANALYSIS_DATA[district] = []
            SOIL_ANALYSIS_DATA[district].append(row)

# --- Crop Production Data ---
CROP_PRODUCTION_DATA = {}
crop_production_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/crop_production_data.csv"  # Update if needed

if os.path.exists(crop_production_csv_path):
    with open(crop_production_csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            district = row["District"].strip().lower()
            if district not in CROP_PRODUCTION_DATA:
                CROP_PRODUCTION_DATA[district] = []
            CROP_PRODUCTION_DATA[district].append(row)

# --- Crop Price Data ---
CROP_PRICE_DATA = {}
crop_price_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/crop_price_data.csv"  # Update path if needed


if os.path.exists(crop_price_csv_path):
    with open(crop_price_csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Use 'District' or city-level key as appropriate
            district = row.get("District", "").strip().lower()
            if not district:
                continue
            if district not in CROP_PRICE_DATA:
                CROP_PRICE_DATA[district] = []
            CROP_PRICE_DATA[district].append(row)


SOIL_IMAGES = {
    "copper": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Cu.jpg",
        "legend": {
            (50, 150, 0, 255): "Sufficient",  # Green
            (197, 76, 37, 255): "Deficient",  # Red
        },
    },
    "soil_salinity": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_EC.jpg",
        "legend": {
            (210, 219, 50, 255): "Mild salinity",  # Yellow
            (208, 207, 82, 255): "Low Salinity",  # Brownish
            (141, 182, 0, 255): "High salinity",  # Green
        },
    },
    "iron": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Fe.jpg",
        "legend": {
            (250, 50, 50, 255): "Deficient",  # Red
            (50, 149, 0, 255): "Sufficient",  # Green
        },
    },
    "Mangnese": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Mn.jpg",
        "legend": {
            (50, 150, 0, 255): "Sufficient",  # Green
            (118, 116, 17, 255): "Deficient",  # Red
        },
    },
    "Organic_Carbon": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_OC.jpg",
        "legend": {
            (250, 50, 50, 255): "Low",  # Red
            (50, 150, 0, 255): "High",  # Green
            (249, 249, 50, 255): "Medium",  # Yellow
        },
    },
    "Ph": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_pH.jpg",
        "legend": {
            (10, 98, 9, 255): "Normal",  # Green
            (255, 115, 222, 255): "Slightly Alkaline",  # Pink
            (192, 154, 107, 255): "Moderately Alkaline",  # Brown
        },
    },
    "Phosphorus": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Fe.jpg",
        "legend": {
            (50, 150, 0, 255): "High",  # Green
            (249, 250, 50, 255): "Medium",  # Yellow
        },
    },
    "Pottasium": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_P.jpg",
        "legend": {
            (50, 150, 0, 255): "High",  # Green
            (249, 250, 50, 255): "Medium",  # Yellow
            (250, 50, 50, 255): "Low",  # Red
        },
    },
    "Sulphur": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_S.jpg",
        "legend": {
            (50, 150, 0, 255): "Sufficient",  # Green
            (197, 76, 37, 255): "Deficient",  # Red
        },
    },
    "Zinc": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Zn.jpg",
        "legend": {
            (50, 150, 0, 255): "Sufficient",  # Green
            (197, 76, 37, 255): "Deficient",  # Red
        },
    },
}

# The geo bounds your images represent
MIN_LAT, MAX_LAT = 23.3, 30.9  # South, North (adjust as per your crop)
MIN_LNG, MAX_LNG = 69.3, 78.5  # West, East (adjust as per your crop)


def latlng_to_pixel(lat, lng, img_width, img_height):
    x = int(((lng - MIN_LNG) / (MAX_LNG - MIN_LNG)) * img_width)
    y = int(((MAX_LAT - lat) / (MAX_LAT - MIN_LAT)) * img_height)
    return x, y


def closest_color(rgb, legend):
    # Use only first 3 channels for matching (ignore alpha)
    rgb = tuple(rgb[:3])
    distances = [
        (sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, lrgb[:3])), name)
        for lrgb, name in legend.items()
    ]
    return min(distances, key=lambda x: x[0])[1]


def get_window_mode(img, x, y, legend, window=2):
    """Returns the mode class in a (2*window+1)x(2*window+1) square around (x, y)."""
    values = []
    for dx in range(-window, window + 1):
        for dy in range(-window, window + 1):
            nx, ny = x + dx, y + dy
            if 0 <= nx < img.width and 0 <= ny < img.height:
                try:
                    px_rgb = img.getpixel((nx, ny))[:3]
                    values.append(closest_color(px_rgb, legend))
                except Exception:
                    pass
    if values:
        return Counter(values).most_common(1)[0][0]
    else:
        return "Unknown"


# class SoilPropertiesView(APIView):
#     def post(self, request, format=None):
#         lat = request.data.get("lat")
#         lng = request.data.get("lng")
#         if lat is None or lng is None:
#             return Response({"error": "Missing lat/lng"}, status=400)

#         result = {}
#         for key, val in SOIL_IMAGES.items():
#             try:
#                 img = Image.open(val["path"])
#                 width, height = img.size
#                 x, y = latlng_to_pixel(float(lat), float(lng), width, height)
#                 value = get_window_mode(img, x, y, val["legend"], window=2)  # 5x5 window
#                 result[key] = value
#             except Exception as e:
#                 result[key] = f"Error: {str(e)}"
#         return Response(result)


class SoilPropertiesView(APIView):
    def post(self, request, format=None):
        lat = request.data.get("lat")
        lng = request.data.get("lng")
        city = request.data.get("city", "").strip().lower()

        print(f"Received POST: lat={lat}, lng={lng}, city='{city}'")  # DEBUG

        if lat is None or lng is None:
            return Response({"error": "Missing lat/lng"}, status=400)

        # Soil data
        result = {}
        for key, val in SOIL_IMAGES.items():
            try:
                img = Image.open(val["path"])
                width, height = img.size
                x, y = latlng_to_pixel(float(lat), float(lng), width, height)
                value = get_window_mode(img, x, y, val["legend"], window=2)
                result[key] = value
            except Exception as e:
                result[key] = f"Error: {str(e)}"

        # Climate data
        climate_data = CLIMATE_DATA.get(city, {})
        forest_data = FOREST_POP_DATA.get(city, {})
        river_data = RIVER_DATA.get(city, [])
        estimated_area = ESTIMATED_AREA_DATA.get(city, "Not available")
        well_depth_data = WELL_DEPTH_DATA.get(city, {})
        water_usage_data = WATER_USAGE_DATA.get(city, {})
        rainfall_data = RAINFALL_DATA.get(city, {})
        soil_analysis_rows = SOIL_ANALYSIS_DATA.get(city, [])  # Now returns a list!
        crop_production_rows = CROP_PRODUCTION_DATA.get(city, [])
        crop_price_rows = CROP_PRICE_DATA.get(city, [])

        # Rainfall data with debug prints
        print(f"Trying to find water usage  for: '{city}'")
        print("All water usage districts:", list(WATER_USAGE_DATA.keys()))  # DEBUG
        print("water usage  data found:", water_usage_data)  # DEBUG

        return Response(
            {
                "soil_data": result,
                "climate_data": climate_data,
                "forest_population_data": forest_data,
                "river_data": river_data,
                "estimated_area_data": estimated_area,
                "rainfall_data": rainfall_data,
                "well_depth_data": well_depth_data,
                "water_usage_data": water_usage_data,
                "soil_analysis_data": soil_analysis_rows,
                "crop_production_data": crop_production_rows,
                "crop_price_data": crop_price_rows,  # <--- NEW!
            }
        )
