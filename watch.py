import time
import feedparser
import sqlite3
import spacy

sync_freq     = 15 * 60 # every x seconds
feed_file     = 'feeds.txt'
db_name       = 'fviz.db'

conn = sqlite3.connect(db_name)
cur  = conn.cursor()

nlp = spacy.load('en_core_web_sm')

def load_feeds() -> [str]:
    with open(feed_file) as file:
        return [line.rstrip() for line in file]

def story_exists(url: str) -> bool:
    cur.execute('SELECT * FROM story WHERE url=\"{0}\"'.format(url))
    return cur.fetchone() is not None

def find_links(title: str) -> [int]:
    title = title.replace('"', '')
    title = title.replace('\'', '')
    ntitle = nlp(title)
    links = []
    for ent in ntitle.ents:
        if ent.label_ != 'GPE':
            continue
        s = 'SELECT * FROM loc WHERE asciiname=\"{0}\" ORDER BY population DESC'.format(ent.text)
        cur.execute(s)
        mloc = cur.fetchone()
        if mloc is not None:
            links.append(mloc[0])
    return links

def add_links(sid: int, links: [int]):
    for link in links:
        cur.execute('INSERT OR REPLACE INTO link(story, loc) VALUES(?, ?)',
                    (sid, link))
    conn.commit()

def sync():
    print('sync')
    feeds = load_feeds()
    for feed in feeds:
        print(feed)
        entries = feedparser.parse(feed).entries
        for entry in entries:
            title = entry.get('title', '')
            desc  = entry.get('description', '')
            url   = entry.get('link', '')
            date  = entry.get('published', '')
            if url == '' or story_exists(url):
                continue
            print(title)
            cur.execute("""INSERT INTO story(title, desc, url, date)
                           VALUES(?, ?, ?, ?)""",
                        (title, desc, url, date))
            sid = cur.lastrowid
            if title != '':
                links = find_links(title)
                add_links(sid, links)
            if desc != '':
                links = find_links(desc)
                add_links(sid, links)
    conn.commit()

while True:
    sync()
    time.sleep(sync_freq)
