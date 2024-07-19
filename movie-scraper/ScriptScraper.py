import os
from bs4 import BeautifulSoup
import requests

class ScriptScrapper:
    def __init__(self):
        self.root = "https://www.subslikescript.com"
        self.website = f"{self.root}/movies"
        self.links = []

        # Create scripts directory if it doesn't exist
        if not os.path.exists("scripts"):
            os.makedirs("scripts")
    
    def get_links(self):
        result = requests.get(self.website)
        content = result.content
        soup = BeautifulSoup(content, "lxml")

        box = soup.find("article", class_="main-article")

        for link in box.find_all("a", href=True):
            self.links.append(link['href'])
    
    def get_script(self, link):
        result = requests.get(link)
        content = result.content
        soup = BeautifulSoup(content, "lxml")

        # Assuming the script is within a "div" with the class "full-script"
        script = soup.find("div", class_="full-script")
        if script:
            script = script.get_text(separator="\n")
        else:
            script = ""
        
        return script
  
    def save_script(self, script, title):
        with open(f"scripts/{title}.txt", "w", encoding="utf-8") as f:
            f.write(script)
  
    def run(self):
        self.get_links()

        for link in self.links:
            script = self.get_script(f"{self.root}{link}")
            title = link.split("/")[-1]
            self.save_script(script, title)
  
if __name__ == "__main__":
    scrapper = ScriptScrapper()
    scrapper.run()
