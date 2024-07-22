from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

website = "https://www.adamchoi.co.uk/overs/detailed"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(website)

all_matches_button = driver.find_element(By.XPATH, "//label[@analytics-event='All matches']")
all_matches_button.click()
# find element by tag name
matches = all_matches_button = driver.find_elements(By.TAG_NAME, "tr")

date = []
home_team = []
score = []
away_team = []

for match in matches:
    match_data = match.find_elements(By.TAG_NAME, "td")
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

print(df)




