import sqlite3
import csv
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import setup_logger

 
logger = setup_logger(__name__)

def load_car(csv_file, table_name, db_file):
    try:
        with open(csv_file, encoding='utf-8', errors='replace') as file:
            reader = csv.reader(file)
            next(reader)
            
            data = list(reader)
                
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            placeholder = ','.join(['?'] * len(data[0]))
            cursor.executemany(f'INSERT OR IGNORE INTO {table_name} VALUES ({placeholder})', data)
            conn.commit()
        
    except FileNotFoundError as fnf : logger.info(f'Wrong: {fnf}')
    except Exception as err : logger.info(f'Wrong :{err}')
    
