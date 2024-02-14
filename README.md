# scrapy-selenium and Docker
Using Scrapy with Selenium and Docker

## Overview

This project utilizes Scrapy with Selenium to scrape data from a real estate website (https://www.sreality.cz/). The scraped data is stored in a PostgreSQL database, and a simple Python server is included to display the scraped information on a web page. 

## How to Run

1. Clone the repository:

    ```bash
    git clone https://github.com/CasualMathEnjoyer/scrapy-selenium_docker.git
    ```
2. Run the project using Docker Compose:

    ```bash
    docker-compose up
    ```
3. Wait for the initialisation and scraping to be completed.
   - Initialisation is slow (about 30s on my computer), because of a healthcheck ensuring that the container running selenium/standalone-chrome is ready to accept connections.
5. Access the scraped data via a simple Python server. Open your web browser and navigate to http://localhost:8080.

## Configurations
1. Set up your Selenium configurations in `setting.py`.

    ```python
    SELENIUM_DRIVER_NAME = 'chrome'
    SELENIUM_COMMAND_EXECUTOR = "http://selenium:4444/wd/hub"
    SELENIUM_DRIVER_ARGUMENTS = ['--headless']
    ```

2. Change parameters of the SeleniumRequest in `seleniumspider.py`:

    ```python
    yield SeleniumRequest(
        url=start_url,
        callback=self.parse,
        wait_time=10,
        wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'title')),
    )
    ```

    Adjust the `wait_time` and `wait_until` parameters based on your needs.
3. Set the number of pages to be scraped:
   ```python
    class SeleniumSpider(scrapy.Spider):
        name = "seleniumspider"
        start_url = "https://www.sreality.cz/hledani/prodej/byty?strana="
        currect_url = ""
        entries_scraped = 0
        max_page = 2  # here
    ```

## Changes to the scrapy-selenium package in `scrapy_selenium_ed/middlewares.py`:

```python
# Remote driver configuration
elif command_executor is not None:
    from selenium import webdriver
    capabilities = driver_options.to_capabilities()
    self.driver = webdriver.Remote(
        command_executor=command_executor,
        options=driver_options,  # added driver_options
        # desired_capabilities=capabilities  # removed capabilities
    )
```

## Sources and inspiration:

- https://www.zenrows.com/blog/scrapy-selenium#can-i-use-selenium-with-scrapy
- https://stackoverflow.com/questions/31746182/docker-compose-wait-for-container-x-before-starting-y
- https://github.com/clemfromspace/scrapy-selenium
