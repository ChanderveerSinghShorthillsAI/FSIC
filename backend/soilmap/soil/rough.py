import os
import shutil
import pandas as pd

csv_file = '/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/labeled_image_data_of_lands.csv'
images_folder = '/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/testing_images'
output_folder = '/home/shtlp_0060/Desktop/FSIC/backend/soilmap/soil/data/dataset/images/'

df = pd.read_csv(csv_file)
for idx, row in df.iterrows():
    img = row['filename']
    label = 'cultivable' if row['label'] == '[cultivable]' else 'non-cultivable'
    src = os.path.join(images_folder, img)
    dst_dir = os.path.join(output_folder, label)
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy(src, dst_dir)
