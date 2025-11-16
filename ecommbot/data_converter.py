import pandas as pd
from langchain_core.documents import Document

product_data = pd.read_csv(r"/Users/saniyashinde/Documents/Projects/ecommerce_chatbot/data/flipkart_product.csv",
                           encoding="latin1")
print(product_data.head())
