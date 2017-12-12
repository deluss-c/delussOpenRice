from flask import Flask

app = Flask(__name__)

from scraper.views import scraper
app.register_blueprint(scraper)