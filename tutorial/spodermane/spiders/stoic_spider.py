import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://www.goodreads.com/quotes/tag/stoicism'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.quoteText'):
            yield {
                'text': quote.css('::text').get(),
                'author': quote.css('span.authorOrTitle::text').get(),
                'book': quote.css('a.authorOrTitle::text').get(),
                # 'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('a.next_page::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
