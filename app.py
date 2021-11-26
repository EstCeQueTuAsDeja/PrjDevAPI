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


	return str(result)

@app.route('/map')
def map():

	if request.method== 'GET':
		depart=request.args.get('depart')
		arrive=request.args.get('arrive')
		voiture=request.args.get('voitures')
		coords = get_geo_parameter(depart,arrive)

		con = DBm.connect()	
		con.row_factory = sql.Row
		voitures = DBm.selectModel(con,voiture)

		autonomie = float(voitures[0][2])
		

		temps_chargement_voiture = voitures[0][3]
		 




		depart = coords[0]
		arrive = coords[1]
		res = coords_calc(coords)

		distance = res['routes'][0]['summary']['distance']/1000

		stop_count = round(distance/autonomie,0)+1
		
		temps_de_pause = (temps_chargement_voiture/60) * stop_count



		stop_points = get_segment(depart,arrive,stop_count)
		client = Client(wsdl='http://127.0.0.1:8000/?wsdl')
		result = client.service.get_time(int(round(distance,0)), int(round(temps_de_pause,0)))

		points_borne = []
		for stop_point in stop_points:
			
			point_borne=request_api(stop_point)
			points_borne.append(point_borne)

		

		m =  make_map_great_again(res,coords)

		m = add_markers(m,points_borne)

		map_html = m._repr_html_()

	return render_template('map.html',map=map_html,distance=round(distance,2),time=round(result,2))



if __name__ == '__main__':

	app.run(debug=True,port=80)

