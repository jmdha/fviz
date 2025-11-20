import flask
import feedparser
import random
import dateutil

sources = [
    'https://feeds.services.tv2.dk/api/feeds/nyheder/rss',
    'https://www.dr.dk/nyheder/service/feeds/senestenyt'
]

tentries = []

for source in sources:
    data = feedparser.parse(source)
    tentries.extend(data.entries)

entries = sorted(
    tentries,
    key=lambda d: dateutil.parser.parse(d.published),
    reverse=True
)

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/stories')
def stories():
    return flask.render_template('stories.html', stories=entries[:20])
