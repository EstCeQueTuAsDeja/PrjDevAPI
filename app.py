from flask import *
from geopy.geocoders import Nominatim
import requests
import json


API_URL = "https://opendata.reseaux-energies.fr/api/records/1.0/search/?dataset=bornes-irve&q=&facet=region"

app=Flask(__name__)

@app.route('/')
def index():
	if request.method== 'GET':
		depart=request.args.get('depart')
		arrive=request.args.get('arrive')		

		geolocator = Nominatim(user_agent="Pierre")
		location = geolocator.geocode(depart)
		depart = [location.latitude,location.longitude]


	return render_template('index.html',depart=depart)

@app.route('/api')
def api():
	response = requests.get(API_URL)
	content = json.loads(response.content.decode("utf-8"))

	return content

if __name__ == '__main__':

	app.run(debug=True)
	'''
	response = requests.get(API_URL)
	content = json.loads(response.content.decode("utf-8"))
	print(content)
	'''