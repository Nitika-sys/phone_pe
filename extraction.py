import pandas as pd
import json
import os

# Define the path to the data
path = "pulse/data/aggregated/transaction/country/india/state/"
state_list = os.listdir(path)

columns = {
    'State': [], 'Year': [], 'Quarter': [], 
    'Transaction_Type': [], 'Transaction_Count': [], 'Transaction_Amount': []
}

for state in state_list:
    cur_state = path + state + "/"
    year_list = os.listdir(cur_state)
    
    for year in year_list:
        cur_year = cur_state + year + "/"
        file_list = os.listdir(cur_year)
        
        for file in file_list:
            cur_file = cur_year + file
            with open(cur_file, 'r') as f:
                data = json.load(f)
                
                # Digging into the JSON structure
                for i in data['data']['transactionData']:
                    name = i['name']
                    count = i['paymentInstruments'][0]['count']
                    amount = i['paymentInstruments'][0]['amount']
                    
                    columns['State'].append(state.replace("-", " ").title())
                    columns['Year'].append(int(year))
                    columns['Quarter'].append(int(file.strip('.json')))
                    columns['Transaction_Type'].append(name)
                    columns['Transaction_Count'].append(count)
                    columns['Transaction_Amount'].append(amount)

# Create DataFrame
df_agg_trans = pd.DataFrame(columns)
print("Extraction Complete! Total Rows:", len(df_agg_trans))
print(df_agg_trans.head())

import sqlite3
from sqlalchemy import create_engine

# This will create a file named 'phonepe_data.db' in your folder
engine = create_engine('sqlite:///phonepe_data.db')

# Push your DataFrame to this local file
df_agg_trans.to_sql('aggregated_transaction', engine, if_exists='replace', index=False)

print("Data saved locally to phonepe_data.db!")