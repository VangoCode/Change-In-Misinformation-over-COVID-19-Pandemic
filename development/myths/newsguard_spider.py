"""
Web scraping that gets a collection of COVID-19 myths from
https://www.newsguardtech.com/special-reports/coronavirus-misinformation-tracking-center/
using the scrapy library.

Copyright and Usage Information
==================================================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Ron Varshavsky and Elsie (Muhan) Zhu.
"""
import scrapy


class NewsGuardScraperSpider(scrapy.Spider):
    """A spider that scrapes the myths from the NewsGuard website"""
    name = 'newsguard'

    start_urls = ['https://www.newsguardtech.com/special-reports/coronavirus-misinformation-tracking-center/']

    def parse(self, response: scrapy.http.TextResponse, *args, **kwargs) -> None:
        """Extract the myths from the NewsGuard website, clean them, and write them to a file"""
        myths = response.xpath("//ol/li/strong/a/text()").extract()
        file_name = 'extracted_myths.txt'
        print(myths)
        with open(file_name, 'w') as f:
            for myth in myths:
                myth = myth.replace('\xa0', '')
                myth = myth.replace('“', '')
                myth = myth.replace('”', '')
                myth = myth.replace('‘', '')
                myth = myth.replace('’', '')
                myth = myth.replace('MYTH:', '')
                myth = myth.strip()
                f.write(myth + '\n')
