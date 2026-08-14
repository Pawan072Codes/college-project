import pandas as pd
from sqlalchemy import create_engine

# Step 1: read csv
df = pd.read_csv("data/data.csv", encoding="latin1")

# Step 2: rename columns to match our table (CamelCase -> snake_case)
df.columns = ["invoice_no", "stock_code", "description", "quantity",
              "invoice_date", "unit_price", "customer_id", "country"]

# Step 3: fix invoice_date format
df["invoice_date"] = pd.to_datetime(df["invoice_date"], format="%m/%d/%Y %H:%M")

# Step 4: connect to postgres (apna password daalo YOUR_PASSWORD ki jagah)
engine = create_engine("postgresql://postgres:Pawan%409873@localhost:5432/business_analytics")

# Step 5: push into table
df.to_sql("sales_raw", engine, if_exists="replace", index=False)

print("Data loaded successfully!")