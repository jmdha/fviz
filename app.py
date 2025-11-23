import flask
import folium
import folium.plugins
import sqlite3

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/map')
def map():
    conn = sqlite3.connect('fviz.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT A.lat, A.lon
        FROM loc A
        INNER JOIN link B
        ON A.id == B.loc
    """)
    heat = cur.fetchall()
    hmap = folium.Map([18, 18], zoom_start=3, tiles="Cartodb dark_matter")
    folium.plugins.HeatMap(heat).add_to(hmap)
    hmap.get_root().height = "100%"
    return hmap.get_root()._repr_html_()
