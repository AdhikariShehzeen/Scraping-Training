import scrapy


class BookSpiderSpider(scrapy.Spider):
    name = "book_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        articles = response.css('article.product_pod')
        for article in articles:
            book_name = article.css('h3 a[href]::text').get()
            book_link = article.css('h3 a[href]').extract()[0]
            book_price = article.css('div.product_price p.price_color::text').get()
            yield{'book_name':book_name,
                  'book_link': book_link,
                  'book_price' : book_price

            }

        pass
