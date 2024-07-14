import requests
from bs4 import BeautifulSoup
import csv

def scrape_website(url):
    response = requests.get(url) # GET request to the URL
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        data = [p.text for p in paragraphs]
        return data
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Paragraph Text'])  # header
        for item in data:
            writer.writerow([item])

def ask_input():
  url = input("Enter the URL you want to scrape: ")
  return url

def main():
    url = str(ask_input())
    filename = "scraped_data.csv"
    
    print("Starting web scraping...")
    scraped_data = scrape_website(url)
    
    if scraped_data:
        save_to_csv(scraped_data, filename)
        print(f"Data successfully scraped and saved to {filename}")
    else:
        print("Scraping failed.")

if __name__ == "__main__":
    main()