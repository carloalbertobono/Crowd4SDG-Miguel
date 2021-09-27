# Crowd4SDG-Miguel
In order to run this interface:

- Create a nice virtual environment 
   - virtualenv -p python3 VIRTUAL
   - source VIRTUAL/bin/activate
  or with conda
   - conda create -n VIRTUAL python=3.8.10
   - conda activate VIRTUAL

- Install these two required packages (this step needs only to be done once):
   - pip install pandas
   - pip install flask
   - pip install Flask-Session
   - pip install geopy
   - pip install geotext
   - pip install folium
- Type: 
   - export FLASK_APP=app.py
- Run the flask app by typing:
   - flask run --host 0.0.0.0 --port 2000


In order to use this interface:
- Select a source, introduce the keywords and set the number of images to be shown (default = 100)
- Select a filter to apply or click on download to get the filtered images in a csv.
- Reset to clean the interface and associated data.
