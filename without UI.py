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
VIDEO_FILE_PATH = os.path.join(PROJECT_PATH,"Videos")
LINKS_FILE_PATH = os.path.join(PROJECT_PATH,"Links")
FILE_FORMAT = "mkv"



options = Options()
options.add_argument("user-data-dir=C:\\Users\\Techron\\AppData\\Local\\Google\\Chrome\\User Data")
driver = webdriver.Chrome(options=options)
driver.get(domain)
input("We are opening the website for you.\n Navigate to the main page of the anime and click 'Enter' key.\n\n")
url = driver.current_url
driver.quit()

while True:
    option = input("Option 1. Download the videos\nOption 2. Download the download links for porting to Free Download manager\n")
    print(f"Option {option} selected\n")
    if option == "2" or option == "1":
        break
    else:
        print("Invalid Option. Try again\n")

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


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created successfully.")
    else:
        print(f"Folder '{folder_name}' already exists. Skipping creation.")



def download_video(vidUrl, filepath):
    try:
        response = requests.get(vidUrl, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'wb') as file, tqdm(
                desc=os.path.basename(filepath),
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    file.write(chunk)
                    bar.update(len(chunk))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


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


def get_the_download_links():
    anime_title = title.text.replace(" Watch on GogoAnime Official Website", "")
    specific_anime_folder = os.path.join(VIDEO_FILE_PATH, anime_title)
    create_folder(specific_anime_folder)
    for episode in range(first_episode, last_episode + 1):
        soup = get_html(episode_dict[episode])
        download_button = soup.find('li', class_='dowloads')
        download_link = download_button.find('a')
        driver.get(download_link['href'])
        driver.implicitly_wait(10)
        time.sleep(5)
        download_link2 = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Download') and contains(text(), '480')]")))
        with open(f'{title.text.replace(" Watch on GogoAnime Official Website","")}  links.txt', 'a') as file:
            print(download_link2.get_attribute('href'))
            file.write(download_link2.get_attribute('href'))
            file.write('\n')


def download_the_episodes():
    anime_title = title.text.replace(" Watch on GogoAnime Official Website","")
    specific_anime_folder = os.path.join(VIDEO_FILE_PATH,anime_title)
    create_folder(specific_anime_folder)
    for episode in range(first_episode, last_episode + 1):
        soup = get_html(episode_dict[episode])
        download_button = soup.find('li', class_='dowloads')
        download_link = download_button.find('a')
        driver.get(download_link['href'])
        driver.implicitly_wait(10)
        time.sleep(5)
        download_link2 = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Download') and contains(text(), '480')]")))
        print(download_link2.get_attribute('href'))
        download_video(download_link2.get_attribute('href'),(os.path.join(specific_anime_folder,f"EP {episode}.{FILE_FORMAT}")))

download_the_episodes()
