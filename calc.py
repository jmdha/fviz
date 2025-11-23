import time
import feedparser
import sqlite3
import urllib.request
import os
import zipfile
import csv

sync_freq     = 15 * 60 # every x seconds
feed_file     = 'feeds'
db_name       = 'story.db'
cities500_url = 'https://download.geonames.org/export/dump/cities500.zip'
cities500_zip = 'cities500.zip'
cities500_dir = 'cities500'
cities500     = 'cities500.txt'

conn = sqlite3.connect(db_name)

def cities500_init():
    if not os.path.isfile(cities500):
        urllib.request.urlretrieve(cities500_url, cities500_zip)
        with zipfile.ZipFile(cities500_zip, 'r') as zip_ref:
            zip_ref.extractall(cities500_dir)
        os.remove(cities500_zip)
        os.rename(os.path.join(cities500_dir, cities500), cities500)
        os.rmdir(cities500_dir)

def db_init():
    cur  = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS story(
            id INTEGER PRIMARY KEY, title varchar(200) NOT NULL, url varchar(200) NOT NULL
        )"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS loc(
            id INTEGER PRIMARY KEY, name varchar(200), lat float, lon float
        )"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS link(
            story INTEGER, loc INTEGER, PRIMARY KEY (story, loc)
        )"""
    )
    conn.commit()

def db_cities_fill():
    cur = conn.cursor()
    with open(cities500) as citiesfile:
        reader = csv.reader(citiesfile, delimiter='\t')
        for row in reader:
            if "\"" in row[1]:
                continue
            s = """INSERT OR REPLACE INTO loc (id, name, lon, lat)
                   VALUES({id}, \"{name}\", {lon}, {lat})"""
            s = s.format(id=row[0], name=row[2], lon=row[4], lat=row[5])
            cur.execute(s)
    conn.commit()

def setup():
    cities500_init()
    db_init()
    db_cities_fill()

def load_feeds() -> [str]:
    with open(feed_file) as file:
        return [line.rstrip() for line in file]

def story_exists(url: str) -> bool:
    s = "SELECT * FROM story WHERE url=\"{url}\""
    s = s.format(url=url)
    cur = conn.cursor()
    cur.execute(s)
    return cur.fetchone() is not None

def add_links(story_id: int, title: str):
    cur  = conn.cursor()
    for word in title.split():
        s = "SELECT * FROM loc WHERE name=\"{word}\""
        s = s.format(word=word)
        cur.execute(s)
        loc_id = cur.fetchone()
        if loc_id is not None:
            loc_id = loc_id[0]
            s = """INSERT INTO link(story, loc)
                   VALUES({story_id}, {loc_id})"""
            s = s.format(story_id=story_id, loc_id=loc_id)
            cur.execute(s)
    conn.commit()

def sync():
    feeds = load_feeds()
    cur  = conn.cursor()
    print('loading feeds...')
    for feed in feeds:
        data    = feedparser.parse(feed)
        entries = data.entries
        for entry in entries:
            title = entry.title.replace("\"", "\"\"")
            url   = entry.link.replace("\"", "\"\"")
            if story_exists(url):
                continue
            print(title)
            s = """INSERT INTO story (title, url)
                   VALUES(\"{title}\", \"{url}\")"""
            s = s.format(title=title, url=url)
            cur.execute(s)
            cur.execute("SELECT last_insert_rowid()")
            i = cur.fetchone()[0]
            add_links(i, title)
    conn.commit()

setup()
while True:
    sync()
    time.sleep(sync_freq)
