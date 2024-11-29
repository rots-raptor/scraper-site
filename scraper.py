import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

def download_image(url, folder, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(os.path.join(folder, filename), "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image saved: {filename}")
        else:
            print(f"Failed to download image: {url}")
    except Exception as e:
        print(f"Error: {e}")

def scrape_car_model(driver, city, car_model, base_folder):
    base_url = f"https://divar.ir/s/{city}"
    driver.get(base_url)
    print(f"Opened Divar for city: {city}")

    search_field_selector = "input.kt-nav-text-field__input"
    search_field = driver.find_element(By.CSS_SELECTOR, search_field_selector)
    search_field.send_keys(car_model)
    search_field.send_keys(Keys.RETURN)
    print(f"Searching for: {car_model}")
    time.sleep(5)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    car_ads = soup.find_all("div", class_="kt-post-card__body")
    print(f"Found {len(car_ads)} ads for {car_model}.")

    model_folder = os.path.join(base_folder, car_model)
    os.makedirs(model_folder, exist_ok=True)

    for i, ad in enumerate(car_ads[:200], start=1):
        img_tag = ad.find("img")
        if img_tag and "src" in img_tag.attrs:
            img_url = img_tag["src"]
            download_image(img_url, model_folder, f"image_{i}.jpg")

if __name__ == "__main__":
    # Configuration
    city = "tehran"
    car_models = ["206", "207", "405", "504", "Peride", "Samand LX", "Samand Soren", 
                  "Tara", "Dena", "Rana", "206 SD", "L90"]
    base_folder = "dataset"

    driver = webdriver.Chrome(options=options)

    try:
        for car_model in car_models:
            print(f"Scraping data for: {car_model}")
            scrape_car_model(driver, city, car_model, base_folder)
            print(f"Finished scraping for: {car_model}")

    finally:
        driver.quit()

    print("Scraping completed for all car models.")
