import scrapy
import time


class KotvolosPySpider(scrapy.Spider):
    name = "Kotvolos.py"
    allowed_domains = ["www.kotsovolos.gr"]
    start_urls = ["https://www.kotsovolos.gr/household-appliances/fridges/fridge-freezers"]
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    custom_settings = {
    'DOWNLOAD_DELAY': 3,  # 2 seconds delay
    # 'RETRY_TIMES': 5,     # Retry 5 times in case of request failures
    # 'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429],
    # 'CONCURRENT_REQUESTS_PER_DOMAIN': 1  # Limit concurrent requests to one per domain
    }

    def parse(self, response):
        
        for page_no in range(1,11):
            print('page no ====================== ',page_no )
            url = f'https://www.kotsovolos.gr/api/ext/getProductsByCategory?params=pageNumber%3D{page_no}%26pageSize%3D36%26catalogId%3D10551%26langId%3D-24%26orderBy%3D5&catId=35822&storeId=10151&isCPage=false'
            yield scrapy.Request(url, headers=self.headers ,callback=self.parse_json)
            
        pass

    def parse_json(self, reponse):
        print('------------------------------------------------------')
        data = reponse.json()['catalogEntryView']
        # print('@@@@@@@@@@@@@@@@@@0', data[0]["UserData"])
        for i in data:
            U_id = i["uniqueID"]
            name = i["name"]
            url = i["UserData"][0]['seo_url']
            price = i["price_EUR"]

            yield{'Unique id': U_id,
                'Name' : name,
                'URL' : url,
                'Price' : price        
                }
            




