import pandas as pd
import sqlite3

df = pd.read_csv("data/cleaned_retail.csv")

conn = sqlite3.connect("data/retail.db")

df.to_sql("retail", conn, if_exists="replace", index=False)

print("Data loaded into SQLite")

df.columns = df.columns.str.replace(' ', '')