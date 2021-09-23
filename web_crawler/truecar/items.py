from .settings import MONGO_DATABASE, MONGO_URI

import datetime
import pymongo
import re
from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst

def make_numerical(text):
    """Transforms strings that are numerical into integer values."""
    return int(re.sub('[^\d.]', '', text))

def parse_year(text):
    """Returns year from parse_text function."""
    return int(text.split(' ')[0])

def parse_make(text):
    """Returns make from parse_text function."""
    return text.replace('\xa0', ' ').split(' ')[1]

def parse_model(text):
    """Returns model from parse_text function."""
    return ' '.join(text.split()[2:])

def parse_trim(text):
    """Returns clean trim text."""
    return text.replace('\xa0', ' ')

def geocode(location):
    """Geocode from city and state."""
    loc = location.split(',')

    city = loc[0]
    state = loc[1].strip()

    # Connect to database containing latitude and longitude data
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]

    # Connect to collection cities
    cities = db.get_collection('cities')

    # Query latitude and longitude from city and state
    lat_long = cities.find_one({
            'city': city,
            'state': state
        }, {
            '_id': 0, 
            "latitude": 1,
            "longitude": 1
        })

    # Check if query found match
    if lat_long:
        lat = lat_long["latitude"]
        lng = lat_long["longitude"]

    # If city not in database use random location in state for coordinates.
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

    return {
        'city': city, 
        'state': state, 
        'latitude': lat, 
        'longitude': lng
        }

def parse_listing_date(text):
    """Extract date from how many days ago vehicle was listed."""

    days_ago = datetime.timedelta(int(text.split(' ')[0]))
    today = datetime.date.today()

    return str(today - days_ago)

def parse_mpg(text):
    """Returns dictionary containing city and highway mpg."""
    mpg = text.split()

    return {
        "cty": int(mpg[0]),
        "hwy": int(mpg[3])
    }

class VehicleItem(Item):
    # Using VIN as MongoDB unique identifier field.
    _id = Field(output_processor=TakeFirst())

    # Features common to all vehicle listings
    year = Field(
        input_processor=MapCompose(parse_year),
        output_processor=TakeFirst()
    )
    make = Field(
        input_processor=MapCompose(parse_make),
        output_processor=TakeFirst()
    )
    model = Field(
        input_processor=MapCompose(parse_model, str.strip),
        output_processor=TakeFirst()
    )
    trim = Field(output_processor=TakeFirst())
    price = Field(
        input_processor=MapCompose(make_numerical),
        output_processor=TakeFirst()
    )
    mileage = Field(
        input_processor=MapCompose(make_numerical),
        output_processor=TakeFirst()
    )
    location = Field(
        input_processor=MapCompose(geocode),
        output_processor=TakeFirst()
    )
    date_listed = Field(
        input_processor=MapCompose(parse_listing_date),
        output_processor=TakeFirst()
    )

    # Vehicle Overview Features
    style = Field(output_processor=TakeFirst())
    exterior_color = Field(output_processor=TakeFirst())
    interior_color = Field(output_processor=TakeFirst())
    mpg = Field(
        input_processor=MapCompose(parse_mpg),
        output_processor=TakeFirst()
    )
    engine = Field(output_processor=TakeFirst())
    drive_type = Field(output_processor=TakeFirst())
    fuel_type = Field(output_processor=TakeFirst())
    transmission= Field(output_processor=TakeFirst())

    # Features pertaining to trucks only
    cab_type = Field(output_processor=TakeFirst())
    bed_length = Field(output_processor=TakeFirst())

    # Vehicle History Report Features 
    accidents = Field(output_processor=TakeFirst())
    title = Field(output_processor=TakeFirst())
    owners = Field(output_processor=TakeFirst())
    use_type = Field(output_processor=TakeFirst())

    # Features from VIN decoder 
    vin_series = Field(output_processor=TakeFirst())
    vin_trim = Field(output_processor=TakeFirst())