import scrapy
from ..items import RealityItem

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# importing edited version of scrapy_selenium, as it is not compatible with selenium 4.17
from selenium_scraper.scrapy_selenium_ed import SeleniumRequest

import logging
logging.basicConfig(level=logging.INFO)
# logging.getLogger('scrapy').setLevel(logging.INFO)
# logging.getLogger('scrapy').propagate = False
logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
logger.setLevel(logging.WARNING)

class ScrapingClubSpider(scrapy.Spider):
    name = "seleniumspider"
    start_url = "https://www.sreality.cz/hledani/prodej/byty?strana="
    currect_url = ""
    entries_scraped = 0
    max_page = 2

    def start_requests(self):
        start_urls = []
        for i in range(1, self.max_page + 1):  # going through pages
            start_urls.append(self.start_url + str(i))
        logging.debug(start_urls)
        for start_url in start_urls:
            self.currect_url = start_url
            logging.debug(f"Request url: {start_url}")
            yield SeleniumRequest(url=start_url, callback=self.parse,
                                  wait_time=10,
                                  wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'title')),
                                  # screenshot=True,  # will work instead of wait
                                  )
    def parse(self, response):

        # to take a screenshot
        # with open(f'image{self.entries_scraped}.png', 'wb') as image_file:
        #     image_file.write(response.meta['screenshot'])

        reality_item = RealityItem()
        realities = response.css('div.property.ng-scope')
        for reality in realities:
            self.entries_scraped += 1
            reality_item['number'] = self.entries_scraped
            reality_item['title'] = reality.css('h2 a span ::text').get()
            reality_item['imgurl'] = reality.css('div a img ::attr(src)').get()
            yield reality_item

