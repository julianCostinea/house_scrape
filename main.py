import smtplib
from email.message import EmailMessage
import os

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
import time
from dotenv import load_dotenv

from selenium.webdriver.common.by import By

load_dotenv()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
browser = webdriver.Chrome(options=chrome_options)
gmail_password = os.environ.get("GMAIL_PASSWORD")

try:
    # browser.get(
    #     "https://www.boligsiden.dk/tilsalg/villa?priceMax=1500000&priceMin=1200000&lotAreaMin=900&energyLabels=a,b,c&radius=35565|10.330817,55.357865")
    # print("Page title was '{}'".format(browser.title))

    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }

    # TODO: also get second page
    # response = requests.get(
    #     "https://www.edc.dk/soeg/?ejd-typer=1&g-areal=900&energi=a1,a2,a2010,a2015,a2020,b,c&pageNr=1&pris=1200000-1500000&expenses=0-2000&postnr=5000,5200,5210,5220,5230,5240,5250,5260,5270,5290,5300,5330,5350,5370,5380,5390,5400,5450,5462,5463,5464,5466,5471,5474,5485,5491,5492,5500,5540,5550,5560,5580,5591,5592,5600,5610,5620,5631,5642,5672,5683,5690,5700,5750,5762,5771,5772,5792,5800,5853,5854,5856,5863,5871,5874,5881,5882,5883,5884,5892&sort=26",
    #     headers=header)
    # data = response.text
    # soup = BeautifulSoup(data, "html.parser")

    with open('houses.txt', encoding='utf-8') as file:
        house_addresses = file.readlines()

    new_house_addresses = []

    browser.get("https://www.edc.dk/soeg/?ejd-typer=1&g-areal=900&energi=a1,a2,a2010,a2015,a2020,b,c&pageNr=1&pris=1200000-1500000&expenses=0-2000&postnr=5000,5200,5210,5220,5230,5240,5250,5260,5270,5290,5300,5330,5350,5370,5380,5390,5400,5450,5462,5463,5464,5466,5471,5474,5485,5491,5492,5500,5540,5550,5560,5580,5591,5592,5600,5610,5620,5631,5642,5672,5683,5690,5700,5750,5762,5771,5772,5792,5800,5853,5854,5856,5863,5871,5874,5881,5882,5883,5884,5892&sort=26")
    browser.maximize_window()
    time.sleep(5)
    all_house_posts = browser.find_elements(By.CSS_SELECTOR, "div[class='col-span-6 md:col-span-3']")

    # for each house post, find text inside selector font-black text-sm md:text-base whitespace-nowrap overflow-hidden text-ellipsis mr-2
    # only take first element in house_post

    # email setup
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    # Authentication
    s.login("julian.costinea@gmail.com", gmail_password)
    # Create a MIME text object
    msg = EmailMessage()
    msg['From'] = "julian.costinea@gmail.com"
    msg['To'] = "emil.costinea@gmail.com"

    for house_post in all_house_posts:
        house_details = house_post.find_element(By.CSS_SELECTOR, "address[class='contents not-italic']")
        house_link = house_post.find_element(By.TAG_NAME, "a").get_attribute("href")

        house_street = house_details.find_element(By.CSS_SELECTOR, "h3[class='col-span-2 col-start-1 row-start-1 mb-2 block overflow-hidden text-ellipsis whitespace-normal font-bold text-primary line-clamp-1']").get_attribute("innerText")
        house_city = house_details.find_element(By.CSS_SELECTOR, "span[class='col-span-1 col-start-1 row-start-2 block text-sm erhverv:text-business-pigeon-blue']").get_attribute("innerText")
        house_address = f"{house_street}, {house_city}"
        if house_address in house_addresses:
            continue

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
        time.sleep(2)
        zoom_out_button.click()
        time.sleep(2)
        zoom_out_button.click()
        time.sleep(2)
        zoom_out_button.click()
        time.sleep(2)
        zoom_out_button.click()
        time.sleep(5)
        collapse_button = browser.find_elements(By.CLASS_NAME, "collapse")
        collapse_button[1].click()
        time.sleep(9)
        basement_icons = browser.find_elements(By.CSS_SELECTOR, ".legend.building")
        with_basement_icon = basement_icons[0]
        without_basement_icon = basement_icons[1]
        # get sibling of without_basement_icon
        with_basement_text = with_basement_icon.find_element(By.XPATH, "following-sibling::*").text
        without_basement_text = without_basement_icon.find_element(By.XPATH, "following-sibling::*").text
        if "0 bygninger" in with_basement_text.lower() and "0 bygninger" in without_basement_text.lower() and house_address not in house_addresses:
            browser.get("https://bbr.dk/se-bbr-oplysninger/")
            time.sleep(5)
            try:
                decline_cookies_button = browser.find_element(By.CSS_SELECTOR, ".cpDontAcceptBtn")
                decline_cookies_button.click()
            except NoSuchElementException:
                pass
            time.sleep(2)
            address_input = browser.find_element(By.ID, "searchcomponent_input")
            address_input.send_keys(house_address)
            time.sleep(2)
            address_input.send_keys(Keys.ENTER)
            time.sleep(5)
            house_info = browser.find_element(By.CSS_SELECTOR, ".large-12.cell").text
            # check if house_info contains "herunder asbest"
            if "herunder asbest" not in house_info.lower():
                new_house_addresses.append(house_address)
                del msg['Subject']
                msg['Subject'] = f'New House found at {house_address}'
                msg.set_content(f"House found at\n https://www.edc.dk{house_link}")
                s.send_message(msg)

    with open('houses.txt', 'w', encoding='utf-8') as file:
        for house_address in new_house_addresses:
            file.write(f"{house_address}\n")

finally:
    s.quit()
    browser.quit()
