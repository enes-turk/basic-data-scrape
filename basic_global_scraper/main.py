import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv


def scrape_website(url):
  response = requests.get(url)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    orders = []
    elements = []
    types = []
    contents = []
    
    for i, element in enumerate(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'])):
        tag_name = element.name
        
        element_type = 'header' if tag_name.startswith('h') else 'paragraph'
        
        elements.append(tag_name)
        types.append(element_type)
        contents.append(element.get_text(strip=True))
        orders.append(i + 1)
    
    df = pd.DataFrame({
        'Order': orders,
        'Element': elements,
        'Type': types,
        'Content': contents
    })
    
    return df
  else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    return None

def save_to_csv(data, filename):
  with open(f'scrapes/{filename}', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Element', 'Type', 'Content', 'Order'])  # headers
    for index, row in data.iterrows():
      writer.writerow(row)

def main():
  url = "https://www.nesine.com/iddaa?et=1&ocg=MS-2%2C5&gt=Pop%C3%BCler"  # Replace with the URL you want to scrape
  result = scrape_website(url)
  
  print("Starting web scraping...")
  scraped_data = scrape_website(url)
  
  if scraped_data is not None:
    filename = "scraped_data.csv"
    save_to_csv(scraped_data, filename)
    print(f"Data successfully scraped and saved to {filename}")
  else:
    print("Scraping failed.")

if __name__ == "__main__":
  main()