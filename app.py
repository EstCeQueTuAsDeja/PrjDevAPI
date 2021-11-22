from flask import *
from geopy.geocoders import Nominatim
import requests
import json
import sqlite3 as sql
import initdatabase as iDB
import dbmanage as DBm
from zeep import Client
import openrouteservice
from openrouteservice import convert
import folium


API_URL = "https://opendata.reseaux-energies.fr/api/records/1.0/search/?dataset=bornes-irve&q=&facet=region"

app=Flask(__name__)

@app.route('/')
def index():

	con = DBm.connect()	
	con.row_factory = sql.Row
	voitures = DBm.selectAll(con)

	return render_template('index.html', voitures=voitures)

@app.route('/api')
def api():

	client = openrouteservice.Client(key='5b3ce3597851110001cf62480449e75063564d28ad2b9bc79cc1d62e')
	coords = [[5.7357819,45.1875602],[6.1288847,45.8992348]]
	res = client.directions(coords)
	decoded = convert.decode_polyline(res['routes'][0]['geometry'])
	response = requests.get(API_URL)
	content = json.loads(response.content.decode("utf-8"))

	return content



@app.route('/soap')
def soap():
	client = Client(wsdl='http://127.0.0.1:8000/?wsdl')
	result = client.service.get_time(100, 2)

	return str(result)

@app.route('/map')
def map():


	client = openrouteservice.Client(key='5b3ce3597851110001cf62480449e75063564d28ad2b9bc79cc1d62e')

	if request.method== 'GET':
		depart=request.args.get('depart')
		arrive=request.args.get('arrive')		

		geolocator = Nominatim(user_agent="Pierre")
		location = geolocator.geocode(depart)
		depart = [location.longitude,location.latitude]
		location = geolocator.geocode(arrive)
		arrive = [location.longitude,location.latitude]
		center = [(arrive[1]+depart[1])/2,(depart[0]+arrive[0])/2]


		coords = [depart,arrive]
		res = client.directions(coords)
		decoded = convert.decode_polyline(res['routes'][0]['geometry'])
		distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
		m = folium.Map(location=center,zoom_start=7, control_scale=True,tiles="cartodbpositron")
		folium.GeoJson(decoded).add_child(folium.Popup(distance_txt,max_width=300)).add_to(m)
		folium.Marker(
		    location=list(coords[0][::-1]),
		    popup="Grenoble",
		    icon=folium.Icon(color="blue"),
		).add_to(m)

		folium.Marker(
		    location=list(coords[1][::-1]),
		    popup="Annecy",
		    icon=folium.Icon(color="red"),
		).add_to(m)

	#return str(center)
	return m._repr_html_()




if __name__ == '__main__':

	app.run(debug=True)
	'''
	response = requests.get(API_URL)
	content = json.loads(response.content.decode("utf-8"))
	print(content)
	'''
