"""
Web scraping that gets a collection of COVID-19 myths from
https://www.newsguardtech.com/special-reports/coronavirus-misinformation-tracking-center/
using the scrapy library.
"""
import scrapy


class NewsGuardScraperSpider(scrapy.Spider):
    name = 'newsguard'

    start_urls = ['https://www.newsguardtech.com/special-reports/coronavirus-misinformation-tracking-center/']

    def parse(self, response):
        myths = response.xpath("//ol/li/strong/a/text()").extract()
        file_name = 'extracted_myths.txt'
        print(myths)
        with open(file_name, 'w') as f:
            for myth in myths:
                myth = myth.replace('\xa0', '')
                myth = myth.replace('“', '')
                myth = myth.replace('”', '')
                myth = myth.replace('MYTH:', '')
                myth = myth.strip()
                f.write(myth + '\n')
