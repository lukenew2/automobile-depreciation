from .secret import password

BOT_NAME = 'truecar'

SPIDER_MODULES = ['truecar.spiders']
NEWSPIDER_MODULE = 'truecar.spiders'

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 1

DOWNLOAD_DELAY = 0.25

CONCURRENT_REQUESTS_PER_DOMAIN = 1

COOKIES_ENABLED = False

ITEM_PIPELINES = {
   'truecar.pipelines.MongoPipeline': 100,
}

# LOG_LEVEL = 'INFO'

MONGO_DATABASE = 'vehicles'
MONGO_URI = f'mongodb+srv://admin:{password}@vehicles.y1ps2.mongodb.net/vehicles?retryWrites=true&w=majority'

SCRAPER_SLOT_MAX_ACTIVE_SIZE = 5_000_000_000