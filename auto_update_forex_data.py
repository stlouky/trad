import os
import time
import subprocess
import argparse
from datetime import timedelta

"""
Auto Update Forex Data

Tento skript automaticky stahuje Forex data v pravidelných intervalech pomocí skriptu forex_data_downloader.py.

Použití:
    python3 auto_update_forex_data.py -p EURUSD -t M5

Argumenty:
    -p, --pair      Měnový pár (např. EURUSD)
    -t, --timeframe Časový rámec (např. M5)

Podporované časové rámce:
    M1, M5, M15, M30, H1, H4, D1

Potřebné nástroje:
    - Python 3
    - Selenium
    - Requests
    - webdriver_manager
    - forex_data_downloader.py

Instalace potřebných nástrojů:
    pip install selenium requests webdriver_manager

Skript forex_data_downloader.py musí být ve stejné složce jako tento skript.
"""

def delete_existing_files(pair, timeframe):
    timeframes = {
        "M1": f"{pair}1.csv",
        "M5": f"{pair}5.csv",
        "M15": f"{pair}15.csv",
        "M30": f"{pair}30.csv",
        "H1": f"{pair}60.csv",
        "H4": f"{pair}240.csv",
        "D1": f"{pair}1440.csv"
    }
    filename = timeframes.get(timeframe, None)
    if filename and os.path.exists(filename):
        os.remove(filename)
        print(f"Deleted existing file: {filename}")

def countdown(seconds):
    for i in range(seconds, 0, -1):
        td = str(timedelta(seconds=i))
        print(f"Next update in {td}...", end='\r')
        time.sleep(1)

def auto_update_forex_data(pair, timeframe):
    while True:
        delete_existing_files(pair, timeframe)
        
        try:
            print(f"Starting data download for {pair} with timeframe {timeframe}...")
            # Volání skriptu pro stahování dat
            subprocess.run(["python3", "forex_data_downloader.py", "-p", pair, "-t", timeframe])
            print(f"Data for {pair} with timeframe {timeframe} downloaded successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Čekání podle časového rámce s dodatečnou 5sekundovou prodlevou
        if timeframe == "M1":
            countdown(1 * 60 + 5)
        elif timeframe == "M5":
            countdown(5 * 60 + 5)
        elif timeframe == "M15":
            countdown(15 * 60 + 5)
        elif timeframe == "M30":
            countdown(30 * 60 + 5)
        elif timeframe == "H1":
            countdown(60 * 60 + 5)
        elif timeframe == "H4":
            countdown(4 * 60 * 60 + 5)
        elif timeframe == "D1":
            countdown(24 * 60 * 60 + 5)
        else:
            print(f"Unsupported timeframe: {timeframe}")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto update Forex data")
    parser.add_argument("-p", "--pair", type=str, required=True, help="Měnový pár (např. EURUSD)")
    parser.add_argument("-t", "--timeframe", type=str, required=True, choices=["M1", "M5", "M15", "M30", "H1", "H4", "D1"], help="Časový rámec (např. M5)")

    args = parser.parse_args()

    auto_update_forex_data(args.pair, args.timeframe)
