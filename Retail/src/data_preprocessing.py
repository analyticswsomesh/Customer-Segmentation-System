import pandas as pd

df = pd.read_csv("data/online_retail_II.csv")

# Cleaning
df = df.dropna(subset=['Customer ID'])
df = df[df['Quantity'] > 0]
df = df[df['Price'] > 0]
df.columns = df.columns.str.replace(' ', '')
# Convert date
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Revenue column
df['Revenue'] = df['Quantity'] * df['Price']

df.to_csv("data/cleaned_retail.csv", index=False)

print("Cleaning done")
