import scrapy


class TestSpiderSpider(scrapy.Spider):
    name = "test_spider"
    allowed_domains = ["webscraper.io"]
    start_urls = ["https://webscraper.io/test-sites/e-commerce/static/computers/tablets"]
    # def start_requests(self):
    #     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    #                 }
    #     yield scrapy.Request(url=self.start_urls, headers=headers, callback=self.parse)


    def parse(self, response):
        products = response.xpath('//div[@class= "product-wrapper card-body"]')
        for product in products:
            product_name = product.xpath('.//a[@class="title"]/@title').get()
            product_price = product.xpath(".//div[@class='caption']//h4[@class='price float-end card-title pull-right']/text()").get()
            rating = product.xpath('.//div[@class="ratings"]//p[2]//@data-rating').get()
            reviews = product.xpath('.//div[@class="ratings"]/p[@class="review-count float-end"]/text()').get()
            product_link = 'https://webscraper.io' + product.xpath('.//a[@class="title"]/@href').get()
            yield{'product_name': product_name,
                  'product_price' : product_price,
                  'rating' : rating,
                  'reviews' : reviews,
                  'product_link' : product_link

            }
        next_page = response.css('a[rel="next"] ::attr(href)').get()

        if next_page is not None:
           print('next page')
           next_page_url =  next_page
           yield response.follow(next_page_url, callback=self.parse)



        pass
