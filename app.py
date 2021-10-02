from flask import *
from geopy.geocoders import Nominatim





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


if __name__ == '__main__':

	app.run(debug=True)