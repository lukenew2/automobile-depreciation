"""Module containing vehicle listings web scraping code"""

# Import Packages
from security import password

import datetime
import json
import pymongo
import re
import requests
import scrapy
from scrapy.crawler import CrawlerProcess

class TrueCar(scrapy.Spider):

    name = 'truecar'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
    url = 'https://www.truecar.com/used-cars-for-sale/listings/price-above-1000/location-seattle-wa/?page='

    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25
    }

    def start_requests(self):
        # Loop over all pages 
        for page in range(1, 22770):
            next_page = self.url + str(page) + '&searchRadius=5000'
            yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse)

    def parse(self, res):
        # extract links
        links = res.css('ul.margin-bottom-3').css('li').css('a::attr(href)').getall()

        # follow links recursively
        for link in links:
            yield res.follow(url=link, headers=self.headers, callback=self.parse_link)

    def parse_link(self, res):
        # Extract year, make, and model
        title = res.css('div.margin-top-3').css('div.heading-2::text').get().replace('\xa0', ' ').split(' ')

        # Extract price 
        price = res.css('div.margin-top-3').css('div.margin-top-3.margin-top-lg-0.col-12.col-lg-4').css('div.heading-2.margin-top-3::text').get()

        # Extract mileage
        mileage = res.css('div.margin-top-3').css('div.margin-top-3.margin-top-lg-0.col-12.col-lg-4').css('p.margin-top-1::text').get()

        # Extract location
        location = res.css('div.margin-top-3').css('div.margin-top-3.margin-top-lg-0.col-12.col-lg-4').css('div.padding-top-2').css('p::text').get()
        city = location.split(',')[0]
        state = location.split(',')[1].strip()

        # Query latitude and longitude from existing mongodb collection
        # Establish connection to mongodb atlas cluster
        client = pymongo.MongoClient(f"mongodb+srv://admin:{password}@vehicles.y1ps2.mongodb.net/vehicles?retryWrites=true&w=majority")
        db = client.vehicles

        # Connect to cities collection
        cities = db.get_collection('cities')

        # Query latitude and longitude 
        lat_long = cities.find_one({
            'city': city,
            'state': state
        }, {
            '_id': 0, 
            "latitude": 1,
            "longitude": 1
        })

        # Ensure existence of city in collection
        if lat_long:
            lat = lat_long["latitude"]
            lng = lat_long["longitude"]

        # Use random location in state for coordinates
        else:
            lat_long = cities.find_one({
                'state': state
            }, {
                '_id': 0, 
                "latitude": 1,
                "longitude": 1
            })

            lat = lat_long["latitude"]
            lng = lat_long["longitude"]

        # Extract listing date
        days_ago = datetime.timedelta(int(res.css('div.padding-y-4').css('div._uoj6re.padding-left-2').css('p::text').get().split(' ')[0]))
        today = datetime.date.today()

        # Extract VIN
        vin = res.css('div.padding-y-4').css('div.margin-top-3.margin-top-sm-0.col-12.col-sm-6.col-md-4').css('div._uoj6re.padding-left-2').css('p::text').get()

        items = {
            'vin': vin,
            'year': int(title[0]),
            'make': title[1],
            'model': ' '.join(title[2:]).strip(),
            'price': int(re.sub('[^\d.]', '', price)),
            'mileage': int(re.sub('[^\d.]', '', mileage)),
            'location': {
                    'city': city,
                    'state': state,
                    'latitude': lat,
                    'longitutde': lng
                },
            'date_listed': str(today - days_ago),
        }

        # Extract vehicle overview features
        feature_names = res.css('div.container.container-max-width-2').css('div.padding-y-5').css('div.row').css('div.d-flex.flex-column').css('div.heading-4::text').getall()
        values = res.css('div.container.container-max-width-2').css('div.padding-y-5').css('div.row').css('div.d-flex.flex-column').css('p.font-size-3::text').getall()

        for (feature, value) in zip(feature_names, values):
            clean_feature = feature.lower().replace(' ', '_')
            items[clean_feature] = value

        # Extract vehicle history report
        history_report_values = res.css('fieldset.d-flex.w-100.padding-top-2_5').css('div.heading-2::text').getall()
        history_report_names = res.css('fieldset.d-flex.w-100.padding-top-2_5').css('p._1crvurj::text').getall()

        for (feature, value) in zip(history_report_names, history_report_values):
            clean_feature = feature.lower().replace(' ', '_')
            items[clean_feature] = value

        # Clean city and highway mpg
        items['mpg'] = {
                items['mpg'].split()[1]: int(items['mpg'].split()[0]),
                items['mpg'].split()[4]: int(items['mpg'].split()[3])
            }
        
        # Decode VIN for additional information using API call
        vin_api = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/'
        post_fields = {'format': 'json', 'data': vin}
        r = requests.post(url=vin_api, data=post_fields)
        vin_decoded = json.loads(r.text)['Results'][0]

        # Extract series
        series = vin_decoded['Series']
        items['series'] = series 

        # Extract trim
        trim = vin_decoded['Trim']
        items['trim'] = trim

        # Create collection names vehicle_listings
        collection = db['vehicle_listings']

        # Insert document into collection
        collection.insert_one(items)

# main driver
if __name__=='__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(TrueCar)
    process.start()