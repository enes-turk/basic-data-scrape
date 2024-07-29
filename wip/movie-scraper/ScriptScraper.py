import os
from bs4 import BeautifulSoup
import requests
import sys

class ScriptScraper:
    def __init__(self):
        self.root = "https://www.subslikescript.com"
        self.website = f"{self.root}/movies"
        self.links = []
        self.start = 1
        self.end = 1
        self.pagination = self.get_pagination()

        # Create scripts directory if it doesn't exist
        try:
            if not os.path.exists("movie-scraper/scripts"):
                os.makedirs("movie-scraper/scripts")
        except OSError as e:
            print(f"Error creating directory: {e}")
            sys.exit(1)
    
    def get_links(self, start=None, end=None):
        start = start or self.start
        end = end or self.end
        
        for i in range(start, end + 1):
            try:
                soup = self.get_content(f"{self.website}?page={i}")
                box = soup.find("article", class_="main-article")

                if box:
                    for link in box.find_all("a", href=True):
                        self.links.append(link['href'])
                else:
                    print(f"Warning: No content found on page {i}")
            except Exception as e:
                print(f"Error processing page {i}: {e}")
    
    def get_script(self, link):
        try:
            soup = self.get_content(link)
            script = soup.find("div", class_="full-script")
            if script:
                return script.get_text(separator="\n")
            else:
                print(f"Warning: No script found at {link}")
                return ""
        except Exception as e:
            print(f"Error getting script from {link}: {e}")
            return ""
    
    def get_pagination(self):
        try:
            soup = self.get_content(self.website)
            pagination = soup.find("ul", class_="pagination")
            if pagination:
                pages = pagination.find_all("li", class_="page-item")
                last_page = pages[-2].text
                return int(last_page)
            else:
                print("Warning: No pagination found, defaulting to 1 page")
                return 1
        except Exception as e:
            print(f"Error getting pagination: {e}")
            return 1
        
    def get_content(self, url):
        try:
            result = requests.get(url)
            result.raise_for_status()  # Raises an HTTPError for bad responses
            return BeautifulSoup(result.text, "lxml")
        except requests.RequestException as e:
            print(f"Error fetching content from {url}: {e}")
            return BeautifulSoup("", "lxml")  # Return empty soup on error

    def save_script(self, script, title):
        try:
            title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            with open(f"movie-scraper/scripts/{title}.txt", "w", encoding="utf-8") as f:
                f.write(script)
        except IOError as e:
            print(f"Error saving script {title}: {e}")
  
    def run(self, start=None, end=None):
        print("Getting links...")
        self.get_links(start, end)
        
        print(f"Found {len(self.links)} links.")
        
        for i, link in enumerate(self.links, 1):
            print(f"Processing link {i}/{len(self.links)}: {link}")
            script = self.get_script(f"{self.root}{link}")
            title = link.split("/")[-1]
            self.save_script(script, title)
            print(f"Saved script: {title}")

def main():
    try:
        scraper = ScriptScraper()
        print(f"Detected {scraper.pagination} pages of content.")
        start = int(input("Enter the start page: "))
        end = int(input("Enter the end page: "))
        scraper.run(start, end)
    except ValueError as e:
        print(f"Invalid input: {e}. Please enter valid integers for start and end pages.")
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()