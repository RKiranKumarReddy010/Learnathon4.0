##############################################################
#Project Name : BFSI
#File Name : _datecleaner.py
#Team Name : ThunderBolt
#Description : This will preprocess the datetime data 
##############################################################
import re
from datetime import datetime
import pandas as pd

class DateTimeCleaner:
    def parse_mixed_date(date_str):
        patterns = [
            (r'^\d{1,2}/\d{1,2}/\d{4}$', '%m/%d/%Y'),   
            (r'^\d{2}-\d{2}-\d{4}$', '%m-%d-%Y'),      
            (r'^\d{2}/\d{2}/\d{4}$', '%m/%d/%Y'),       
            (r'^\d{2}-\d{2}-\d{4}$', '%d-%m-%Y'),      
            (r'^\d{2}/\d{2}/\d{4}$', '%d/%m/%Y'),       
            (r'^\d{2}-\d{2}-\d{4}$', '%Y-%m-%d'),      
        ]
        for pattern, date_format in patterns:
            if re.match(pattern, date_str):
                try:
                    return datetime.strptime(date_str, date_format)
                except ValueError:
                    continue
        return None
    
    def merge_date_columns(data, col1_idx, col2_idx, new_col_name="Policy_Period"):
        new_data = []
        for row in data:
            merged = f"{row[col1_idx]} to {row[col2_idx]}"
            new_row = row + [merged]
            new_data.append(new_row)
        return new_data

    def merge_date_columns_by_index(data, col1_idx, col2_idx, new_col_name):
        col1 = data.columns[col1_idx]
        col2 = data.columns[col2_idx]
        data[col1] = pd.to_datetime(data[col1])
        data[col2] = pd.to_datetime(data[col2])
        data[new_col_name] = (data[col2] - data[col1]).dt.days

#################################################################
#Testing the functioanlity.
"""date_strings = [
    "08-12-2025", "4/15/2026", "4/24/2026", "3/17/2026",
    "11-01-2025", "12/16/2025", "03-09-2026", "10/30/2025",
    "06-11-2025", "11-12-2025", "11/26/2025"
]

parsed_dates = [DateTimeCleaner.parse_mixed_date(ds) for ds in date_strings]
print(parsed_dates)"""