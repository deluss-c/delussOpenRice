#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import urllib
from bs4 import BeautifulSoup
import eventlet


class openRiceScraper():
    def __init__(self):
        self.base_url = "https://www.openrice.com"
        self.country = "hongkong"
        self.language_short = "en"

    def fetch(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }
        req = urllib2.Request(url, None, headers)
        r = urllib2.urlopen(req).read()
        return r

    def get_restaurant_data(self, html):
        soup = BeautifulSoup(html, "lxml")

        restaurant_dict = {}
        restaurant_dict["english_name"] = soup.find('div', {"class": "smaller-font-name"}).text
        restaurant_dict["chinese_name"] = soup.find('div', {"class": "poi-name-container "}).find('span').text
        # issue on openrice: for this page the english adress is in chinese, if we put english as a language we got chinese adresse then english adress (wrong order) and if we put the page in chinese we get both adresse in chinese
        address_div = soup.find_all('section', {"class": "address-section"})[0].find_all('a', {"data-href": "#map"})
        restaurant_dict["english_address"] = address_div[0].text.strip()
        restaurant_dict["chinese_address"] = address_div[1].text.strip()

        tag_list = soup.find('div', {"class": "header-poi-categories dot-separator"}).find_all('a')
        tags = ""
        for tag in tag_list:
            tags = tags + tag.text + ","
        restaurant_dict["tags"] = tags[:-1]

        a_content = soup.find('div', {"class": "main-menu table-center"}).find_all('a')[2].text
        restaurant_dict["photo_number"] = a_content[a_content.find("(") + 1:a_content.find(")")]
        return restaurant_dict

    def get_restaurant_urls(self, r):
        soup = BeautifulSoup(r, "lxml")
        soup_restaurants = soup.find_all('li', {
            "class": "sr1-listing-content-cell pois-restaurant-list-cell first-poi-in-same-region"})
        soup_restaurants = soup_restaurants + soup.find_all('li', {
            "class": "sr1-listing-content-cell pois-restaurant-list-cell "})

        restaurant_urls = []
        for soup_restaurant in soup_restaurants[:10]:
            url_complement = soup_restaurant.find_all('div', {"class": "title-wrapper"})[0].find('a')['href']
            restaurant_urls.append(self.base_url + url_complement)
        return restaurant_urls

    def scraper(self, name, location):
        name = urllib.quote_plus(name)
        location = urllib.quote_plus(location)
        url = self.base_url + '/' + self.language_short + '/' + self.country \
              + '/restaurants?where=' + location + '&what=' + name
        r = self.fetch(url)

        restaurant_urls = self.get_restaurant_urls(r)

        pool = eventlet.GreenPool()
        restaurant_html = []
        for body in pool.imap(self.fetch, restaurant_urls):
            restaurant_html.append(body)

        restaurants_list = []
        for html in restaurant_html:
            restaurant_dict = self.get_restaurant_data(html)
            restaurants_list.append(restaurant_dict)

        return restaurants_list
