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
from functions import get_geo_parameter,coords_calc,make_map_great_again,add_markers,get_segment


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

	if request.method== 'GET':
		depart=request.args.get('depart')
		arrive=request.args.get('arrive')		
		coords = get_geo_parameter(depart,arrive)


		depart = coords[0]
		arrive = coords[1]

		res = coords_calc(coords)


		stop_points = get_segment(depart,arrive,4)


		m =  make_map_great_again(res,coords)

		m = add_markers(m,stop_points)

		map_html = m._repr_html_()

	return map_html



if __name__ == '__main__':

	app.run(debug=True)

