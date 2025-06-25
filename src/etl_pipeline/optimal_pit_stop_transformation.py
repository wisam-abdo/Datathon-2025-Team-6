import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from etl_pipeline.extract_from_snowflake import get_data

def calc_avg_previous_laps(race_data, pit_stop_rows):
    avg_prev_laps = pit_stop_rows.copy()
    avg_times = []

    for index, row in pit_stop_rows.iterrows():
        race_id = row["RACEID"]
        constructor_id = row["CONSTRUCTORID"]
        circuit_id = row["CIRCUITID"]
        driver_id = row["DRIVERID"]
        pit_stop_lap = row["CURRENT_LAP"]

        conditions = (race_data["RACEID"] == race_id) & \
        (race_data["CONSTRUCTORID"] == constructor_id) & \
        (race_data["CIRCUITID"] == circuit_id) & \
        (race_data["DRIVERID"] == driver_id) & \
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
    formatted_race_data = race_data.copy()
    formatted_race_data["LAP_TIME_MILLISECONDS"] -= formatted_race_data["PIT_STOP_DURATION"].fillna(0)

    avg_fut_laps = pit_stop_rows.copy()
    avg_times = []

    for index, row in pit_stop_rows.iterrows():
        race_id = row["RACEID"]
        constructor_id = row["CONSTRUCTORID"]
        circuit_id = row["CIRCUITID"]
        driver_id = row["DRIVERID"]
        pit_stop_lap = row["CURRENT_LAP"]

        conditions = (race_data["RACEID"] == race_id) & \
        (formatted_race_data["CONSTRUCTORID"] == constructor_id) & \
        (formatted_race_data["CIRCUITID"] == circuit_id) & \
        (formatted_race_data["DRIVERID"] == driver_id) & \
        (formatted_race_data["CURRENT_LAP"] >= pit_stop_lap) & \
        (formatted_race_data["CURRENT_LAP"] < pit_stop_lap + 5)

        previous_laps = formatted_race_data[conditions].sort_values("CURRENT_LAP")

        if len(previous_laps) > 0:
            avg_time = previous_laps["LAP_TIME_MILLISECONDS"].mean()
        else:
            avg_time = None
        
        avg_times.append(avg_time)

    avg_fut_laps["AVG_FUTURE_LAPS"] = avg_times
    return avg_fut_laps


def format_data(race_data):
    print("Name Column dropped!")
    race_data = race_data.drop("NAME", axis=1)
    print("Values converted to float type")
    race_data.astype(float)
    print("Begining data reformatting...")
    pit_stop_rows = race_data.copy()
    print("Rows in which a pitstop occurs pulled!")
    pit_stop_rows = pit_stop_rows[~pit_stop_rows["STOP"].isnull()]
    print("Ensuring data has a five pitstop")
    previous_row = pit_stop_rows.shift(-1)
    # Conditionals created to evaluate the same driver's race pit_stops and not pitstops across different races/drivers.
    conditionals = (pit_stop_rows["CURRENT_LAP"] - previous_row["CURRENT_LAP"] >= 5) | \
    ((pit_stop_rows['RACEID'] == previous_row['RACEID']) & \
     (pit_stop_rows['CIRCUITID'] == previous_row['CIRCUITID']) & \
     (pit_stop_rows['CONSTRUCTORID'] == previous_row['CONSTRUCTORID']))
    
    pit_stop_rows = pit_stop_rows[conditionals]
    
    pit_stop_rows = calc_avg_previous_laps(race_data, pit_stop_rows)
    pit_stop_rows.dropna(subset=['AVG_PREVIOUS_LAPS'], inplace=True)
    pit_stop_rows = calc_positional_change(race_data, pit_stop_rows)
    pit_stop_rows = calc_avg_future_laps(race_data, pit_stop_rows)
    pit_stop_rows.dropna(subset=['AVG_FUTURE_LAPS'], inplace=True)

    pit_stop_rows = pit_stop_rows.drop(["PIT_STOP_DURATION", "STOP"], axis=1)

    unique_races = pit_stop_rows['RACEID'].unique()
    split = max(1, int(len(unique_races) * 0.1))
    
    train_races = unique_races[:-split]
    test_races = unique_races[-split:]

    train_data = pit_stop_rows[pit_stop_rows["RACEID"].isin(train_races)]
    test_data = pit_stop_rows[pit_stop_rows["RACEID"].isin(test_races)]

    x_train = train_data[["RACEID", "DRIVERID", "CIRCUITID", "CONSTRUCTORID", "POSITION", "CURRENT_LAP", "LAP_TIME_MILLISECONDS", "AVG_PREVIOUS_LAPS"]]
    y_train = train_data[["NEW_POSITION", "AVG_FUTURE_LAPS"]]
    y_test = test_data[["NEW_POSITION", "AVG_FUTURE_LAPS"]]
    x_test = test_data[["RACEID", "DRIVERID", "CIRCUITID", "CONSTRUCTORID", "POSITION", "CURRENT_LAP", "LAP_TIME_MILLISECONDS", "AVG_PREVIOUS_LAPS"]]

    test_case = race_data[(race_data["RACEID"] == test_races[0]) & (race_data["CONSTRUCTORID"] == 1) & (race_data["DRIVERID"] == 1)]
    test_case = test_case.drop(["STOP", "PIT_STOP_DURATION"], axis = 1)

    test_case = calc_avg_previous_laps(race_data, test_case)
    test_case = calc_positional_change(race_data, test_case)
    test_case = calc_avg_future_laps(race_data, test_case)

    return x_train, x_test, y_train, y_test, test_case

    
if __name__ == "__main__":
    data = get_data()
    x_train, x_test, y_train, y_test, test_case = format_data(data)

    print(test_case)
