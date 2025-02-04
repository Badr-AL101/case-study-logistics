import pandas as pd
import re
import json
import pymysql
from sqlalchemy import create_engine,text
from datetime import datetime

today = datetime.now().strftime("%Y%m%d")
with open(f'/usr/app/data/data_{today}.json', 'r') as f:
    data = json.load(f)

df = pd.json_normalize(data=data,sep="_")

def clean_column_names(cols):
    # prefix uppercase with underscore
    clean_cols = []
    for col in cols:
        new_st = ""
        for char in col:
            if char.isupper():
                char = "_" + char
            new_st += char
        clean_cols.append(new_st)
    clean_cols = [re.sub(r'__+', '_', col.lower().strip()) for col in clean_cols]
    return clean_cols
df.columns = clean_column_names(df.columns)

def list_to_string(lst):
    # Convert all items to string and then join them with a comma
    return ', '.join(str(item) for item in lst)
df['pickup_address_geo_location'] = df['pickup_address_geo_location'].apply(list_to_string)
df['dropoff_address_geo_location'] = df['dropoff_address_geo_location'].apply(list_to_string)

# Load to db

password_file = "/run/secrets/db_password"
with open(password_file,"r") as f:
     db_password = f.readline().strip()

# Database connection URL
DATABASE_URL = f"mysql+pymysql://user:{db_password}@logistics-etl-warehouse-1/logistics"

engine = create_engine(DATABASE_URL, echo=True)

df.to_sql('logistics_raw',engine,index=False,if_exists='replace')

with engine.connect() as connection:
    # Query to fetch the MySQL server version
    result = connection.execute(text("SELECT * FROM logistics_raw limit 5"))
    print(result)
