import json
import numpy as np
import pandas as pd

filename = "training_result_files/traffic_fine_process.json"
with open(filename) as f:
    table = json.load(f)
    # config consists of {technique}_{sequ-enc}_{event-enc} eg. LSTM_PREPAD_ONEHOT
    configs = list(table.keys())

    result_of_each_config = {}
    # calculations for LSTMs and CNNs results
    for config in configs[:12]:
        # Analytics of each fold (array)
        # Each fold contains the result of each metric (Accuracy, Precision, Recall, F1, Time)
        config_analytics = table[config]
        config_result = []
        for metric in range(5):
            arr = np.array(config_analytics)[:, metric]
            mean = round(np.mean(arr), 5)
            std = round(np.std(arr), 5)
            config_result.append(f"{mean};{std}")
        result_of_each_config[config] = config_result

    # calculations for DTs results
    for config in configs[12:]:
        config_analytics = table[config]
        # reduce to "gini" criterion
        gini_results = [row[2:] for row in config_analytics if "gini" in row]
        config_result = []
        for metric in range(5):
            arr = np.array(gini_results)[:, metric]
            mean = round(np.mean(arr), 5)
            std = round(np.std(arr), 5)
            config_result.append(f"{mean};{std}")
        result_of_each_config[config] = config_result

    df = pd.DataFrame(result_of_each_config, index=["Accuracy", "Precision", "Recall", "F1", "Time"])
    print(df)
    df.to_csv('training_results.csv', mode='a', header=False)

