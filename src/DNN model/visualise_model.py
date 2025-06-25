import pandas as pd
import matplotlib.pyplot as plt

def plot_pred_vs_actual_analysis():

    actual_results = pd.read_csv("plot_pred_vs_actual_analysis_data\\actual.csv")
    predicted_results = pd.read_csv("plot_pred_vs_actual_analysis_data\predictions.csv")

    plt.plot(predicted_results.index, predicted_results['AVG_FUTURE_LAPS'], label='Predicted Avg Lap Time After Five Laps', color='red', linestyle='-')
    plt.plot(actual_results.index, actual_results['AVG_FUTURE_LAPS'], label='Actual Avg Lap Time After Five Laps', color='blue', linestyle='--')

    plt.xlabel('Laps')
    plt.ylabel('Time (ms)')
    plt.title('Compairson in Predicted and Actual Avg Lap Times')
    plt.legend()

    plt.show()

def plot_pred_vs_current_analysis():
    current_lap_time = pd.read_csv("plot_pred_vs_current_analysis_data\current_lap_time.csv")
    predicted_results = pd.read_csv("plot_pred_vs_current_analysis_data\predictions.csv")

    plt.plot(predicted_results.index, predicted_results['AVG_FUTURE_LAPS'], label='Predicted Avg Lap Time After Five Laps', color='red', linestyle='-')
    plt.plot(current_lap_time.index, current_lap_time['LAP_TIME_MILLISECONDS'], label='Current Lap Time', color='blue', linestyle='--')

    plt.xlabel('Laps')
    plt.ylabel('Time (ms)')
    plt.title('Compairson in Predicted and Actual Avg Lap Times')
    plt.legend()

    plt.show()

if __name__ == "__main__":
    plot_pred_vs_actual_analysis()
    plot_pred_vs_current_analysis()
