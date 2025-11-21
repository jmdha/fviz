import flask
import feedparser
import random
import dateutil
import folium
import folium.plugins

sources = [
    'https://feeds.services.tv2.dk/api/feeds/nyheder/rss',
    'https://www.dr.dk/nyheder/service/feeds/senestenyt'
]

entries = []

for source in sources:
    data = feedparser.parse(source)
    entries.extend(data.entries)

entries = sorted(
    entries,
    key=lambda d: dateutil.parser.parse(d.published),
    reverse=True
)

locs = ["Ukraine", "København", "Aarhus"]

locmap = {
    "Ukraine": [48.379433, 31.16558]
}
hmap = folium.Map([56, 10], zoom_start=7, tiles="Cartodb dark_matter")
heat = []

for entry in entries:
    for word in entry.title.split():
        print(word)
        if word in locmap:
            heat.append(locmap[word])
folium.plugins.HeatMap(heat).add_to(hmap)

hmap.get_root().height = "100%"
hmap_html = hmap.get_root()._repr_html_()

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/stories')
def stories():
    return flask.render_template('stories.html', stories=entries[:20])

@app.route('/map')
def map():
    return hmap_html

