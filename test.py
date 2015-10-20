import urllib2
import urllib
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
	f=urllib.urlopen("http://www.hz66.com")
	s=f.read()
	return s

if __name__ == '__main__':
	app.run(debug=True)