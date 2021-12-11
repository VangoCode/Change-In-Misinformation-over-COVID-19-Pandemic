"""
Web scraping that gets a collection of COVID-19 myths from
https://www.newsguardtech.com/special-reports/coronavirus-misinformation-tracking-center/
using the scrapy library.
"""
import scrapy


class NewsGuardScraperSpider(scrapy.Spider):
    """
    A spider that scrapes the myths from the NewsGuard website
    """
    name = 'newsguard'

    start_urls = ['https://www.newsguardtech.com/special-reports/coronavirus-misinformation-tracking-center/']

    def parse(self, response: scrapy.http.TextResponse, *args, **kwargs) -> None:
        """Extract the myths from the NewsGuard website, clean them, and write them to a file"""
        myths = response.xpath("//ol/li/strong/a/text()").extract()
        file_name = 'extracted_myths2.txt'
        print(myths)
        with open(file_name, 'w') as f:
            for myth in myths:
                myth = myth.replace('\xa0', '')
                myth = myth.replace('“', '')
                myth = myth.replace('”', '')
                myth = myth.replace('MYTH:', '')
                myth = myth.strip()
                f.write(myth + '\n')
