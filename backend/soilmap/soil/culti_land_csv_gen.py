# from ultralytics import YOLO
# import os
# import glob
# from pathlib import Path

# IMAGE_DIR = "sat_images"
# OUT_DIR = "yolo_results"
# os.makedirs(OUT_DIR, exist_ok=True)

# # Load pre-trained YOLOv8 model
# model = YOLO("yolov8n.pt")  # Or yolov8s.pt for slightly better accuracy

# # COCO classes commonly marking "non-cultivable": adjust for your needs
# NOT_CULTIVABLE_CLASSES = [
#     'car', 'truck', 'bus', 'motorcycle', 'bicycle', 
#     'person', 'building', 'road', 'parking meter', 'bench', 
#     'traffic light', 'fire hydrant', 'stop sign' , 'water hydrant',
#     'traffic sign', 'street light', 'fence', 'wall', 'bridge',
#     'tunnel', 'railway', 'power line', 'utility pole', 'telephone pole',
#     'lamp post', 'billboard', 'advertisement', 'sign board', 'construction barrier', 
#     'construction site', 'garbage bin', 'trash can', 'recycling bin', 'street furniture', 
#     'public bench', 'bus stop', 'taxi stand', 'parking lot', 'driveway', 
#     'sidewalk', 'pavement', 'footpath', 'crosswalk', 'pedestrian crossing', 
#     'traffic cone',
# ]

# results_csv = open(os.path.join(OUT_DIR, 'grid_results.csv'), 'w')
# results_csv.write("index,cultivable,detected_classes\n")

# for image_path in glob.glob(f"{IMAGE_DIR}/*.png"):
#     img_name = Path(image_path).name
#     index = img_name.split('_')[1].replace('.png', '')  # <-- NEW
#     result = model(image_path)[0]
#     detected_classes = set()
#     for box in result.boxes:
#         class_idx = int(box.cls[0])
#         detected_class = model.names[class_idx]
#         detected_classes.add(detected_class)
#     # Mark not cultivable if any NOT_CULTIVABLE class is detected
#     if any(cls in NOT_CULTIVABLE_CLASSES for cls in detected_classes):
#         cultivable = 0
#     else:
#         cultivable = 1
#     # results_csv.write(f"{img_name},{cultivable},{'|'.join(detected_classes)}\n")
#     results_csv.write(f"{index},{cultivable},{'|'.join(detected_classes)}\n")
#     print(f"{img_name}: cultivable={cultivable}, classes={detected_classes}")

# results_csv.close()
# print("Inference done. Results in grid_results.csv")

from ultralytics import YOLO # Import YOLO model from ultralytics
import os
import glob # For file path operations
from pathlib import Path # For handling file paths

IMAGE_DIR = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/sat_images"  # <-- Yahi pe prediction CLI se bhi kari thi
OUT_DIR = "/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/yolo_results" # Output directory for results
MODEL_PATH = "/home/shtlp_0060/Desktop/FSIC/runs/classify/train/weights/best.pt"# Path to your trained YOLOv8 model

os.makedirs(OUT_DIR, exist_ok=True) # 
model = YOLO(MODEL_PATH) # Load the trained YOLOv8 model

results_csv = open(os.path.join(OUT_DIR, 'grid_results.csv'), 'w')  # Open results CSV file for writing
results_csv.write("index,cultivable,predicted_class,conf\n") # Write header to CSV

for image_path in glob.glob(f"{IMAGE_DIR}/*.png"):# 
    img_name = Path(image_path).name # Get the image file name
    index = img_name.split('_')[1].replace('.png', '')  # # Extract index from the image name
    # Perform classification inference using the YOLO model
    # task="classify" specifies that we want to classify the image
    # The model will return a prediction object with probabilities and class names

    pred = model(image_path, task="classify")[0] # Get the first prediction
    pred_label = pred.names[pred.probs.top1]   # Get the predicted class label
    conf = float(pred.probs.top1conf) # Get the confidence score of the prediction

    cultivable = 1 if pred_label == "cultivable" else 0 # Determine if the land is cultivable
    results_csv.write(f"{index},{cultivable},{pred_label},{conf:.3f}\n") # Write the results to the CSV file
    print(f"{img_name}: cultivable={cultivable}, class={pred_label}, conf={conf:.3f}")

results_csv.close()
print("Classification inference done. Results in grid_results.csv")
