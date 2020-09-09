import scrapy
import re
from urllib.parse import urljoin

START_URL = 'https://www.yellowpages.com.eg/en/related-categories'

class YellowPagesSpider(scrapy.Spider):
    name = 'yellow_pages'
    start_urls = [START_URL]

    def parse_page(self, response):
        # Get all urls
        urls = response.css("a::attr(href)").getall()

        # Convert urls to absolute
        urls = [urljoin(response.url, url) for url in urls]

        # Filter urls for pages
        pages = [url for url in urls if '/en/related-categories/p' in url]

        # Filter urls for categories
        categories = [url for url in urls if '/en/condensed-category/' in url]
        
        for url in categories:
            yield response.follow(url, self.parse_category)

        for url in pages:
            yield response.follow(url, self.parse_page)

    parse = parse_page

    def parse_category(self, response):
        # Get category key
        url_parts = response.url.split('/')
        category_key = url_parts[url_parts.index('condensed-category') + 1]

        # Get all urls
        urls = response.css("a::attr(href)").getall()

        # Convert urls to absolute
        urls = [urljoin(response.url, url) for url in urls]

        # Filter urls for listing pages
        pages = [url for url in urls if f'/en/condensed-category/{category_key}/p' in url]

        # Filter urls for companies
        companies = [url for url in urls if '/en/profile/' in url]

        # Clean urls
        companies = [url.split('?')[0].split('#')[0] for url in companies]

        for url in companies:
            yield response.follow(url, self.parse_company)

        for url in pages:
            yield response.follow(url, self.parse_category)

    def parse_company(self, response):
        record = {
            'id': response.url.split('/')[-1],
            'title': response.xpath('//h1/text()').get().strip(),
            'address': response.css('.des-address.address::text').get().strip(),
            'categories': response.css('.categories .category a::text').getall(),
            'branches': [a.split('/')[-1] for a in response.css('#branches a::attr(href)').getall()],
            'url': response.url,
        }

        yield record
