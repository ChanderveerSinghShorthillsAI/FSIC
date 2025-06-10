from rest_framework.views import APIView
from rest_framework.response import Response
from PIL import Image

# Set your soil image paths and legend mappings here
SOIL_IMAGES = {
    "copper": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Cu.jpg",  # Change to your actual path!
        "legend": {
            (50, 150, 0, 255): "Sufficient",  # Green
            (197, 76, 37, 255): "Deficient",  # red
            # Add other legend colors as needed
        },
    },
    "soil_salinity": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_EC.jpg",  # Change to your actual path!
        "legend": {
            (210, 219, 50, 255): "Mild salinity",  # Yellow
            (208, 207, 82, 255): "Low Salinity",  # brownish
            (141, 182, 0, 255): "High salinity",  # green
            # Add other legend colors as needed
        },
    },
    "iron": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Fe.jpg",  # Change to your actual path!
        "legend": {
            (250, 50, 50, 255): "Deficient",  # red
            (50, 149, 0, 255): "Sufficient",  # green
            # Add other legend colors as needed
        },
    },
    "Mangnese": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Mn.jpg",  # Change to your actual path!
        "legend": {
            (50, 150, 0, 255): "Sufficient",  # Green
            (118, 116, 17, 255): "Deficient",  # red
            # Add other legend colors as needed
        },
    },
    "Organic_Carbon": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_OC.jpg",  # Change to your actual path!
        "legend": {
            (250, 50, 50, 255): "Low",  # Red
            (50, 150, 0, 255): "High",  # Green
            (249, 249, 50, 255): "Medium",  # Yellow
            # Add other legend colors as needed
        },
    },
    "Ph": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_pH.jpg",  # Change to your actual path!
        "legend": {
            (10,98,9,255): "Normal",  # green
            (255,115,222,255): "Slightly Alkaline",  # Pink
            (192,154,107,255): "Moderately Alkaline",  # Brown
            # Add other legend colors as needed
        },
    },
    "Phosphorus": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Fe.jpg",  # Change to your actual path!
        "legend": {
            (50,150,0,255): "High",  # green
            (249,250,50,255): "Medium",  # Yellow
            # Add other legend colors as needed
        },
    },
    "Pottasium": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_P.jpg",  # Change to your actual path!
        "legend": {
            (50,150,0,255): "High",  # green
            (249,250,50,255): "Medium",  # Yellow
            (250, 50, 50, 255): "Low", # Red
            # Add other legend colors as needed
        },
    },
    "Sulphur": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_S.jpg",  # Change to your actual path!
        "legend": {
            (50, 150, 0, 255): "Sufficient",  # Green
            (197, 76, 37, 255): "Deficient",  # red
            # Add other legend colors as needed
        },
    },
    "Zinc": {
        "path": "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/images/2_Zn.jpg",  # Change to your actual path!
        "legend": {
            (50, 150, 0, 255): "Sufficient",  # Green
            (197, 76, 37, 255): "Deficient",  # red
            # Add other legend colors as needed
        },
    },
    # Add other images similarly...
}

# The geo bounds your images represent
MIN_LAT, MAX_LAT = 23.3, 30.9  # South, North (replace with actual)
MIN_LNG, MAX_LNG = 69.3, 78.5  # West, East (replace with actual)


def latlng_to_pixel(lat, lng, img_width, img_height):
    x = int(((lng - MIN_LNG) / (MAX_LNG - MIN_LNG)) * img_width)
    y = int(((MAX_LAT - lat) / (MAX_LAT - MIN_LAT)) * img_height)
    return x, y


def closest_color(rgb, legend):
    # Returns the closest color's name in legend to rgb
    distances = [
        (sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, lrgb)), name)
        for lrgb, name in legend.items()
    ]
    return min(distances, key=lambda x: x[0])[1]


class SoilPropertiesView(APIView):
    def post(self, request, format=None):
        lat = request.data.get("lat")
        lng = request.data.get("lng")
        if lat is None or lng is None:
            return Response({"error": "Missing lat/lng"}, status=400)

        result = {}
        for key, val in SOIL_IMAGES.items():
            try:
                img = Image.open(val["path"])
                width, height = img.size
                x, y = latlng_to_pixel(float(lat), float(lng), width, height)
                rgb = img.getpixel((x, y))[:3]
                value = closest_color(rgb, val["legend"])
                result[key] = value
            except Exception as e:
                result[key] = f"Error: {str(e)}"
        return Response(result)
