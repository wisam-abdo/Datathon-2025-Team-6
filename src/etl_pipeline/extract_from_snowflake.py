import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.create_db_connection import connect_to_snowflake


def get_optimal_pit_stop_data(conn):
    query = f"""SELECT * FROM optimal_pit_stop_model limit 5500;"""
    opt_ps_data = pd.read_sql_query(query, conn)
    return opt_ps_data


def get_data():
    print("Establishing Connection...")
    conn = connect_to_snowflake()
    print("Retriving 'optimal_pit_stop_data' from the Database...")
    race_data = get_optimal_pit_stop_data(conn)
    return race_data
