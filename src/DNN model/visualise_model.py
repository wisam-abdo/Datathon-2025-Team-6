import pandas as pd
import matplotlib.pyplot as plt

def plot_optimal_pit_stop_analysis():

    actual_results = pd.read_csv("optimal_pit_stop_analysis_data\\actual.csv")
    predicted_results = pd.read_csv("optimal_pit_stop_analysis_data\predictions.csv")

    plt.plot(predicted_results.index, predicted_results['AVG_FUTURE_LAPS'], label='Predicted Avg Lap Time After Five Laps', color='red', linestyle='-')
    plt.plot(actual_results.index, actual_results['AVG_FUTURE_LAPS'], label='Actual Avg Lap Time After Five Laps', color='blue', linestyle='--')

    plt.xlabel('Laps')
    plt.ylabel('Time (ms)')
    plt.title('Compairson in Predicted and Actual Avg Lap Times')
    plt.legend()

    plt.show()

if __name__ == "__main__":
    plot_optimal_pit_stop_analysis()
