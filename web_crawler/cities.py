"""Module containing cities web scraping code."""

# Import Packages
import pymongo 
import scrapy 
from scrapy.crawler import CrawlerProcess 


class Cities(scrapy.Spider):

    name = 'cities' 
    url = 'https://www.latlong.net/category/cities-236-15'

    def start_requests(self):

        # Loop over all pages
        for page in range(1, 10):
            page_url = self.url + f'-{page}' + '.html'
            yield scrapy.Request(url=page_url, callback=self.parse)

    def parse(self, res):
        # Extract city names 
        locations = res.css('table').css('a::text').getall()
        
        # Extract latitude and longitude
        lat_longs = res.css('table').css('tr').css('td::text').getall()

        lats = []
        longs = []

        for index, cord in enumerate(lat_longs):

            if index % 2 == 0:
                lats.append(cord)
            elif index % 2 == 1:
                longs.append(cord)

        # Establish connection to mongodb atlas cluster
        client = pymongo.MongoClient(f"mongodb+srv://admin:password@vehicles.y1ps2.mongodb.net/vehicles?retryWrites=true&w=majority")
        db = client.vehicles

        # Create collection named cities
        collection = db['cities']

        for (location, lat, long) in zip(locations, lats, longs):

            item = {
                'city': location.split(',')[0],
                'state': location.split(',')[1].strip(),
                'latitude': float(lat),
                'longitude': float(long)
            }

            # Insert document into cities collection
            collection.insert_one(item)

# Main Driver
if __name__=='__main__':
    # Run Scraper 
    process = CrawlerProcess()
    process.crawl(Cities)
    process.start()