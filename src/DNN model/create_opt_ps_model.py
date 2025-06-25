import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from sklearn.preprocessing import StandardScaler
from etl_pipeline.extract_from_snowflake import get_data
from etl_pipeline.optimal_pit_stop_transformation import format_data


def create_model(x_train, y_train):
    x_train = x_train.values
    y_train = y_train.values

    x_scaler = StandardScaler()
    scaled_x_train_Data = x_scaler.fit_transform(x_train)

    y_scaler = StandardScaler()
    scaled_y_train_Data = y_scaler.fit_transform(y_train)
    


    model = Sequential([
        Dense(64, activation="relu", input_shape=(scaled_x_train_Data.shape[1],)),
        Dropout(0.2),

        Dense(32, activation="relu"),
        Dropout(0.2),

        Dense(scaled_y_train_Data.shape[1])
    ])

    model.compile(optimizer=Adam(learning_rate=0.001), loss="mse", metrics=["mae"])
    model.fit(scaled_x_train_Data, scaled_y_train_Data, batch_size=64, epochs=50, validation_split=0.1, verbose=1)

    return model, x_scaler, y_scaler


def test_model(test_case, model, x_scaler, y_scaler):
    try:
        os.makedirs("plot_pred_vs_actual_analysis_data")
    except Exception as e:
        print(e)

    try:
        os.makedirs("plot_pred_vs_current_analysis_data")
    except Exception as e:
        print(e)

    x_test_case = test_case[["RACEID", "DRIVERID", "CIRCUITID", "CONSTRUCTORID", "POSITION", "CURRENT_LAP", "LAP_TIME_MILLISECONDS", "AVG_PREVIOUS_LAPS"]]
    y_test_case = test_case[["NEW_POSITION", "AVG_FUTURE_LAPS"]]

    y_test_case.to_csv("plot_pred_vs_actual_analysis_data\\actual.csv")

    x_test_case = x_test_case.values
    x_test_case = x_scaler.transform(x_test_case)
    predictions = model.predict(x_test_case)
    predictions = y_scaler.inverse_transform(predictions)
    predictions = pd.DataFrame(predictions, columns=['NEW_POSITION', "AVG_FUTURE_LAPS"])

    predictions.to_csv("plot_pred_vs_actual_analysis_data\predictions.csv")

    current_lap_time = test_case["LAP_TIME_MILLISECONDS"]
    predictions.to_csv("plot_pred_vs_current_analysis_data\predictions.csv")
    current_lap_time.to_csv("plot_pred_vs_current_analysis_data\current_lap_time.csv")

if __name__ == "__main__":
    data = get_data()
    x_train, x_test, y_train, y_test, test_case = format_data(data)

    model, x_scaler, y_scaler  = create_model(x_train, y_train)
    
    test_model(test_case, model, x_scaler, y_scaler)
