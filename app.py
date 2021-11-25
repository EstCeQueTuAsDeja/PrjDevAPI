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
from functions import get_geo_parameter,coords_calc,make_map_great_again,add_markers,get_segment,request_api




app=Flask(__name__)

@app.route('/')
def index():

	con = DBm.connect()	
	con.row_factory = sql.Row
	voitures = DBm.selectAll(con)

	return render_template('index.html', voitures=voitures)

@app.route('/api')
def api():

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

		points_borne = []
		for stop_point in stop_points:
			print(stop_point)
			point_borne=request_api(stop_point)
			points_borne.append(point_borne)

		print(points_borne)

		m =  make_map_great_again(res,coords)

		m = add_markers(m,points_borne)

		map_html = m._repr_html_()

	return map_html



if __name__ == '__main__':

	app.run(debug=True)

