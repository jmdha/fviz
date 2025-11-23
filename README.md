#

## local setup
```
git clone https://github.com/jmdha/fviz.git
cd fviz
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python setup.py # This needs to be run first
.venv/bin/python calc.py  # 1. Then these two are run seperately
.venv/bin/flask run       # 2. 'calc.py' is the news tracker, while flask is the webserver
```
