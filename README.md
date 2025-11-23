# fviz
An analysis of the frequency in which cities are mentioned in the news.

The analysis runs a periodic semantic analysis of various RSS-feeds to find cities, which are then stored in an SQLite database, and then served on a Flask & Leaflet website.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d00e770d-4262-4a49-b457-17da19429c54" />


## data
The city data (Names & Coordinates) is taken from https://geonames.org.

## technologies
 - [flask](https://flask.palletsprojects.com/en/stable/)
 - [leaflet](https://leafletjs.com/)
 - [sqlite3](https://sqlite.org/index.html)
 - [feedparser](https://pypi.org/project/feedparser/)
 - [spacy](https://spacy.io/)

## todo
  - spacy denotes both cities and countries as 'GPE', as such, whenever a country is mentioned it is mistaken as a city. This leads to some false positives, e.g. Venezuela -> A city in Cuba, Mexico -> A city in Philippines.
  - handle duplicate city names. currently the one with the biggest population is chosen, however, that simply means the smaller cities are never linked
  - cache generated map instead of re-rendering on each request

## local setup
```
git clone https://github.com/jmdha/fviz.git
cd fviz
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python setup.py # This needs to be run first
.venv/bin/python watch.py # 1. Then these two are run seperately
.venv/bin/flask run       # 2. 'calc.py' is the news tracker, while flask is the webserver
```
