import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess

class WorldometersSpider(scrapy.Spider):
    name = "worldometers"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]
    
    def __init__(self, *args, **kwargs):
        super(WorldometersSpider, self).__init__(*args, **kwargs)
        self.data = []

    def parse(self, response):
        countries = response.xpath("//td/a")

        for country in countries:
            country_name = country.xpath(".//text()").get()
            country_link = country.xpath(".//@href").get()

            yield response.follow(country_link, callback=self.parse_country, meta={'country_name': country_name})

    def parse_country(self, response):
        country_name = response.meta['country_name']
        rows = response.xpath("(//table[contains(@class, 'table-striped')])[1]/tbody/tr")
        
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            
            self.data.append({
                "country_name": country_name,
                "year": year,
                "population": population
            })

    def closed(self, reason):
        df = pd.DataFrame(self.data)
        df.to_csv('worldometers_population.csv', index=False)
        print(f"Data saved to worldometers_population.csv")

def run_spider():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

    process.crawl(WorldometersSpider)
    process.start()

if __name__ == "__main__":
    run_spider()