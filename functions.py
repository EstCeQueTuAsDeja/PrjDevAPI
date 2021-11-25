import folium
import openrouteservice
from geopy.geocoders import Nominatim
from openrouteservice import convert


def get_geo_parameter(depart,arrive):

	geolocator = Nominatim(user_agent="Pierre")
	location = geolocator.geocode(depart)
	depart = [location.longitude,location.latitude]
	location = geolocator.geocode(arrive)
	arrive = [location.longitude,location.latitude]
	center = [(arrive[1]+depart[1])/2,(depart[0]+arrive[0])/2]

	return [depart,arrive]


def coords_calc(coords):

	client = openrouteservice.Client(key='5b3ce3597851110001cf62480449e75063564d28ad2b9bc79cc1d62e')
	
	res = client.directions(coords)
	
	return res


def make_map_great_again(res,coords):

	center = [(coords[0][1]+coords[1][1])/2,(coords[0][0]+coords[1][0])/2]
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

	return m

def get_segment(depart, arrive, autonomie):

	stop_points = []
	point_special = [depart[1]-arrive[1],depart[0]-arrive[0]]
	segment=[point_special[0]/autonomie,point_special[1]/autonomie]

	for i in range(autonomie-1):

		if depart[1]>arrive[1]:
			stop_points.append(depart[1] - (segment[0]*i))

		else :
			stop_points.append(depart[1] + (segment[0]*i))


		if depart[0]>arrive[0]:
			stop_points.append(depart[0] - (segment[1]*i))

		else :
			stop_points.append(depart[0] + (segment[1]*i))
