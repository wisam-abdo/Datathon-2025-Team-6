import pandas as pd


def get_optimal_pit_stop_data(conn):
    query = f"""SELECT * FROM optimal_pit_stop_model limit 1000;"""
    opt_ps_data = pd.read_sql_query(query, conn)
    return opt_ps_data
