import scrapy
from datetime import datetime, timedelta
from urllib.parse import urljoin
import re


class NdtvSpiderSpider(scrapy.Spider):
    name = "ndtv_spider"
    allowed_domains = ["www.ndtv.com"]
    start_urls = ["https://www.ndtv.com/latest/"]

    def parse(self, response):
        today = datetime.today().date()
        articles = response.css('div.lisingNews div.news_Itm')
        
        for article in articles:
            link = article.css('a::attr(href)').get()
            title = article.css('a::text').get().strip()
            pub_date = self.extract_date_from_string(article.css('span.pst-by_lnk::text').get())
            
            if pub_date > today:
                yield response.follow(link, callback=self.parse_article)
            elif pub_date == today and title not in self.titles:
                yield response.follow(link, callback=self.parse_article)
            else:
                print(f"Ignoring article: {title} published on {pub_date}")
        
        next_page = response.css('a.btnLnk arrowBtn next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        pass


    def parse_article(self, response):
        title = response.css('h1.sp-ttl::text').get().strip()
        link = response.url
        description = response.css('div.story__content p::text').getall()
        if not description:
            description = response.css('div.sp-cn.ins_storybody p::text').getall()
        description = '\n'.join(description).strip()
        
        pub_date = self.extract_date_from_string(response.css('span.pst-by_lnk::text').get())
        
        yield {
            'title': title,
            'link': link,
            'description': description,
            'pubDate': pub_date,
            'DateFetched': datetime.now(),
            'source': 'NDTV'
        }
    
    def extract_date_from_string(self, string):
        # Define the regex pattern to match the date format
        pattern = r"([a-zA-Z]+) (\d{1,2}), (\d{4})"

        # Search for the pattern in the string
        match = re.search(pattern, string)

        if match:
            # Extract the matched groups
            month_str, day_str, year_str = match.groups()

            # Convert month string to its numerical representation
            month = datetime.strptime(month_str, "%B").month

            # Convert strings to integers
            day = int(day_str)
            year = int(year_str)

            # Create a datetime object
            date = datetime(year, month, day).date()
            
            return date
        else:
            return None
