import time
import csv
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

# Scrape page with Selenium
def scrape():
    chrome_options = Options()
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(executable_path="/Users/dominic/chromedriver", options=chrome_options)
    browser.get("https://player.boom973.com/")

    play_button = browser.find_element_by_css_selector('.icon-play')
    play_button.click()

    print("Waiting...")

    WebDriverWait(browser, 5).until(
        lambda browser :
            browser.find_element_by_css_selector('#track-info-artist>span').text != "",
    )

    html = browser.page_source
    browser.close()

    return html

# Parse HTML with BS4
def parse_page():
    html = scrape()
    soup = BeautifulSoup(html, 'lxml')
    artist_name = soup.select_one('#track-info-artist>span').get_text()
    song_title = soup.select_one('#track-info-title>span').get_text()
    return artist_name, song_title

# Loop forever, appending new songs to CSV file
while True:
    filename = 'boom973-stats.csv'
    artist_name, song_title = parse_page()
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")

    print("Found song {} by {} at {}".format(song_title, artist_name, date_time))

    with open(filename, mode='a') as song_file:
        song_writer = csv.writer(song_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        song_writer.writerow([artist_name, song_title, date_time])

    time.sleep(240)
