"""Module containing truecar web scraping spider."""

import json
import requests
import scrapy
from scrapy.loader import ItemLoader
from truecar.items import VehicleItem


class TrueCar(scrapy.Spider):

    name = 'truecar'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'} 
    domain = 'https://www.truecar.com'
    url = 'https://www.truecar.com/used-cars-for-sale/listings/price-above-1000/location-seattle-wa/?page='

    def start_requests(self):

        # Adjust range to adjust number of pages that need scraped
        for page in range(1, 1000):
            next_page = self.url + str(page) + '&searchRadius=5000&sort[]=created_date_desc'

            yield scrapy.Request(url=next_page, 
                                headers=self.headers, 
                                callback=self.parse)
    
    def parse(self, res):

        # Extract links to individual vehicle listings
        links = res.css('ul.margin-bottom-3 li a::attr(href)').getall()

        # Follow each link recursively
        for link in links:
            yield res.follow(url=self.domain + link,
                             headers=self.headers,
                             callback=self.parse_link)

    def parse_link(self, res):
        loader = ItemLoader(item=VehicleItem(), response=res)

        # Features Common to all Vehicles
        loader.add_css('_id', 'p[data-test="vinNumber"]::text')
        loader.add_css('year', 'div.row.margin-top-3 h1.heading-base.d-flex.flex-column.margin-right-2 div.heading-2::text')
        loader.add_css('make', 'div.row.margin-top-3 h1.heading-base.d-flex.flex-column.margin-right-2 div.heading-2::text')
        loader.add_css('model', 'div.row.margin-top-3 h1.heading-base.d-flex.flex-column.margin-right-2 div.heading-2::text')
        loader.add_css('trim', 'div.row.margin-top-3 h1.heading-base.d-flex.flex-column.margin-right-2 div.heading-base::text')
        loader.add_css('price', 'div.row.margin-top-3 div.margin-top-3.margin-top-lg-0.col-12.col-lg-4 div.heading-2.margin-top-3::text')
        loader.add_css('mileage', 'div.row.margin-top-3 div.margin-top-3.margin-top-lg-0.col-12.col-lg-4 p.margin-top-1::text')
        loader.add_css('location', 'div.margin-top-3 div.padding-top-2 div.d-flex.align-items-center.padding-top-1 p::text')
        loader.add_css('date_listed', 'p[data-test="listedDays"]::text')
        
        # Vehicle Overview Features
        features = res.css('div.container.container-max-width-2 div.padding-y-5 div.d-flex.flex-column div.heading-4::text').getall()
        values = res.css('div.container.container-max-width-2 div.padding-y-5 div.d-flex.flex-column p.font-size-3::text').getall()
        
        for (feature, value) in zip(features, values):
            feature_clean = feature.lower().replace(' ', '_')
            loader.add_value(feature_clean, [value])

        # Vehicle History Report Features
        values = res.css('fieldset.d-flex.w-100.padding-top-2_5 div.heading-2::text').getall()
        features = res.css('fieldset.d-flex.w-100.padding-top-2_5 p._1crvurj::text').getall()     

        for (feature, value) in zip(features, values):
            feature_clean = feature.lower().replace(' ', '_')

            # Feature name changes to owner when vehicle has singular owner
            # Here we ensure our feature name stays consistent
            if feature_clean == 'owner':
                feature_clean = 'owners'

            # Same thing as above with accidents feature
            if feature_clean == 'accident':
                feature_clean = 'accidents'

            loader.add_value(feature_clean, [value])

        # Features from VIN Decoder
        # VIN Decoder API
        vin_api = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/'
        vin = res.css('p[data-test="vinNumber"]::text').get()

        # Send Post Request to API with VIN
        post_fields = {'format': 'json', 'data': vin}
        r = requests.post(url=vin_api, data=post_fields)

        # Load Decoded VIN Data
        vin_decoded = json.loads(r.text)['Results'][0]

        # Extract Series and Trim from VIN Decoder
        loader.add_value('vin_series', vin_decoded['Series'])
        loader.add_value('vin_trim', vin_decoded['Trim'])
        
        yield loader.load_item()