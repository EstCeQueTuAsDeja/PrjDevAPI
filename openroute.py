import openrouteservice
import json
import folium
from openrouteservice import convert



client = openrouteservice.Client(key='5b3ce3597851110001cf62480449e75063564d28ad2b9bc79cc1d62e')


coords = [[5.7357819,45.1875602],[6.1288847,45.8992348]]
#call API
res = client.directions(coords)
#test our response
# with(open('test.json','+w')) as f:
#  f.write(json.dumps(res,indent=4, sort_keys=True))

decoded = convert.decode_polyline(res['routes'][0]['geometry'])

distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
duration_txt = "<h4> <b>Temps :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"

m = folium.Map(location=[45.1875602, 5.7357819],zoom_start=5, control_scale=True,tiles="cartodbpositron")
folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt,max_width=300)).add_to(m)
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



m.save('map.html')

