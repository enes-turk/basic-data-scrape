import requests
from bs4 import BeautifulSoup
import csv
from time import sleep

def scrape_wikipedia(url):
    # Send a GET request to the URL
    headers = {
        'User-Agent': 'WikipediaScraper/1.0 (https://example.com/my-scraper; scraper@example.com)'
    }
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title = soup.find(id="firstHeading").text.strip()
        
        # Extract main content
        content = soup.find(id="mw-content-text")
        
        # Extract paragraphs
        paragraphs = [p.text.strip() for p in content.find_all('p') if p.text.strip()]
        
        # Extract section headers
        headers = [h.text.strip() for h in content.find_all(['h2', 'h3', 'h4', 'h5', 'h6'])]
        
        # Extract references
        references = [ref.text.strip() for ref in soup.find_all('ol', class_='references') if ref.text.strip()]
        
        return {
            'title': title,
            'paragraphs': paragraphs,
            'headers': headers,
            'references': references
        }
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Type', 'Content'])  # Header
        writer.writerow(['Title', data['title']])
        for paragraph in data['paragraphs']:
            writer.writerow(['Paragraph', paragraph])
        for header in data['headers']:
            writer.writerow(['Section Header', header])
        for reference in data['references']:
            writer.writerow(['Reference', reference])

def main():
    base_url = "https://en.wikipedia.org/wiki/"
    topic = "Artificial_intelligence"  # Replace with the topic you want to scrape
    url = base_url + topic
    filename = f"{topic}_data.csv"
    
    print(f"Starting Wikipedia scraping for: {topic}")
    scraped_data = scrape_wikipedia(url)
    
    if scraped_data:
        save_to_csv(scraped_data, filename)
        print(f"Data successfully scraped and saved to {filename}")
    else:
        print("Scraping failed.")
    
    # Be polite and don't hammer the server
    sleep(1)

if __name__ == "__main__":
    main()