	"""
Nápověda:
Tento skript slouží ke stažení historických dat Forex z webu forexsb.com.

Potřebné nástroje:
    - selenium: Automatizace webového prohlížeče
    - requests: HTTP knihovna pro Python
    - webdriver_manager: Automatická správa chromedriveru
    - chromedriver: Webdriver pro Google Chrome
    - chromium-browser: Bezhlavý prohlížeč Chrome (pro Linux)

Instalace nástrojů:
    pip install selenium requests webdriver_manager

Použití:
  python3 forex_data_downloader.py -p MĚNOVÝ_PÁR -t ČASOVÝ_RÁMEC

Parametry:
  -p, --pair       Zadejte měnový pár ve formátu EURUSD (např. EURUSD, GBPUSD)
  -t, --timeframe  Zadejte časový rámec (M1, M5, M15, M30, H1, H4, D1 nebo All)

Příklady použití:
  Pro stažení dat měnového páru EUR/USD pro časový rámec M5:
    python3 forex_data_downloader.py -p EURUSD -t M5

  Pro stažení dat měnového páru EUR/USD pro všechny časové rámce:
    python3 forex_data_downloader.py -p EURUSD -t All    
"""

import os
import time
import requests
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

def download_forex_data(currency_pair, timeframe):
    # Nastavení headless režimu pro Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.binary_location = "/usr/bin/chromium-browser"

    # Použití ChromeDriverManager k automatickému stažení a nalezení chromedriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print("Navigating to the Forex historical data page...")
        driver.get("https://forexsb.com/historical-forex-data")

        # Kontrola, zda je stránka načtena správně
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("Page loaded.")

        # Přepnutí do iframe
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "data-app-frame"))
        )
        driver.switch_to.frame(iframe)
        print("Switched to iframe.")

        # Výběr měnového páru
        symbol_select = Select(WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "select-symbol"))
        ))
        symbol_select.select_by_value(currency_pair)
        print(f"Selected symbol: {currency_pair}")

        # Výběr formátu Forex Strategy Builder (CSV)
        format_select = Select(WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "select-format"))
        ))
        format_select.select_by_value("3")
        print("Selected format: 3")

        # Kliknutí na tlačítko Load Data
        load_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "btn-load-data"))
        )
        load_button.click()
        print("Clicked the Load Data button...")

        # Čekání na zobrazení odkazů ke stažení
        download_links = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.XPATH, f"//a[contains(text(), '{currency_pair}')]"))
        )
        print("Download links appeared.")

        # Stažení souborů
        timeframes = {
            "M1": f"{currency_pair}1.csv",
            "M5": f"{currency_pair}5.csv",
            "M15": f"{currency_pair}15.csv",
            "M30": f"{currency_pair}30.csv",
            "H1": f"{currency_pair}60.csv",
            "H4": f"{currency_pair}240.csv",
            "D1": f"{currency_pair}1440.csv"
        }

        if timeframe == "All":
            for filename in timeframes.values():
                download_link = driver.find_element(By.XPATH, f"//a[contains(text(), '{filename}')]").get_attribute("href")
                print(f"Downloading {filename} from {download_link}")
                response = requests.get(download_link)
                with open(filename, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded {filename}")
        else:
            filename = timeframes[timeframe]
            download_link = driver.find_element(By.XPATH, f"//a[contains(text(), '{filename}')]").get_attribute("href")
            print(f"Downloading {filename} from {download_link}")
            response = requests.get(download_link)
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Forex historical data")
    parser.add_argument('-p', '--pair', required=True, help="Měnový pár ve formátu EURUSD (např. EURUSD, GBPUSD)")
    parser.add_argument('-t', '--timeframe', required=True, help="Časový rámec (M1, M5, M15, M30, H1, H4, D1 nebo All)")
    args = parser.parse_args()

    download_forex_data(args.pair, args.timeframe)
