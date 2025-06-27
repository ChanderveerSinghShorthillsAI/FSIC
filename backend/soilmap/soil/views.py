# fetching data from csv code 

# from rest_framework.views import APIView # this is used to create API views
# from rest_framework.response import Response # this is used to send responses back to the client
# from PIL import Image # Python Imaging Library for image processing
# from collections import Counter # Counter is used to count occurrences of elements
# import csv
# import os

# # Set your soil image paths and legend mappings here
# # Load climate data once at startup
# CLIMATE_DATA = {} # Dictionary to hold climate data for each city
# climate_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/rajasthan_city_climate_split.csv" # Update the path if you move the file
# if os.path.exists(climate_csv_path): # Check if the file exists
#     with open(climate_csv_path, encoding="utf-8") as f: # Open the file with UTF-8 encoding because it may contain non-ASCII characters
#         reader = csv.DictReader(f) # Read the CSV file as a dictionary
#         for row in reader: # Iterate through each row in the CSV
#             city = row["City"].strip().lower() # Use lower-case and strip for matching
#             CLIMATE_DATA[city] = row # Store the row data in the dictionary with city as the key

# # --- Forest/Population Data ---

# FOREST_POP_DATA = {}
# forest_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/rajasthan_district_forest_stats.csv"
# if os.path.exists(forest_csv_path):
#     with open(forest_csv_path, encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             # Use lower-case and strip for matching
#             district = row["Name of District"].strip().lower()
#             FOREST_POP_DATA[district] = row


# # --- River Data ---
# RIVER_DATA = {}
# river_csv_path = (
#     "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/rajasthan_river_data.csv"
# )
# if os.path.exists(river_csv_path):
#     with open(river_csv_path, encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             district = row["District"].strip().lower()
#             entry = {
#                 "Name of River": row["Name of River"],
#                 "Area in Ha.": row["Area in Ha."],
#             }
#             if district not in RIVER_DATA:
#                 RIVER_DATA[district] = []
#             RIVER_DATA[district].append(entry)

# # Estimated Area Data
# ESTIMATED_AREA_DATA = {}
# est_area_csv_path = (
#     "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/rajasthan_ravine_area.csv"
# )
# if os.path.exists(est_area_csv_path):
#     with open(est_area_csv_path, encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             district = row["District"].strip().lower()
#             ESTIMATED_AREA_DATA[district] = row["Estimated Area in Ha."]

# # --- Rainfall Data ---
# RAINFALL_DATA = {}
# rainfall_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/rajasthan_rainfall_distribution_june2025.csv"
# if os.path.exists(rainfall_csv_path):
#     with open(rainfall_csv_path, encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             # Key on lowercased district for consistency
#             district = row["District"].strip().lower()
#             print(f"Loading rainfall for district: '{district}'")  # DEBUG
#             RAINFALL_DATA[district] = row
#     print("Loaded RAINFALL_DATA keys:", list(RAINFALL_DATA.keys()))  # DEBUG
# else:
#     print("Rainfall CSV path not found:", rainfall_csv_path)  # DEBUG

# # --- Well Water Depth Data ---
# WELL_DEPTH_DATA = {}
# well_depth_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/rajasthan_groundwater_wells.csv"
# if os.path.exists(well_depth_csv_path):
#     with open(well_depth_csv_path, encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             # Key on lowercased, stripped District Name for consistency
#             district = row["District Name"].strip().lower()
#             WELL_DEPTH_DATA[district] = row

# # --- Water Usage Data ---
# WATER_USAGE_DATA = {}
# water_usage_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/water_usage_data.csv"  # Update the path if you move the file
# if os.path.exists(water_usage_csv_path):
#     with open(water_usage_csv_path, encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             # Key on lowercased district name for lookup consistency
#             district = row["District"].strip().lower()
#             WATER_USAGE_DATA[district] = row

# # --- Soil Analysis Data (Multiple Rows Per District) ---
# SOIL_ANALYSIS_DATA = {}
# soil_analysis_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/soil_analysis_data.csv"  # Update path if needed
# if os.path.exists(soil_analysis_csv_path):
#     with open(soil_analysis_csv_path, encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             district = row["District"].strip().lower()
#             if district not in SOIL_ANALYSIS_DATA:
#                 SOIL_ANALYSIS_DATA[district] = []
#             SOIL_ANALYSIS_DATA[district].append(row)

# # --- Crop Production Data ---
# CROP_PRODUCTION_DATA = {}
# crop_production_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/crop_production_data.csv"  # Update if needed

# if os.path.exists(crop_production_csv_path):
#     with open(crop_production_csv_path, encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             district = row["District"].strip().lower()
#             if district not in CROP_PRODUCTION_DATA:
#                 CROP_PRODUCTION_DATA[district] = []
#             CROP_PRODUCTION_DATA[district].append(row)

# # --- Crop Price Data ---
# CROP_PRICE_DATA = {}
# crop_price_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/crop_price_data.csv"  # Update path if needed


# if os.path.exists(crop_price_csv_path):
#     with open(crop_price_csv_path, encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             # Use 'District' or city-level key as appropriate
#             district = row.get("District", "").strip().lower()
#             if not district:
#                 continue
#             if district not in CROP_PRICE_DATA:
#                 CROP_PRICE_DATA[district] = []
#             CROP_PRICE_DATA[district].append(row)


# SOIL_IMAGES = { # Dictionary to hold soil image paths and legends , # keys are the soil properties and values are dictionaries with image path and legend
#     "copper": {
#         "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Cu.jpg",
#         "legend": {
#             (50, 150, 0, 255): "Sufficient",  # Green 
#             (197, 76, 37, 255): "Deficient",  # Red
#         },
#     },
#     "soil_salinity": {
#         "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_EC.jpg",
#         "legend": {
#             (210, 219, 50, 255): "Mild salinity",  # Yellow
#             (208, 207, 82, 255): "Low Salinity",  # Brownish
#             (141, 182, 0, 255): "High salinity",  # Green
#         },
#     },
#     "iron": {
#         "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Fe.jpg",
#         "legend": {
#             (250, 50, 50, 255): "Deficient",  # Red
#             (50, 149, 0, 255): "Sufficient",  # Green
#         },
#     },
#     "Mangnese": {
#         "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Mn.jpg",
#         "legend": {
#             (50, 150, 0, 255): "Sufficient",  # Green
#             (118, 116, 17, 255): "Deficient",  # Red
#         },
#     },
#     "Organic_Carbon": {
#         "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_OC.jpg",
#         "legend": {
#             (250, 50, 50, 255): "Low",  # Red
#             (50, 150, 0, 255): "High",  # Green
#             (249, 249, 50, 255): "Medium",  # Yellow
#         },
#     },
#     "Ph": {
#         "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_pH.jpg",
#         "legend": {
#             (10, 98, 9, 255): "Normal",  # Green
#             (255, 115, 222, 255): "Slightly Alkaline",  # Pink
#             (192, 154, 107, 255): "Moderately Alkaline",  # Brown
#         },
#     },
#     "Phosphorus": {
#         "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_P.jpg",
#         "legend": {
#             (50, 150, 0, 255): "High",  # Green
#             (249, 250, 50, 255): "Medium",  # Yellow
#         },
#     },
#     "Pottasium": {
#         "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_K.jpg",
#         "legend": {
#             (50, 150, 0, 255): "High",  # Green
#             (249, 250, 50, 255): "Medium",  # Yellow
#             (250, 50, 50, 255): "Low",  # Red
#         },
#     },
#     "Sulphur": {
#         "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_S.jpg",
#         "legend": {
#             (50, 150, 0, 255): "Sufficient",  # Green
#             (197, 76, 37, 255): "Deficient",  # Red
#         },
#     },
#     "Zinc": {
#         "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Zn.jpg",
#         "legend": {
#             (50, 150, 0, 255): "Sufficient",  # Green
#             (197, 76, 37, 255): "Deficient",  # Red
#         },
#     },
# }

# # The geo bounds your images represent
# MIN_LAT, MAX_LAT = 23.3, 30.9  # South, North 
# MIN_LNG, MAX_LNG = 69.3, 78.5  # West, East 


# def latlng_to_pixel(lat, lng, img_width, img_height):
#     x = int(((lng - MIN_LNG) / (MAX_LNG - MIN_LNG)) * img_width) # Convert longitude to x pixel
#     y = int(((MAX_LAT - lat) / (MAX_LAT - MIN_LAT)) * img_height) # Convert latitude to y pixel
#     # Ensure x and y are within bounds
#     return x, y


# def closest_color(rgb, legend): # Find the closest color in the legend to the given RGB tuple
#     """Finds the closest color in the legend to the given RGB tuple."""
#     # Use only first 3 channels for matching (ignore alpha)
#     rgb = tuple(rgb[:3]) # Take only the first 3 channels (R, G, B)
#     # Calculate squared distances to avoid sqrt for performance
#     # legend is a dictionary with RGB tuples as keys and color names as values
#     distances = [ # List of tuples (distance, color name)
#         (sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, lrgb[:3])), name) # Calculate squared distance
#         for lrgb, name in legend.items() # Iterate over legend items to compare colors and names 
#     ]
#     return min(distances, key=lambda x: x[0])[1] # return the color name with property like sufficient with the smallest distance


# def get_window_mode(img, x, y, legend, window=2.135): # Get the most common color in a window around (x, y)
#     """Returns the mode class in a (2*window+1)x(2*window+1) square around (x, y)."""
#     values = [] # List to hold color values in the window
#     for dx in range(-window, window + 1): # Iterate over the x range of the window
#         for dy in range(-window, window + 1):# Iterate over the y range of the window
#             nx, ny = x + dx, y + dy # Calculate the new pixel coordinates
#             if 0 <= nx < img.width and 0 <= ny < img.height: # Check if the pixel is within bounds
#                 try: # Get the pixel color at (nx, ny)
#                     px_rgb = img.getpixel((nx, ny))[:3] # Get the RGB tuple (ignore alpha channel if present)
#                     values.append(closest_color(px_rgb, legend)) # Find the closest color property in the legend and append it to values
#                 except Exception:
#                     pass
#     if values: # If we have any values in the window, return the most common one
#         return Counter(values).most_common(1)[0][0] # Return the most common color name
#     else:
#         return "Unknown"





# class SoilPropertiesView(APIView): # This class handles the POST request to get soil properties based on latitude and longitude
#     """API endpoint to get soil properties based on latitude and longitude.
#     Expects POST data with 'lat' and 'lng' keys.
#     Returns a JSON response with soil properties and other related data.
#     """
#     def post(self, request, format=None):
#         lat = request.data.get("lat") # Get latitude from request data
#         lng = request.data.get("lng") # Get longitude from request data
#         city = request.data.get("city", "").strip().lower() # Get city from request data, default to empty string if not provided

#         print(f"Received POST: lat={lat}, lng={lng}, city='{city}'")  # DEBUG

#         if lat is None or lng is None:
#             return Response({"error": "Missing lat/lng"}, status=400)

#         # Soil data
#         result = {} # Dictionary to hold soil property results
#         for key, val in SOIL_IMAGES.items(): # Iterate over each soil property
#             try: # Try to open the image file for the soil property
#                 img = Image.open(val["path"]) # Open the image file
#                 width, height = img.size # Get the dimensions of the image
#                 x, y = latlng_to_pixel(float(lat), float(lng), width, height) # Convert lat/lng to pixel coordinates
#                 value = get_window_mode(img, x, y, val["legend"], window=2) # Get the most common color in a 5x5 window around the pixel
#                 result[key] = value # Store the result in the dictionary , the result is the most common color name for the soil property 
#             except Exception as e:
#                 result[key] = f"Error: {str(e)}"

#         # Climate data
#         climate_data = CLIMATE_DATA.get(city, {})
#         forest_data = FOREST_POP_DATA.get(city, {})
#         river_data = RIVER_DATA.get(city, [])
#         estimated_area = ESTIMATED_AREA_DATA.get(city, "Not available")
#         well_depth_data = WELL_DEPTH_DATA.get(city, {})
#         water_usage_data = WATER_USAGE_DATA.get(city, {})
#         rainfall_data = RAINFALL_DATA.get(city, {})
#         soil_analysis_rows = SOIL_ANALYSIS_DATA.get(city, [])  # Now returns a list!
#         crop_production_rows = CROP_PRODUCTION_DATA.get(city, [])
#         crop_price_rows = CROP_PRICE_DATA.get(city, [])

#         # Rainfall data with debug prints
#         print(f"Trying to find water usage  for: '{city}'")
#         print("All water usage districts:", list(WATER_USAGE_DATA.keys()))  # DEBUG
#         print("water usage  data found:", water_usage_data)  # DEBUG

#         return Response(
#             {
#                 "soil_data": result,
#                 "climate_data": climate_data,
#                 "forest_population_data": forest_data,
#                 "river_data": river_data,
#                 "estimated_area_data": estimated_area,
#                 "rainfall_data": rainfall_data,
#                 "well_depth_data": well_depth_data,
#                 "water_usage_data": water_usage_data,
#                 "soil_analysis_data": soil_analysis_rows,
#                 "crop_production_data": crop_production_rows,
#                 "crop_price_data": crop_price_rows,  # <--- NEW!
#             }
#         )



# # Load cultivability map at server startup
# CULTIVABILITY_MAP = {} # Dictionary to hold cultivability data
# # This map will hold the cultivability status for each grid cell
# # Key: "lat,lng" (rounded to 5 decimals), Value: 0 or 1 (not cultivable or cultivable)
# # Example: "27.08422,74.30923": 1
# # Load the grid results CSV file to populate the CULTIVABILITY_MAP
# grid_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/yolo_results/grid_results.csv"  # Change path!

# with open(grid_csv_path, newline='') as csvfile: # Open the CSV file containing grid results
#     reader = csv.DictReader(csvfile) # Read the CSV file as a dictionary
#     for row in reader: # # Iterate through each row in the CSV
#         index = row['index'] # Extract the index from the row
#         CULTIVABILITY_MAP[index] = int(row['cultivable']) # Store cultivability as int (0 or 1) in the map

   


# # New API endpoint
# class CultivableGridAPI(APIView):
#     def get(self, request):
#         # Returns {"27.08422,74.30923": 1, ...}
#         return Response(CULTIVABILITY_MAP) # Return the cultivability map   




#fetching data from databases code 

from rest_framework.views import APIView
from rest_framework.response import Response
from PIL import Image
from collections import Counter
from .models import (
    water_usage_data,
    soil_analysis_data,
    rajasthan_river_data,
    rajasthan_ravine_area,
    rajasthan_rainfall_distribution_june2025,
    rajasthan_groundwater_wells,
    rajasthan_district_forest_stat,
    rajasthan_city_climate_split,
    ForestAssessment2011_data_file_1,
    crop_production_data,
    crop_price_data,
    NoCIssuance,
    OffenceData,
    BlockMaster,
    ForestFireAlert,
    NurseryData,
    MasterProduce,
    ProduceAuction,
    ProjectShapefile,
    PlantationSite,
    ProjectMonthlyProgress,
    SpeciesCarbonSequestration,
    RainfallDataset,
    SoilMoistureDataset,
    GroundWaterDepth,
    LivestockData,
    DigitalElevationData,
    TemperatureData,
    HumanSettlementData,
    GrasslandWaterBodiesData,
    ForestFireData,
)

# Soil image paths and legend mappings
SOIL_IMAGES = {
    "copper": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Cu.jpg",
        "legend": {
            (50, 150, 0, 255): "Sufficient",
            (197, 76, 37, 255): "Deficient",
        },
    },
    "soil_salinity": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_EC.jpg",
        "legend": {
            (210, 219, 50, 255): "Mild salinity",
            (208, 207, 82, 255): "Low Salinity",
            (141, 182, 0, 255): "High salinity",
        },
    },
    "iron": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Fe.jpg",
        "legend": {
            (250, 50, 50, 255): "Deficient",
            (50, 149, 0, 255): "Sufficient",
        },
    },
    "Mangnese": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Mn.jpg",
        "legend": {
            (50, 150, 0, 255): "Sufficient",
            (118, 116, 17, 255): "Deficient",
        },
    },
    "Organic_Carbon": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_OC.jpg",
        "legend": {
            (250, 50, 50, 255): "Low",
            (50, 150, 0, 255): "High",
            (249, 249, 50, 255): "Medium",
        },
    },
    "Ph": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_pH.jpg",
        "legend": {
            (10, 98, 9, 255): "Normal",
            (255, 115, 222, 255): "Slightly Alkaline",
            (192, 154, 107, 255): "Moderately Alkaline",
        },
    },
    "Phosphorus": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_P.jpg",
        "legend": {
            (50, 150, 0, 255): "High",
            (249, 250, 50, 255): "Medium",
        },
    },
    "Pottasium": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_K.jpg",
        "legend": {
            (50, 150, 0, 255): "High",
            (249, 250, 50, 255): "Medium",
            (250, 50, 50, 255): "Low",
        },
    },
    "Sulphur": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_S.jpg",
        "legend": {
            (50, 150, 0, 255): "Sufficient",
            (197, 76, 37, 255): "Deficient",
        },
    },
    "Zinc": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Zn.jpg",
        "legend": {
            (50, 150, 0, 255): "Sufficient",
            (197, 76, 37, 255): "Deficient",
        },
    },
}

# Geo bounds for images
MIN_LAT, MAX_LAT = 23.3, 30.9  # South, North
MIN_LNG, MAX_LNG = 69.3, 78.5  # West, East

def latlng_to_pixel(lat, lng, img_width, img_height):
    x = int(((lng - MIN_LNG) / (MAX_LNG - MIN_LNG)) * img_width)
    y = int(((MAX_LAT - lat) / (MAX_LAT - MIN_LAT)) * img_height)
    return x, y

def closest_color(rgb, legend):
    rgb = tuple(rgb[:3])
    distances = [
        (sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, lrgb[:3])), name)
        for lrgb, name in legend.items()
    ]
    return min(distances, key=lambda x: x[0])[1]

def get_window_mode(img, x, y, legend, window=2):
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

class SoilPropertiesView(APIView):
    """API endpoint to get soil properties and related data based on latitude, longitude, and district.
    Expects POST data with 'lat', 'lng', and 'district' keys.
    Returns a JSON response with soil properties and other related data.
    """
    def post(self, request, format=None):
        lat = request.data.get("lat")
        lng = request.data.get("lng")
        district = request.data.get("city", "").strip().lower()

        print(f"Received POST: lat={lat}, lng={lng}, district='{district}'")  # DEBUG

        if lat is None or lng is None:
            return Response({"error": "Missing lat/lng"}, status=400)
        if not district:
            return Response({"error": "District is required"}, status=400)

        # Soil data from images
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

        # Database queries
        # Climate data
        climate_data = rajasthan_city_climate_split.objects.filter(City__iexact=district).values().first() or {}

        # Forest and population data
        forest_data = rajasthan_district_forest_stat.objects.filter(District__iexact=district).values().first() or {}

        # River data
        river_data = list(rajasthan_river_data.objects.filter(district__iexact=district).values(
            "river_name", "area_in_ha"
        ))

        # Estimated ravine area
        estimated_area = rajasthan_ravine_area.objects.filter(district__iexact=district).values("estimated_area_ha").first()
        estimated_area = estimated_area["estimated_area_ha"] if estimated_area else "Not available"

        # Rainfall data
        rainfall_data = rajasthan_rainfall_distribution_june2025.objects.filter(district__iexact=district).values().first() or {}

        # Well depth data
        well_depth_data = rajasthan_groundwater_wells.objects.filter(district_name__iexact=district).values().first() or {}

        # Water usage data
        # water_usage_data = list(water_usage_data.objects.filter(district__iexact=district).values(
        #     "crop", "irrigation_method", "water_consumption", "water_availability"
        # ))

        # Soil analysis data
        soil_analysis_rows = list(soil_analysis_data.objects.filter(district__iexact=district).values(
            "soil_type", "ph_level", "organic_matter", "nitrogen_content", "phosphorus_content", "potassium_content"
        ))

        # Crop production data
        crop_production_rows = list(crop_production_data.objects.filter(District__iexact=district).values(
            "Crop", "Season", "area_hectares", "yield_quintals", "production_metric_tons"
        ))

        # Crop price data
        crop_price_rows = list(crop_price_data.objects.filter(District__iexact=district).values(
            "Crop", "Market", "Date", "price_inr_per_quintal"
        ))

        # Additional database queries for new models
        forest_assessment_data = list(ForestAssessment2011_data_file_1.objects.filter(district__iexact=district).values(
            "geographical_area", "very_dense_forest", "mod_dense_forest", "open_forest",
            "total_forest", "percent_of_ga", "change", "scrub"
        ))

        noc_issuance_data = list(NoCIssuance.objects.filter(district__iexact=district).values(
            "circle", "division", "request_no", "process_status", "proposed_area",
            "distance_water_source", "distance_forest_boundary", "distance_protected_area",
            "number_trees", "forest_density", "species_details"
        ))

        offence_data = list(OffenceData.objects.filter(district__iexact=district).values(
            "range", "circle", "division", "offence_type", "fir_date", "items_seized",
            "compounded_amount", "rule_applied"
        ))

        block_master_data = list(BlockMaster.objects.filter(district__iexact=district).values(
            "range", "circle", "division", "block_name", "legal_status", "notify_area"
        ))

        forest_fire_alert_data = list(ForestFireAlert.objects.filter(district__iexact=district).values(
            "range", "circle", "division", "lat_long", "date_time", "status",
            "manpower_req", "organization_req", "affected_forest_area", "wildlife_loss"
        ))

        nursery_data = list(NurseryData.objects.filter(district__iexact=district).values(
            "circle", "division", "nursery_name", "plant_name", "plant_age",
            "plant_height", "plant_price", "total_stock", "online_purchase"
        ))

        master_produce_data = list(MasterProduce.objects.filter(district__iexact=district).values(
            "produce_type", "base_produce_type", "price"
        ))

        produce_auction_data = list(ProduceAuction.objects.filter(district__iexact=district).values(
            "circle", "division", "range", "depot", "int_no", "product_type",
            "product_unit", "product_quantity", "bidding_amount"
        ))

        project_shapefile_data = list(ProjectShapefile.objects.filter(district__iexact=district).values(
            "circle", "division", "range", "block", "lat_long"
        ))

        plantation_site_data = list(PlantationSite.objects.filter(district__iexact=district).values(
            "circle", "division", "range", "village", "scheme", "plantation_year"
        ))

        project_monthly_progress_data = list(ProjectMonthlyProgress.objects.filter(district__iexact=district).values(
            "circle", "division", "range", "site", "scheme", "physical_target",
            "physical_achieved", "budget_utilization", "man_days_generated"
        ))

        species_carbon_data = list(SpeciesCarbonSequestration.objects.all().values(
            "name", "scientific_name", "volume_equation_type", "volume_equation_coefficients",
            "wood_density", "biomass_expansion_factor", "carbon_fraction",
            "co2_conversion_factor", "diameter_growth", "root_shoot_ratio",
            "stem_leaf_biomass_factor"
        ))

        rainfall_dataset_data = list(RainfallDataset.objects.filter(district__iexact=district).values(
            "description", "source", "start_date", "end_date", "spatial_resolution"
        ))

        soil_moisture_data = list(SoilMoistureDataset.objects.filter(district__iexact=district).values(
            "description", "source", "start_date", "end_date", "spatial_resolution"
        ))

        groundwater_depth_data = list(GroundWaterDepth.objects.filter(district__iexact=district).values(
            "lat", "long", "year", "pre_monsoon", "post_monsoon"
        ))

        livestock_data = list(LivestockData.objects.filter(district__iexact=district).values(
            "livestock_type", "livestock_count"
        ))

        digital_elevation_data = list(DigitalElevationData.objects.filter(district__iexact=district).values(
            "description", "source", "year", "spatial_resolution"
        ))

        temperature_data = list(TemperatureData.objects.filter(district__iexact=district).values(
            "description", "source", "start_year", "end_year", "spatial_resolution"
        ))

        human_settlement_data = list(HumanSettlementData.objects.filter(district__iexact=district).values(
            "description", "source", "start_year", "spatial_resolution"
        ))

        grassland_water_data = list(GrasslandWaterBodiesData.objects.filter(district__iexact=district).values(
            "description", "source", "spatial_resolution"
        ))

        forest_fire_data = list(ForestFireData.objects.filter(district__iexact=district).values(
            "state", "circle", "lat_long", "date_time", "forest_block"
        ))

        return Response({
            "soil_data": result,
            "climate_data": climate_data,
            "forest_population_data": forest_data,
            "river_data": river_data,
            "estimated_area_data": estimated_area,
            "rainfall_data": rainfall_data,
            "well_depth_data": well_depth_data,
            # "water_usage_data": water_usage_data,
            "soil_analysis_data": soil_analysis_rows,
            "crop_production_data": crop_production_rows,
            "crop_price_data": crop_price_rows,
            "forest_assessment_2011_data": forest_assessment_data,
            "noc_issuance_data": noc_issuance_data,
            "offence_data": offence_data,
            "block_master_data": block_master_data,
            "forest_fire_alert_data": forest_fire_alert_data,
            "nursery_data": nursery_data,
            "master_produce_data": master_produce_data,
            "produce_auction_data": produce_auction_data,
            "project_shapefile_data": project_shapefile_data,
            "plantation_site_data": plantation_site_data,
            "project_monthly_progress_data": project_monthly_progress_data,
            "species_carbon_data": species_carbon_data,
            "rainfall_dataset_data": rainfall_dataset_data,
            "soil_moisture_data": soil_moisture_data,
            "groundwater_depth_data": groundwater_depth_data,
            "livestock_data": livestock_data,
            "digital_elevation_data": digital_elevation_data,
            "temperature_data": temperature_data,
            "human_settlement_data": human_settlement_data,
            "grassland_water_data": grassland_water_data,
            "forest_fire_data": forest_fire_data,
        })
        
# # New API endpoint
# class CultivableGridAPI(APIView):
#     def get(self, request):
#         # Returns {"27.08422,74.30923": 1, ...}
#         return Response(CULTIVABILITY_MAP) # Return the cultivability map   
import csv
# Load cultivability map at server startup
CULTIVABILITY_MAP = {} # Dictionary to hold cultivability data
# This map will hold the cultivability status for each grid cell
# Key: "lat,lng" (rounded to 5 decimals), Value: 0 or 1 (not cultivable or cultivable)
# Example: "27.08422,74.30923": 1
# Load the grid results CSV file to populate the CULTIVABILITY_MAP
grid_csv_path = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/yolo_results/grid_results.csv"  # Change path!

with open(grid_csv_path, newline='') as csvfile: # Open the CSV file containing grid results
    reader = csv.DictReader(csvfile) # Read the CSV file as a dictionary
    for row in reader: # # Iterate through each row in the CSV
        index = row['index'] # Extract the index from the row
        CULTIVABILITY_MAP[index] = int(row['cultivable']) # Store cultivability as int (0 or 1) in the map

   


# New API endpoint for cultivability map identification using yolov8
class CultivableGridAPI(APIView):
    def get(self, request):
        # Returns {"27.08422,74.30923": 1, ...}
        return Response(CULTIVABILITY_MAP) # Return the cultivability map   


# api to estimate carbon stock 

def parse_coefficients(coeff_str): # helper function to parse coefficients from a string
    """
    Parses a coefficient string like 'a=0.5,c=2.0' into a dictionary {'a': 0.5, 'c': 2.0}.
    """
    coeffs = {}
    if not coeff_str:
        return coeffs
    for part in str(coeff_str).split(','):
        if '=' in part:
            k, v = part.split('=', 1)
            try:
                coeffs[k.strip()] = float(v.strip())
            except ValueError:
                pass
    return coeffs

class DistrictCarbonStockHeatmapAPI(APIView):
    def get(self, request):
        district_carbon_stock = {}
        all_nocs = NoCIssuance.objects.exclude(species_details__isnull=True)
        for noc in all_nocs:
            district = noc.district
            species_info = noc.species_details or {}  # Example: {'Babool': 11, 'Rohida': 31, 'Peepal': 17}
            if not isinstance(species_info, dict):
                continue
            for species, tree_count in species_info.items():
                try:
                    spec = SpeciesCarbonSequestration.objects.get(name__iexact=species)
                    wood_density = float(spec.wood_density) if spec.wood_density else 0.6
                    # Parse coefficients
                    coeffs = parse_coefficients(spec.volume_equation_coefficients)
                    a = coeffs.get('a', 0.5)
                    c = coeffs.get('c', 2.0)   # Use 'c' as exponent (common in volume eqns)
                    # For diameter, use the stored value, else estimate (e.g., 2 cm/year for 10 years)
                    diameter = spec.diameter_growth or 20
                    volume = a * (diameter ** c)  # m³ per tree
                    biomass = volume * wood_density * 1000  # kg (wood_density in g/cm3)
                    agb = biomass * float(spec.biomass_expansion_factor)
                    carbon = agb * float(spec.carbon_fraction)
                    co2 = carbon * float(spec.co2_conversion_factor)
                    total_carbon = co2 * tree_count
                except Exception as e:
                    # print(f"Skipped species {species}: {e}")
                    total_carbon = 0
                district_carbon_stock[district] = district_carbon_stock.get(district, 0) + total_carbon
        return Response(district_carbon_stock)