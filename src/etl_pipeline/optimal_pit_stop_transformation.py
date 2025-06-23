# Determined input data: Constructor, Circuit,  current_possition, current_lap, cumulative_previous_lap_times, last_pit_stop_lap 

# Prediction output: cumulative_position_gain_5_laps, net_race_time_change

import os
import sys
from extract_from_snowflake import get_optimal_pit_stop_data
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.create_db_connection import connect_to_snowflake


def get_data():
    print("Establishing Connection...")
    conn = connect_to_snowflake()
    print("Retriving 'optimal_pit_stop_data' from the Database...")
    race_data = get_optimal_pit_stop_data(conn)
    return race_data

def calc_avg_previous_laps(race_data, pit_stop_rows):
    avg_prev_laps = pit_stop_rows.copy()
    avg_times = []

    for index, row in pit_stop_rows.iterrows():
        race_id = row["RACEID"]
        constructor_id = row["CONSTRUCTORID"]
        circuit_id = row["CIRCUITID"]
        pit_stop_lap = row["CURRENT_LAP"]

        conditions = (race_data["RACEID"] == race_id) & \
        (race_data["CONSTRUCTORID"] == constructor_id) & \
        (race_data["CIRCUITID"] == circuit_id) & \
        (race_data["CURRENT_LAP"] < pit_stop_lap) & \
        (race_data["CURRENT_LAP"] >= pit_stop_lap - 5)

        previous_laps = race_data[conditions].sort_values("CURRENT_LAP")

        if len(previous_laps) > 0:
            avg_time = previous_laps["LAP_TIME_MILLISECONDS"].mean()
        else:
            avg_time = None
        
        avg_times.append(avg_time)

    avg_prev_laps["AVG_PREVIOUS_LAPS"] = avg_times
    return avg_prev_laps


def calc_positional_change(race_data, pit_stop_rows):
    positional_change = pit_stop_rows.copy()
    positional_change["TARGET_LAP"] = positional_change["CURRENT_LAP"] + 5

    merged_data = race_data[["RACEID", "DRIVERID", "CIRCUITID", "CONSTRUCTORID", "CURRENT_LAP", "POSITION"]].rename(columns={"CURRENT_LAP": "TARGET_LAP", "POSITION": "NEW_POSITION"})

    positional_change = positional_change.merge(merged_data,
                                                on = ["RACEID", "DRIVERID", "CIRCUITID", "CONSTRUCTORID", "TARGET_LAP"],
                                                how = "left")
    
    pit_stop_rows = positional_change.drop("TARGET_LAP", axis = 1)
    pit_stop_rows["NEW_POSITION"] = pit_stop_rows["NEW_POSITION"].fillna(pit_stop_rows["POSITION"])
    return pit_stop_rows


def calc_avg_future_laps(race_data, pit_stop_rows):
    


def format_data(race_data):
    print("Begining data reformatting...")
    pit_stop_rows = race_data.copy()
    print("Name Column dropped!")
    pit_stop_rows = pit_stop_rows.drop("NAME", axis=1)
    print("Rows in which a pitstop occurs pulled!")
    pit_stop_rows = pit_stop_rows[~pit_stop_rows["STOP"].isnull()]
    print("Values converted to float type")
    pit_stop_rows.astype(float)
    print("Ensuring data has a five pitstop")
    previous_row = pit_stop_rows.shift(-1)
    # Conditionals created to evaluate the same driver's race pit_stops and not pitstops across different races/drivers.
    conditionals = (pit_stop_rows["CURRENT_LAP"] - previous_row["CURRENT_LAP"] >= 5) | \
    ((pit_stop_rows['RACEID'] == previous_row['RACEID']) & \
     (pit_stop_rows['CIRCUITID'] == previous_row['CIRCUITID']) & \
     (pit_stop_rows['CONSTRUCTORID'] == previous_row['CONSTRUCTORID']))
    
    pit_stop_rows = pit_stop_rows[conditionals]
    
    pit_stop_rows = calc_avg_previous_laps(race_data, pit_stop_rows)

    pit_stop_rows = calc_positional_change(race_data, pit_stop_rows)

    return pit_stop_rows

    
if __name__ == "__main__":
    data = get_data()
    print(format_data(data))
