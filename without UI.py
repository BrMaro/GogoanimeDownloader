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
from selenium.webdriver.common.alert import Alert


domain = "https://gogoanime.dev"
PROJECT_PATH = "C:\\Users\\Techron\\PycharmProjects\\GogoanimeDownloader"
VIDEO_FILE_PATH = os.path.join(PROJECT_PATH,"Videos")
LINKS_FILE_PATH = os.path.join(PROJECT_PATH,"Links")
FILE_FORMAT = "mkv"


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


def get_option():
    while True:
        option = input(
            "Option 1. Download the videos\nOption 2. Get the download links\nChoice: ")
        print(f"Option {option} selected\n")
        if option == "2" or option == "1":
            break
        else:
            print("Invalid Option. Try again\n")
    return option


def get_html(link,ua):
    headers = {"User-Agent": ua}
    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


def get_episodes_to_download(episode_dict):
    while True:
        first_episode_input = int(input("Enter the first episode you want to download: "))
        last_episode_input = int(input("Enter the last episode you want to download: "))

        if 1 <= first_episode_input <= last_episode_input <= len(episode_dict):
            first_episode = first_episode_input
            last_episode = last_episode_input
            break
        else:
            print("Invalid input. Please enter valid episode numbers.")
    return first_episode,last_episode


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


def get_the_download_links(title,episode_dict,first_episode,last_episode):
    global driver
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


def download_the_episodes(title,episode_dict,first_episode,last_episode):
    global driver
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


def main():
    options = Options()
    options.add_argument("user-data-dir=C:\\Users\\Techron\\AppData\\Local\\Google\\Chrome\\User Data")
    driver = webdriver.Chrome(options=options)
    driver.get(domain)
    driver.implicitly_wait(10)
    alert_message = "Navigate to the main page of the anime and click 'Enter' on the console."
    Alert(driver).send_keys(alert_message)
    Alert(driver).accept()
    url = driver.current_url
    driver.quit()

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


    choice = get_option()
    first_episode,last_episode=get_episodes_to_download(episode_dict)

    if choice == "1":
        download_the_episodes(title,episode_dict,first_episode,last_episode)
    else:
        get_the_download_links(title,episode_dict,first_episode,last_episode)
