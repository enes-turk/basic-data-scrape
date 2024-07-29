from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

website = "https://www.adamchoi.co.uk/overs/detailed"

# Specify the path to your ChromeDriver executable
chromedriver_path = r"wip\football-scraping\chromedriver-win64\chromedriver.exe"

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)
driver.get(website)

all_matches_button = driver.find_element(By.XPATH, "//label[@analytics-event='All matches']")
all_matches_button.click()

dropdown = Select(driver.find_element(By.ID, "country"))
dropdown.select_by_visible_text("Turkey")
time.sleep(2)  # Wait for the page to load

matches = driver.find_elements(By.TAG_NAME, "tr")

date = []
home_team = []
score = []
away_team = []

for match in matches:
    print(match.text)
    match_data = match.find_elements(By.TAG_NAME, "td")
    if len(match_data) >= 4:  # Ensure we have enough data
        date.append(match_data[0].text)
        home_team.append(match_data[1].text)
        score.append(match_data[2].text)
        away_team.append(match_data[3].text)

# create a DataFrame for these lists
df = pd.DataFrame({
    "Date": date,
    "Home Team": home_team,
    "Score": score,
    "Away Team": away_team
    })

df.to_csv("matches.csv", index=False)
print(df)

driver.quit()  # Don't forget to close the browser