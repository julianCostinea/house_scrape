import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import Keys
import time

from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
browser = webdriver.Chrome(options=chrome_options)

try:
    # browser.get(
    #     "https://www.boligsiden.dk/tilsalg/villa?priceMax=1500000&priceMin=1200000&lotAreaMin=900&energyLabels=a,b,c&radius=35565|10.330817,55.357865")
    # print("Page title was '{}'".format(browser.title))

    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }

    # TODO: also get second page
    response = requests.get(
        "https://www.boligsiden.dk/tilsalg/villa?priceMax=1500000&priceMin=1200000&lotAreaMin=900&energyLabels=a,b,c&radius=35565|10.330817,55.357865&page=1",
        headers=header)
    data = response.text
    soup = BeautifulSoup(data, "html.parser")

    all_house_posts = soup.select(".overflow-hidden.mx-4.shadow-sm")
    #for each house post, find text inside selector font-black text-sm md:text-base whitespace-nowrap overflow-hidden text-ellipsis mr-2
    #only take first element in house_post
    all_house_posts = all_house_posts[:1]
    for house_post in all_house_posts:
        house_details = house_post.find("div", class_="font-black text-sm md:text-base whitespace-nowrap overflow-hidden text-ellipsis mr-2").contents
        house_street = house_details[0]
        house_city = house_details[1].text
        house_address = f"{house_street}, {house_city}"
        browser.get("https://kamp.klimatilpasning.dk/vandloeb/vandloebsoversvoemmelse?value=1")
        browser.maximize_window()
        time.sleep(5)
        # open_search_button = browser.find_element("id", "opensearch")
        # open_search_button.click()
        time.sleep(2)
        # deny_cookies_button = browser.find_element("id", "CybotCookiebotDialogBodyButtonDecline")
        # deny_cookies_button.click()
        # time.sleep(2)
        address_input = browser.find_element(By.CLASS_NAME, "ssInput")
        address_input.send_keys(house_address)
        time.sleep(2)
        address_input.send_keys(Keys.ENTER)
        time.sleep(5)
        zoom_out_button = browser.find_element(By.CLASS_NAME, "ol-zoom-out")
        zoom_out_button.click()
        zoom_out_button.click()
        zoom_out_button.click()
        zoom_out_button.click()
        zoom_out_button.click()
        zoom_out_button.click()
        time.sleep(7)
        basement_icons = browser.find_elements(By.CSS_SELECTOR, ".legend.building")
        with_basement_icon = basement_icons[0]
        without_basement_icon = basement_icons[1]
        #get sibling of without_basement_icon
        with_basement_text = with_basement_icon.find_element(By.XPATH, "following-sibling::*").text
        without_basement_text = without_basement_icon.find_element(By.XPATH, "following-sibling::*").text
        if "0 bygninger" not in with_basement_text.lower() or "0 bygninger" not in without_basement_text.lower():
            print(f"Risk of rain: {house_address}")
finally:
    browser.quit()
