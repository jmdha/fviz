import sqlite3
import os
import zipfile
import csv
import urllib.request

db_name  = 'fviz.db'
city_url = 'https://download.geonames.org/export/dump/cities1000.zip'
city_zip = 'cities1000.zip'
city_dir = 'cities1000'
citypath = 'cities1000.txt'

# Create DB file and setup tables
conn = sqlite3.connect(db_name)
cur  = conn.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS story(
        id INTEGER PRIMARY KEY,
        title varchar(200) NOT NULL,
        desc varchar(10000) NOT NULL,
        url varchar(200) NOT NULL,
        date datetime
    )"""
)
cur.execute(
    """CREATE TABLE IF NOT EXISTS loc(
        id INTEGER PRIMARY KEY,
        name varchar(200),
        asciiname varchar(200),
        alternatenames varchar(10000),
        country varchar(10),
        lat float, lon float,
        population bigint
    )"""
)
cur.execute(
    """CREATE TABLE IF NOT EXISTS link(
        story INTEGER,
        loc INTEGER,
        PRIMARY KEY (story, loc)
    )"""
)
conn.commit()

# Download and extract city data
urllib.request.urlretrieve(city_url, city_zip)
with zipfile.ZipFile(city_zip, 'r') as zip_ref:
    zip_ref.extractall(city_dir)
os.remove(city_zip)
os.rename(os.path.join(city_dir, citypath), citypath)
os.rmdir(city_dir)

# Insert city data into db
with open(citypath) as cityfile:
    reader = csv.reader(cityfile, delimiter='\t')
    for row in reader:
        if "\"" in row[1]:
            continue
        cur.execute("""INSERT OR REPLACE INTO
                       loc(id, name, asciiname, alternatenames,
                       country, lat, lon, population)
                       VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                    (row[0], row[1], row[2], row[3], row[8],
                     row[4], row[5], row[14]))
os.remove(citypath)

conn.commit()
conn.close()

