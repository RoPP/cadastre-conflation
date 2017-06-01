import geojson

from db_utils import Postgis
from flask import Flask, render_template, jsonify

app = Flask(__name__)
db = Postgis('gis', 'docker', 'docker', 25432, 'localhost')


@app.route('/')
def index() -> object:
    return render_template('index.html')


@app.route('/insee/<int:insee>', methods=['GET'])
def api_insee(insee) -> dict:
    color_city = db.get_insee(insee)
    return geojson.dumps(color_city)


@app.route('/colors/<lonNW>/<latNW>/<lonSE>/<latSE>/<colors>', methods=['GET'])
def api_color(colors, lonNW, latNW, lonSE, latSE) -> dict:
    color_city = db.get_city_with_colors(colors.split(','), float(lonNW), float(latNW), float(lonSE), float(latSE))
    return geojson.dumps(color_city)


@app.route('/colors', methods=['GET'])
def api_colors_list() -> dict:
    return jsonify(db.get_colors())


if __name__ == '__main__':
    app.run(host='0.0.0.0')
