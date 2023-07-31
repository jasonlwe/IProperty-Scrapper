# Author: Pari Malam

import time
import os
from sys import stdout
import json
from selenium import webdriver
from colorama import Fore
import configparser
from lib.postgresdb import POSTGRESQL
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from undetected_chromedriver import Chrome, ChromeOptions

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

options = ChromeOptions()
options.add_argument("--headless")
driver = Chrome(options=options)

FY = Fore.YELLOW
FG = Fore.GREEN
FR = Fore.RED
FW = Fore.WHITE
FC = Fore.CYAN

def iproperty():
    os.system('clear' if os.name == 'posix' else 'cls')
    stdout.write("                                                                                         \n")
    stdout.write(""+Fore.LIGHTRED_EX +"██╗██████╗ ██████╗  ██████╗ ██████╗ ███████╗██████╗ ████████╗██╗   ██╗\n")
    stdout.write(""+Fore.LIGHTRED_EX +"██║██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝╚██╗ ██╔╝\n")
    stdout.write(""+Fore.LIGHTRED_EX +"██║██████╔╝██████╔╝██║   ██║██████╔╝█████╗  ██████╔╝   ██║    ╚████╔╝ \n")
    stdout.write(""+Fore.LIGHTRED_EX +"██║██╔═══╝ ██╔══██╗██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗   ██║     ╚██╔╝  \n")
    stdout.write(""+Fore.LIGHTRED_EX +"██║██║     ██║  ██║╚██████╔╝██║     ███████╗██║  ██║   ██║      ██║\n")
    stdout.write(""+Fore.LIGHTRED_EX +"╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝      ╚═╝\n")
    stdout.write(""+Fore.YELLOW +"═════════════╦═════════════════════════════════╦═══════════════════════════════\n")
    stdout.write(""+Fore.YELLOW   +"╔════════════╩═════════════════════════════════╩═════════════════════════════╗\n")
    stdout.write(""+Fore.YELLOW   +"║ \x1b[38;2;255;20;147m• "+Fore.GREEN+"DESCRIPTION     "+Fore.RED+"    |"+Fore.LIGHTWHITE_EX+"   AUTOMATED WEB SCRAPPING & CRAWLER                "+Fore.YELLOW+"║\n")
    stdout.write(""+Fore.YELLOW   +"╚════════════════════════════════════════════════════════════════════════════╝\n")
iproperty()

def dirdar():
    if not os.path.exists('Results'):
        os.mkdir('Results')
dirdar()

def scrape_page(page_url):
    driver.get(page_url)
    time.sleep(2)

    agent_listings = driver.find_elements(By.XPATH, '//div[@class="ListingHeadingstyle__HeadingLeftColumnWrapper-eumFS gcjzcO"]//div[@id="listing-heading-title"]')
    property_listings = driver.find_elements(By.CLASS_NAME, 'detail-property')
    property_descriptions = driver.find_elements(By.CSS_SELECTOR, '.PremiumCardstyle__BottomDescriptionWrapper-cJESFf.jNvtwR a.depth-listing-card-link')
    price_elements = driver.find_elements(By.CSS_SELECTOR, '.ListingPricestyle__ItemWrapper-etxdML.ejAiy')
    price_psf_elements = driver.find_elements(By.CSS_SELECTOR, '.ListingPricestyle__PricePSFWrapper-eraPyG p')

    min_length = min(len(property_listings), len(property_descriptions), len(agent_listings))

    properties_data = []

    for agent, listing, description, price_element, price_psf_element in zip(agent_listings[:min_length], property_listings[:min_length], property_descriptions[:min_length], price_elements[:min_length], price_psf_elements[:min_length]):
        link = description.get_attribute('href')
        agent_name = agent.text.strip()  # Extracting the agent name from the div

        title_element = listing.find_elements(By.CLASS_NAME, 'PremiumCardstyle__TitleWrapper-eqgGFm')
        property_title = title_element[0].text.strip() if title_element else "Title not found"

        address_element = listing.find_elements(By.CLASS_NAME, 'PremiumCardstyle__AddressWrapper-dFhRxY')
        address = address_element[0].text.strip() if address_element else "Location not found"

        attributes_element = listing.find_elements(By.CLASS_NAME, 'ListingAttributesstyle__ListingAttrsDescriptionItemWrapper-cCDpp')
        attributes = attributes_element[0].text.strip() if attributes_element else "Information not found"

        price = price_element.text.strip() if price_element else "Price not found"
        price_psf = price_psf_element.text.strip() if price_psf_element else "Price PSF not found"

        properties_data.append({
            "Datetime": time.strftime('%Y-%m-%d | %H:%M:%S'),
            "Agent Name": agent_name,
            "Title": property_title,
            "Location": address,
            "Price": price,
            "PSF": price_psf,
            "Information": attributes,
            "Details": link
        })

        print(Fore.WHITE + 'Datetime      :   ', Fore.RED + time.strftime('%Y-%m-%d | %H:%M:%S'))
        print(Fore.WHITE + 'Agent Name    :   ', Fore.GREEN + agent_name)
        print(Fore.WHITE + 'Title         :   ', Fore.GREEN + property_title)
        print(Fore.WHITE + 'Location      :   ', Fore.GREEN + address)
        print(Fore.WHITE + 'Price         :   ', Fore.GREEN + price, price_psf)
        print(Fore.WHITE + 'Information   :   ', Fore.GREEN + attributes)
        print(Fore.WHITE + 'Details       :   ', Fore.GREEN + link)
        print(Fore.CYAN + '.++====================================================================================================++.')

    return properties_data

def scrape_by_choice(state, choice):
    if choice == 1:
        base_url = f"https://www.iproperty.com.my/sale/{state}/all-residential/?l1&page="
        data_type = "Sale"
    elif choice == 2:
        base_url = f"https://www.iproperty.com.my/rent/{state}/all-residential/?l1&page="
        data_type = "Rent"
    else:
        print(f"{FR}Whut are you doin?")
        return

    all_properties_data = []

    for page_num in range(1, 20):
        page_url = base_url + str(page_num)
        print(Fore.GREEN + '\n[RUNNING] :', Fore.RED + '['+data_type + '] ' + Fore.GREEN + page_url + '\n')
        properties_data = scrape_page(page_url)
        all_properties_data.extend(properties_data)

    return all_properties_data

print(f"{FY}[1] - {FG}BUY (SALE)      {FY}[2] - {FG}RENT\n")
options = int(input(f"{FY}[CHOOSE]  : {FG}"))
state = input(f"{FY}[AREA]    : {FG}")
scraped_data = scrape_by_choice(state, options)

def insert_into_db(property_data):
    db = POSTGRESQL()
    for property_entry in property_data:
        sql = '''
            INSERT INTO property."IPROPERTY" ("AGENT_NAME", "TITLE", "DISTRICT", "PRICE", "PRICE_PSF", "DESC", "URL")
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        args = (
            property_entry["Agent Name"],
            property_entry["Title"],
            property_entry["Location"],
            property_entry["Price"],
            property_entry["PSF"],
            property_entry["Information"],
            property_entry["Details"]
        )
        db.execute(sql, args)
        db.commit()

    db.close()

insert_into_db(scraped_data)


output_file = f'Results/{state.lower()}_{options}.json'
with open(output_file, 'w') as json_file:
    json.dump(scraped_data, json_file, indent=4)

print(Fore.GREEN + '[SAVED]   : ', Fore.CYAN + 'Scraped data saved as JSON: ' + Fore.GREEN + output_file + '\n')

driver.quit()
