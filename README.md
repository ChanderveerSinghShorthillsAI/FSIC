Currently the data is being fetched from csvs only from data folder  and showing on frontend , the commented code in the views.py is of the integration of database to our project , and in the database the data is filled already with some dummy data and some real data in the tables . hence the backend of database integration is working (tested with postman) but the frontend code is not designed yet in mapview.jsx to fetch data from database from backend , so frontend is fetching only csvs data until now . 

main files for frontend - src/mapview.jsx , src/utils.jsx

main files for backend -  


data/ contains all the csvs real time 

images/ it contains all the soil properties images which we have superimposed on our map to get soil data

yolo_results/ it contains the our predicted model csv output of all grids 

change_sat_images.py it is used to rename the sat_images/ images name .

district.geojson - main file on which rajasthan boundaries and district boundaries are made  

culti_land_csv_gen.py - it is used to make csv of all the grids to decide as cultivable and non cultivable sing our yolo model.

make_rajasthan_grid_csv.py - it is used to o gridding on rajasthan on which we can do indexing and rename images as grid_1.png , grid_2.png etc

models.py - it contains the databases which we are about to use according to the official pdf of the competition and our own real data , for their tables we have inserted dummy data for now 

satellite_image_fetcher.py - it is used to fetch 12900 satellite images of rajasthan grid wise .

rough.py - it is used to to segregate image sin our dataset as cultivable and not cultivable  

views.py - contain our main backend logic

runs/ folder is the output folder we got from running our yolo model .