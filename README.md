Project Overview
Till now, the project frontend is made with React Leaflet, and the backend is built with Django. On opening the page, you will see a map of Rajasthan with state and district boundaries, created using the rajasthan.geojson and district.geojson files. On each district, you can see the carbon stock of each district by default, colored according to the scale shown in the UI, which is based on the carbon stock content of each district.

Upon clicking a district, a grid will appear on that district, with each cell measuring 0.05 x 0.05 degrees. When the gridding appears, you will see some grids colored green and others black. The green grids represent areas that can be cultivated, while the black grids indicate areas that cannot be cultivated due to commercialization. This classification is done with the help of a vision model called YOLOv8, which we have trained with 520 satellite images. Using this model, all the grids of Rajasthan (approximately 12,900), whose images are in the sat_images/ folder, are analyzed to predict whether the land is cultivable or not.

Then, upon clicking a green grid, all the data mapped to that grid will appear in the sidebar.

Currently, data fetching is faster with CSVs, but as we have now switched to using databases, the fetching speed has become slower. This can be improved in the future.

Notes on Code
The commented-out code in views.py is for fetching data from CSVs in the data folder, which is faster. However, since shifting to PostgreSQL DB, the fetching speed is currently slower compared to CSVs, but this can be improved later (e.g., by using indexing).

Main Files
Frontend
src/mapview.jsx

src/utils.jsx

Backend
views.py (contains our main backend logic)

models.py (contains the database models used according to the official PDF of the competition and our real data; currently, dummy data is inserted for the tables)

Data and Support Files
data/
Contains all the real-time CSV files.

images/
Contains all the soil property images that we have superimposed on our map to get soil data.

yolo_results/
Contains the predicted model CSV output for all grids.

change_sat_images.py
Used to rename images in the sat_images/ directory.

district.geojson
The main file used for Rajasthan and district boundaries.

culti_land_csv_gen.py
Used to generate a CSV for all the grids to classify them as cultivable or non-cultivable using our YOLO model.

make_rajasthan_grid_csv.py
Used to create the grid over Rajasthan, enabling us to index and rename images as grid_1.png, grid_2.png, etc.

satellite_image_fetcher.py
Used to fetch the 12,900 satellite images of Rajasthan, grid-wise.

rough.py
Used to segregate images in our dataset as cultivable and non-cultivable.

runs/
The output folder generated from running our YOLO model.