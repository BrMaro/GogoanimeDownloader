import time
import os
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import random
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import keyboard

domain = "https://gogoanime.dev"
PROJECT_PATH = "C:\\Users\\Techron\\PycharmProjects\\GogoanimeDownloader"
# options = Options()
# options.add_argument("--headless")
# # options.add_argument(f'user-agent={ua}')
# options.add_argument("--window-size=1920,1080")
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--allow-running-insecure-content')
# options.add_argument("--disable-extensions")
# options.add_argument("--proxy-server='direct://'")
# options.add_argument("--proxy-bypass-list=*")
# options.add_argument("--start-maximized")
# options.add_argument('--disable-gpu')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--no-sandbox')
options = Options()
options.add_argument("user-data-dir=C:\\Users\\Techron\\AppData\\Local\\Google\\Chrome\\User Data")
driver = webdriver.Chrome(options=options)
driver.get(domain)
input("We are opening the website for you.\n Navigate to the main page of the anime and click 'Enter' key.\n\n;")
url = driver.current_url
driver.quit()




def get_ua():
    uastrings = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"
        ]

    return random.choice(uastrings)


def get_html(link):
    headers = {"User-Agent": ua}
    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


ua = get_ua()
soup = get_html(url)
title = soup.title
print(title.text)

ul_element = soup.find('ul', id='episode_related')
episode_links = ul_element.find_all('a')
episode_links = [domain + (link['href']) for link in episode_links]
episode_number_list = ul_element.find_all(class_='name')
episode_number_list = [float(episode.text.replace("EP ", "")) for episode in episode_number_list]

# Create a dictionary mapping episode numbers to episode links
episode_dict = {k: v for k, v in zip(episode_number_list, episode_links)}

first_episode = 1
last_episode = len(episode_dict)

while True:
    first_episode_input = int(input("Enter the first episode you want to download: "))
    last_episode_input = int(input("Enter the last episode you want to download: "))

    if 1 <= first_episode_input <= last_episode_input <= len(episode_dict):
        first_episode = first_episode_input
        last_episode = last_episode_input
        break
    else:
        print("Invalid input. Please enter valid episode numbers.")

driver = webdriver.Chrome(options=options)
for episode in range(first_episode, last_episode + 1):
    soup = get_html(episode_dict[episode])
    download_button = soup.find('li', class_='dowloads')
    download_link = download_button.find('a')
    #print(download_link['href'])

    driver.get(download_link['href'])
    driver.implicitly_wait(10)
    time.sleep(5)
    download_link2 = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Download') and contains(text(), '480')]")))
    with open(f'{title.text.replace(" Watch on GogoAnime Official Website","")}  links.txt', 'a') as file:
        print(download_link2.get_attribute('href'))
        file.write(download_link2.get_attribute('href'))
        file.write('\n')
