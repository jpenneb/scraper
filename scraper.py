import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

RESTAURANTS_AND_THEIR_URLS = { # TODO: Format as "restaurant name": {"location/zip code", "url"}, # TODO: Add all relevant urls (automate?)
    "Blue Bottle Coffee": "https://www.doordash.com/store/blue-bottle-coffee-los-angeles-2188529/",
    "Two Guns Espresso": "https://www.doordash.com/store/two-guns-espresso-manhattan-beach-24070363/",
    "Peet's Coffee": "https://www.doordash.com/store/peet's-coffee-el-segundo-912213/",
    "Philz Coffee": "https://www.doordash.com/store/philz-coffee-el-segundo-551463/",
    "The Coffee Bean & Tea Leaf": "https://www.doordash.com/store/the-coffee-bean-&-tea-leaf-manhattan-beach-501829/",
    "Panera Bread": "https://www.doordash.com/store/panera-bread-redondo-beach-873975/",
    "Gitana Cafe": "https://www.doordash.com/store/gitana-cafe-hermosa-beach-2670933/",
}
SECONDS_TO_WAIT_FOR_DRIVER = 180

def create_driver_for_python_to_communicate_with_web_browser_at(url):
    driver = webdriver.Safari()
    driver.get(url)
    driver = WebDriverWait(driver, SECONDS_TO_WAIT_FOR_DRIVER)
    return driver

def loop_through_categories_to_scrape_menu_items_and_their_corresponding_prices_and_write_to_csv(SECONDS_TO_WAIT_FOR_DRIVER, restaurant, categories):
    for category in categories:
        menu_items = category.find_elements(By.XPATH, '../following-sibling::div//div[@data-testid="GenericItemCard"]')
        for menu_item in menu_items:
            item = WebDriverWait(menu_item, SECONDS_TO_WAIT_FOR_DRIVER).until(EC.presence_of_element_located((By.XPATH, './/h3'))).text
            try:
                price = WebDriverWait(menu_item, SECONDS_TO_WAIT_FOR_DRIVER).until(EC.presence_of_all_elements_located((By.XPATH, './/span[@data-anchor-id="StoreMenuItemPrice"]'))).text
            except:
                continue

            with open("pricing.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([restaurant, category.text, item, price])

with open("pricing.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["location", "category", "item", "price"])

for restaurant, url in RESTAURANTS_AND_THEIR_URLS.items():
    driver = create_driver_for_python_to_communicate_with_web_browser_at(url)
    menu_categories = driver.until(EC.presence_of_all_elements_located((By.XPATH, '//h2[@data-category-scroll-selector]')))
    loop_through_categories_to_scrape_menu_items_and_their_corresponding_prices_and_write_to_csv(SECONDS_TO_WAIT_FOR_DRIVER, restaurant, menu_categories)
