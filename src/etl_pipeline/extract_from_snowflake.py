# Determined input data: Constructor, Constructor_Engine, Circuit,  current_possition, current_lap, cumulative_previous_lap_times, last_pit_stop_lap 

# Prediction output: cumulative_position_gain_5_laps, net_race_time_change
import sys
import os
import pandas as pd


def get_constructors_data(conn):
    query = f"""SELECT * FROM constructors;"""
    constructors_data = pd.read_sql_query(query, conn)
    return constructors_data


def get_circuits_data(conn):
    query = f"""SELECT * FROM circuits;"""
    circuits_data = pd.read_sql_query(query, conn)
    return circuits_data


def get_lap_times_data(conn):
    query = f"""SELECT * FROM lap_times;"""
    lap_times_data = pd.read_sql_query(query, conn)
    return lap_times_data


def get_pit_stops_data(conn):
    query = f"""SELECT * FROM pit_stops;"""
    pit_stops_data = pd.read_sql_query(query, conn)
    return pit_stops_data


def get_races_data(conn):
    query = f"""SELECT * FROM races;"""
    races_data = pd.read_sql_query(query, conn)
    return races_data

conn = connect_to_snowflake()

query = f"""
SELECT * 
FROM CIRCUITS
LIMIT 10;
"""

data = pd.read_sql_query(query, conn)
print(data)

conn.close()
