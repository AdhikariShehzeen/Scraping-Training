from typing import Iterable
import scrapy
import json
import re


class AjioSpiderSpider(scrapy.Spider):
    name = "ajio_spider"
    allowed_domains = ["www.ajio.com"]
    start_urls = ["https://www.ajio.com/"]

    def parse(self, response):
        # links = response.xpath("//a[re:test(@href, '/c/\d+')]/@href").extract()
        a_tags = response.xpath("//li[@data-test='li-WOMEN']//div[@class='items']//a").extract()

        pattern = re.compile(r'/c/(\d+)')

        # Extract the href values matching the pattern
        categories = [match.group(1) for tag in a_tags if (match := pattern.search(tag))]
        
        for category in categories:
            print('----------------------------------------',category)
            yield scrapy.Request(url=self.start_urls[0],callback=self.start_requests_for_category,meta={'category': category})
           
    def start_requests_for_category(self, response):
        category = response.meta['category']
        
        for i in range(5):
            print('---------------------------------------',i)
            api = f'https://www.ajio.com/api/category/{category}?fields=SITE&currentPage={i}&pageSize=45&format=json&query=%3Arelevance&sortBy=relevance&gridColumns=3&advfilter=true&platform=Desktop&showAdsOnNextPage=true&is_ads_enable_plp=true&displayRatings=true'
            yield scrapy.Request(api, callback=self.parse_json)
    #     pass

    def parse_json(self, response):
        # print(type(response.json()))
        # print('----------------------',response.json())
        print('in parse')
        data = json.loads(response.text)
        products = data.get('products', [])
        print(len(products))
        roducts = data.get('products', [])


        for product in products:
            yield {
                "name": product.get('name', 'N/A'),
                "brandName": product.get('fnlColorVariantData',{}).get('brandName', 'N/A'),
                "discountPercent": product.get('discountPercent', '0%').replace(f'% off', '').strip(),
                "new_price": product.get('price', {}).get('formattedValue', 'Rs.0.00').replace('Rs.', '').replace(',', '').strip(),
                "old_price": product.get('wasPriceData', {}).get('formattedValue', 'Rs.0.00').replace('Rs.', '').replace(',', '').strip(),
                "rating": product.get('averageRating', '0'),
                "rating_count": product.get('ratingCount', '0').replace('K', '000').replace(',', '').strip(),
                "segment_name": product.get('segmentNameText', 'N/A'),
                "brickNameText": product.get('brickNameText','N/A'),
                "url": product.get('url', ''),
            }
        pass
