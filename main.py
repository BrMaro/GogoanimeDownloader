from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions
from selenium.common.exceptions import TimeoutException
import time

# def ad_detection():
#     for window in all_windows:
#         driver.switch_to.window(window)
#         if window != main_window:
#             driver.close()
driver = webdriver.Chrome()
url = "https://gogoanime.dev/"
driver.get(url)
driver.implicitly_wait(10)

input("Please navigate to the desired anime and press Enter to continue...")
current_url = driver.current_url
print("Current URL:", current_url)

ul_element = driver.find_element(By.ID,"episode_related")
episode_links = ul_element.find_elements(By.TAG_NAME,"a")
episode_number_list = ul_element.find_elements(By.CLASS_NAME,"name")
episode_number_list = [float(episode.text.replace("EP ","")) for episode in episode_number_list]
episode_dict = {k: v for k, v in zip(episode_number_list,episode_links)}


status = driver.find_elements(By.CLASS_NAME,"type")
anime_title = driver.find_element(By.TAG_NAME,"h1").text.capitalize()
print(f"{anime_title}\n Episodes: {len(episode_number_list)}\n Status: {status[4].text}")

first_episode = int(input("Enter the first episode you want to download:"))
last_episode = int(input("Enter the last episode you want to download:"))
max_load_time = 10

for episode in range(first_episode, last_episode+1):
    link = episode_dict[episode]
    href = link.get_attribute('href')
    if href and not href.startswith('javascript:'):
        driver.execute_script("window.open('" + href + "', '_blank');")
        try:
            wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
            if driver.execute_script("return document.readyState") != "complete":
                raise TimeoutException
        except TimeoutException:
            driver.stop_client()

        window_handles = driver.window_handles
        driver.switch_to.window(driver.window_handles[-1])
        main_window = driver.current_window_handle

        dowloads_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "dowloads")))
        dowloads_element.click()
        all_windows = driver.window_handles



        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)
        wait = WebDriverWait(driver, 20)
        download_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Download') and contains(text(), '480')]")))
        driver.execute_script("arguments[0].click();",download_link)
        driver.close()

        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])


    print(f"Episode {episode} downloading")