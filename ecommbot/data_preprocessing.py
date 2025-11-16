#%%
import pandas as pd
import numpy as np
import re
import unicodedata

#%%
pd.set_option("display.max_rows", None)

#%%
## Importing the data
product_data = pd.read_csv(r"/Users/saniyashinde/Documents/Projects/ecommerce_chatbot/data/flipkart_product.csv",
                           encoding="latin1")
print(product_data.head())

## Basic Data Cleaning
#%%
## checking the dataset columns and size of dataset
print(product_data.shape)
print(product_data.columns)
#%%
## checking for missing values in the dataset
missing_values = product_data.isnull().sum()
print(missing_values)
#%%
## Dropping rows where price  is null
product_data.dropna(subset=['Price'], inplace = True)
#%%
## Replacing products with empty summary as ""
product_data.fillna(" ", inplace=True)
#%%
## Checking for missing values again in the dataset
missing_values = product_data.isnull().sum()
print(missing_values)
#%%
## Text Preprocessing

## 1.) Cleaning the ProductName column

## Function to clean the ProductName Column

def clean_product_name(text):
    if pd.isna(text):
        return text

    # Normalize unicode (remove hidden/compatibility spaces)
    text = unicodedata.normalize("NFKC", text)

    # Remove trademark and special symbols
    text = re.sub(r"[®™★☆✓•●]", "", text)

    # Remove unwanted characters, keep only letters, numbers, spaces, (), /, and -
    text = re.sub(r'[^a-zA-Z0-9\s\(\)/-]', '', text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Inline abbreviation normalization (case-insensitive, word-boundary safe)
    abbrev_map = {
        "cm": "cm", "mm": "mm", "ml": "mL", "ltr": "L", "ltrs": "L",
        "lt": "L", "l": "L", "kg": "kg", "kgs": "kg", "gm": "g", "gms": "g",
        "w": "W", "kw": "kW", "mah": "mAh",
        "gb": "GB", "tb": "TB", "mbps": "Mbps",
        "pc": "pc", "pcs": "pcs", "pkt": "pack", "pkts": "packs", "nos": "pcs",
        "tv": "TV", "lcd": "LCD", "led": "LED", "dslr": "DSLR", "wifi": "WiFi",
        "uhd": "UHD", "hdr": "HDR", "bluetooth": "Bluetooth", "bt": "Bluetooth", "anc": "ANC",
        "inch" : "in", "centimetre" : "cm", "litre" : "L", "liter" : "L", "watt" : "W", "kilogram" : "kg"
    }

    for abbr, repl in abbrev_map.items():
        pattern = r"\b" + re.escape(abbr) + r"\b"
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    return text
#%%
product_data['ProductName'] = product_data['ProductName'].apply(clean_product_name)

#%%
print(product_data['ProductName'].head().to_string())
#%%
print(product_data['ProductName'].value_counts())

#%%

## 2.) Fixing Price column removing ??

def clean_price(price):
    if pd.isna(price):
        return np.nan
    # Remove non-digit characters except . and ,
    price = re.sub(r'[^\d.,]', '', str(price))
    
    # Replace comma with nothing (if used as thousand separator)
    price = price.replace(',', '')
    
    try:
        return float(price)
    except:
        return np.nan

# Apply the function
product_data['Price'] = product_data['Price'].apply(clean_price)

# Convert to int if you want
product_data['Price'] = product_data['Price'].astype(int)

#%%
print(product_data[['ProductName', 'Price']].head(10))

#%%

# 3.) Converting rate column to int
product_data['Rate'] = product_data['Rate'].astype(int)


#%%

## 4.) Cleaning the Summary column
