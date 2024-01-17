import json
import pandas as pd
from simulate import trials_with_summary 


def generate_parameter_range(start, end, increment):
    return [start + i * increment for i in range(int((end - start) / increment) + 1)]


def experiment(config_file):
    # Read the configuration file
    with open(config_file, 'r') as file:
        config = json.load(file)

    # Generate parameter ranges
    market_mf_range = generate_parameter_range(config["Market MF"]["Range_start"], config["Market MF"]["Range_end"], config["Market MF"]["Increment"])
    chintu_win_prob_range = generate_parameter_range(config["Chintu win probability"]["Range_start"], config["Chintu win probability"]["Range_end"], config["Chintu win probability"]["Increment"])
    bet_size_range = generate_parameter_range(config["Bet size"]["Range_start"], config["Bet size"]["Range_end"], config["Bet size"]["Increment"])
    no_of_timesteps_range = generate_parameter_range(config["No of Timesteps"]["Range_start"], config["No of Timesteps"]["Range_end"], config["No of Timesteps"]["Increment"])

    # Fixed values
    market_initial_wealth = config["market_initial_wealth"]["Value"]
    no_of_trials = config["No of Trials"]["Value"]

    # Prepare a list for storing flattened experiment data
    experiment_data = []

    
    # Iterate over all combinations of parameters
    for market_mf in market_mf_range:
        for chintu_win_prob in chintu_win_prob_range:
            for bet_size in bet_size_range:
                for no_of_timesteps in no_of_timesteps_range:
                    chintu_initial_networth = market_initial_wealth / market_mf
                    print(f"Running trials for Market Initial wealth={market_initial_wealth}, chintu initial wealth = {chintu_initial_networth}, market MF = {market_mf}, Chintu Win Probability={chintu_win_prob}, Bet Size={bet_size}, No of Timesteps={no_of_timesteps}")

                    # Run trials and get the summary
                    _, summary = trials_with_summary(
                        no_of_trials=no_of_trials,
                        market_initial_wealth=market_initial_wealth,
                        chintu_win_probability=chintu_win_prob,
                        chintu_initial_networth_ratio=chintu_initial_networth / market_initial_wealth,
                        bet_size_ratio=bet_size,
                        no_of_time_steps=no_of_timesteps
                    )

                    # Append the summary data to the list
                    experiment_data.append({
                        "Market Initial Wealth": market_initial_wealth,
                        "Chintu Initial Networth": chintu_initial_networth,
                        "Market MF": market_mf,
                        "Chintu Win Probability": chintu_win_prob,
                        "Bet Size": bet_size,
                        "No of Timesteps": no_of_timesteps,
                        "Chintu Percentage Win Times": summary['Chintu Percentage Win Times'],
                        "Chintu Percentage Zero Times": summary['Chintu Percentage Zero Times'],
                        "Chintu Expected Profit Overall": summary['Chintu Expected Profit Overall']
                    })

    # Convert the list of experiment data to a DataFrame
    experiment_results_df = pd.DataFrame(experiment_data)

    # Save the DataFrame to an Excel file
    experiment_results_df.to_excel("Experiment Outcome.xlsx", index=False)

    return experiment_results_df

# Example usage
experiment_results_df = experiment("experiment_config.json")
print(experiment_results_df)
