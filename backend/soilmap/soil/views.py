from rest_framework.views import APIView
from rest_framework.response import Response
from PIL import Image
from collections import Counter
import csv
import os
# Set your soil image paths and legend mappings here

# Load climate data once at startup
CLIMATE_DATA = {}
climate_csv_path = '/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/rajasthan_city_climate_split.csv'
if os.path.exists(climate_csv_path):
    with open(climate_csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            city = row['City'].strip().lower()
            CLIMATE_DATA[city] = row
            
# --- Forest/Population Data ---

FOREST_POP_DATA = {}
forest_csv_path = '/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/rajasthan_district_forest_stats.csv'
if os.path.exists(forest_csv_path):
    with open(forest_csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Use lower-case and strip for matching
            district = row['Name of District'].strip().lower()
            FOREST_POP_DATA[district] = row


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
            (210, 219, 50, 255): "Mild salinity",    # Yellow
            (208, 207, 82, 255): "Low Salinity",     # Brownish
            (141, 182, 0, 255): "High salinity",     # Green
        },
    },
    "iron": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Fe.jpg",
        "legend": {
            (250, 50, 50, 255): "Deficient",     # Red
            (50, 149, 0, 255): "Sufficient",     # Green
        },
    },
    "Mangnese": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Mn.jpg",
        "legend": {
            (50, 150, 0, 255): "Sufficient",     # Green
            (118, 116, 17, 255): "Deficient",    # Red
        },
    },
    "Organic_Carbon": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_OC.jpg",
        "legend": {
            (250, 50, 50, 255): "Low",           # Red
            (50, 150, 0, 255): "High",           # Green
            (249, 249, 50, 255): "Medium",       # Yellow
        },
    },
    "Ph": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_pH.jpg",
        "legend": {
            (10,98,9,255): "Normal",                 # Green
            (255,115,222,255): "Slightly Alkaline",  # Pink
            (192,154,107,255): "Moderately Alkaline",# Brown
        },
    },
    "Phosphorus": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Fe.jpg",
        "legend": {
            (50,150,0,255): "High",              # Green
            (249,250,50,255): "Medium",          # Yellow
        },
    },
    "Pottasium": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_P.jpg",
        "legend": {
            (50,150,0,255): "High",              # Green
            (249,250,50,255): "Medium",          # Yellow
            (250, 50, 50, 255): "Low",           # Red
        },
    },
    "Sulphur": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_S.jpg",
        "legend": {
            (50, 150, 0, 255): "Sufficient",     # Green
            (197, 76, 37, 255): "Deficient",     # Red
        },
    },
    "Zinc": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Zn.jpg",
        "legend": {
            (50, 150, 0, 255): "Sufficient",     # Green
            (197, 76, 37, 255): "Deficient",     # Red
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
    for dx in range(-window, window+1):
        for dy in range(-window, window+1):
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

        # Forest/Population data
        forest_data = FOREST_POP_DATA.get(city, {})

        return Response({
            "soil_data": result,
            "climate_data": climate_data,
            "forest_population_data": forest_data,
        })
