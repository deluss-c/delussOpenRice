from flask import Blueprint, render_template, request
from . import models

scraper = Blueprint("scraper", __name__, static_folder='static')


@scraper.route('/', methods=['GET'])
def index():
    restaurants_list = []
    location = ""
    if request.args:
        name = request.args.get('name')
        location = request.args.get('location')
        ors = models.openRiceScraper()
        restaurants_list = ors.scraper(name, location)
    return render_template('layout.html', restaurants_list=restaurants_list, location=location.title())
