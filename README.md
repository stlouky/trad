# Forex Data Downloader and Auto Update

Tento projekt obsahuje dva Python skripty pro automatické stahování a aktualizaci Forex dat.

## Skripty

### forex_data_downloader.py

Tento skript stahuje historická Forex data pro zadaný měnový pár a časový rámec.

#### Použití:
```bash
python3 forex_data_downloader.py -p EURUSD -t M5
```

#### Argumenty:

- `-p, --pair`      Měnový pár (např. EURUSD)
- `-t, --timeframe` Časový rámec (např. M5)

#### Podporované časové rámce:

- M1, M5, M15, M30, H1, H4, D1

#### Potřebné nástroje:

- Python 3
- Selenium
- Requests
- webdriver_manager

#### Instalace potřebných nástrojů:
```bash
pip install selenium requests webdriver_manager
```

### auto_update_forex_data.py

Tento skript automaticky stahuje Forex data v pravidelných intervalech pomocí skriptu `forex_data_downloader.py`.

#### Použití:
```bash
python3 auto_update_forex_data.py -p EURUSD -t M5
```

#### Argumenty:

- `-p, --pair`      Měnový pár (např. EURUSD)
- `-t, --timeframe` Časový rámec (např. M5)

#### Podporované časové rámce:

- M1, M5, M15, M30, H1, H4, D1

#### Potřebné nástroje:

- Python 3
- Selenium
- Requests
- webdriver_manager
- forex_data_downloader.py

#### Instalace potřebných nástrojů:
```bash
pip install selenium requests webdriver_manager
```

## Příklad použití

### Stahování dat:
```bash
python3 forex_data_downloader.py -p EURUSD -t M5
```

### Automatická aktualizace dat:
```bash
python3 auto_update_forex_data.py -p EURUSD -t M5
```

Skript `auto_update_forex_data.py` bude každých 5 minut + 5 sekund stahovat nová data a nahrazovat stará data. Tento interval se liší podle zadaného časového rámce.

## Poznámky

- Skript `forex_data_downloader.py` musí být ve stejné složce jako `auto_update_forex_data.py`.
- Skripty předpokládají, že máte nainstalovaný prohlížeč Chrome a že je dostupný pro `chromedriver`.

Tento projekt vám pomůže udržovat aktuální historická Forex data pro analýzu a backtesting vašich obchodních strategií.
