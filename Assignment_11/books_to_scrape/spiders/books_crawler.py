import scrapy
from scrapy.http import Request
from ..items import BooksToScrapeItem


class BooksCrawlerSpider(scrapy.Spider):
    name = "books_crawler"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]


    def parse(self, response):
        book_urls = response.xpath('//ol[@class="row"]//article[@class="product_pod"]//h3/a/@href').extract()
        # try:
        #     next_page = response.xpath('//li[@class="next"]/a/@href').get()

        #     if next_page:
        #         print('next page')
        #         next_page_url = next_page
        #         yield response.follow(next_page_url, self.parse)
        # except Exception as e:
        #     print(e)
        for url in book_urls:
            yield Request(response.urljoin(url), callback=self.parse_book)

        pass
    def parse_book(self,response):
        item = BooksToScrapeItem()
        
        image = response.urljoin(response.xpath('//div[@class="item active"]/img/@src').get())

        item['image'] = image
        yield item
        pass