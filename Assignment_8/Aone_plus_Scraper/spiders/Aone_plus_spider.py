import scrapy
from ..items import AonePlusScraperItem


class AonePlusSpiderSpider(scrapy.Spider):
    name = "Aone_plus_spider"
    allowed_domains = ["aoneplus.com"]
    start_urls = ["https://aoneplus.com/product-category/computers-laptops/laptops/"]

    def parse(self, response):
        item = AonePlusScraperItem()
        laptops = response.xpath("//div[@id='tokoo-shop-view-content']/ul//li//div[@class='product-outer']")
        for laptop in laptops:
            name = laptop.xpath('.//h2[@class="woocommerce-loop-product__title"]/text()').get()
            link = laptop.xpath('.//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]/@href').get()
            price = laptop.xpath('.//span[@class="price"]/ins/span/bdi/text()').get()

            # yield{'Name' : name,
            #       'Price' : price,
            #       'url' : link

            # }
            item['Name'] = name
            item['Price'] = price
            item['URL'] = link
            yield item
        try:
            next_page = response.xpath("//a[@class='next page-numbers']/@href").get()

            if next_page:
                print('next page')
                next_page_url = next_page
                yield response.follow(next_page_url, self.parse)
        except Exception as e:
            print(e)

        pass
