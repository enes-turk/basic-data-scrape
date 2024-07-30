import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd

class AudibleScraper:
    def __init__(self, url, driver_path):
        self.url = url
        self.driver_path = driver_path
        self.driver = None
        self.books = []

    def setup_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
        options.add_argument('--log-level=3')
        service = Service(executable_path=self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)

    def get_last_page(self):
        pagination = self.driver.find_element(By.XPATH, ".//ul[contains(@class, 'pagingElements')]")
        pages = pagination.find_elements(By.XPATH, ".//li")
        return int(pages[-2].text)

    def scrape_page(self):
        try:
            container = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "adbl-impression-container"))
            )
            products = WebDriverWait(container, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, ".//li[contains(@class, 'productListItem')]"))
            )

            for product in products:
                book = self.extract_book_info(product)
                self.books.append(book)
                print(f"Scraping: {book['Title']}")

        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Error scraping page: {str(e)}")

    def extract_book_info(self, product):
        return {
            "Title": product.find_element(By.XPATH, ".//h3[contains(@class, 'bc-heading')]").text,
            "Author": product.find_element(By.XPATH, ".//li[contains(@class, 'authorLabel')]").text,
            "Length": product.find_element(By.XPATH, ".//li[contains(@class, 'runtimeLabel')]").text,
            "Link": product.find_element(By.XPATH, ".//a").get_attribute("href")
        }

    def go_to_next_page(self):
        try:
            next_page = self.driver.find_element(By.XPATH, ".//span[contains(@class, 'nextButton')]")
            next_page.click()
            return True
        except NoSuchElementException:
            print("No more pages to scrape.")
            return False

    def scrape(self):
        self.setup_driver()
        self.driver.get(self.url)

        last_page = self.get_last_page()
        current_page = 1

        while current_page <= last_page:
            self.scrape_page()
            if not self.go_to_next_page():
                break
            current_page += 1

        self.driver.quit()

    def save_to_csv(self, filename):
        df = pd.DataFrame(self.books)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

def main():
    # Set up logging
    logging.basicConfig(level=logging.WARNING)
    selenium_logger = logging.getLogger('selenium')
    selenium_logger.setLevel(logging.WARNING)

    # Initialize and run the scraper
    url = "https://www.audible.com/search"
    driver_path = r"wip\chromedriver-win64\chromedriver.exe"
    scraper = AudibleScraper(url, driver_path)
    scraper.scrape()
    scraper.save_to_csv("audible_books.csv")

if __name__ == "__main__":
    main()