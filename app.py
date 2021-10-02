from flask import Flask
from geopy.geocoders import Nominatim





app=Flask(__name__)

@app.route('/')
def index():
	return "<p>Hilloooooooooooooooo</p>"


if __name__ == '__main__':


	address='Annecy'
	geolocator = Nominatim(user_agent="Pierre")
	location = geolocator.geocode(address)
	print(location.address)
	print((location.latitude, location.longitude))
	#app.run(debug=True)