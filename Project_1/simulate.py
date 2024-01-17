import pandas as pd
import random
import sys

def coin_toss_simulation_with_summary(market_initial_wealth=1000000, chintu_win_probability=0.5, chintu_initial_networth_ratio=0.01, bet_size_ratio=0.1, no_of_time_steps=100, bet_strategy='Bet size constant', below_zero_strategy='Below zero no more bets', capital_conservation_strategy='no capital realization', random_seed=None):
    # Generate a random seed if not provided
    if random_seed is None:
        random_seed = random.randint(0, sys.maxsize)
    random.seed(random_seed)
    
    # Initialize initial wealth
    market_wealth = market_initial_wealth
    chintu_wealth = chintu_initial_networth_ratio * market_initial_wealth

    # Initialize bet size
    bet_size = bet_size_ratio * chintu_wealth

    # Define DataFrame columns and data types
    columns = ['Time Step', 'Bet Outcome', 'Bet Size', 'Chintu Networth', 'Market Networth', 'Random Seed']
    dtypes = {'Time Step': 'int', 'Bet Outcome': 'str', 'Bet Size': 'float', 'Chintu Networth': 'float', 'Market Networth': 'float', 'Random Seed': 'int'}
    results = pd.DataFrame(columns=columns).astype(dtypes)

    # Initialize variables to track the time to zero for Chintu
    chintu_zero_time = None

    for step in range(no_of_time_steps):
        # Determine bet size based on strategy
        if bet_strategy == 'Bet proportional to Net worth':
            bet_size = bet_size_ratio * chintu_wealth
        elif bet_strategy == 'Bet inversely proportional to NV':
            bet_size = bet_size_ratio * (1 / chintu_wealth)

        # Simulate coin toss
        outcome = 'Chintu Win' if random.random() <= chintu_win_probability else 'Market Win'

        # Update net worth based on outcome
        if outcome == 'Chintu Win':
            chintu_wealth += bet_size
            market_wealth -= bet_size
        else:
            chintu_wealth -= bet_size
            market_wealth += bet_size

        # Check for Chintu's net worth reaching zero
        if chintu_wealth <= 0 and chintu_zero_time is None:
            chintu_zero_time = step + 1

        # Apply below zero strategy
        if below_zero_strategy == 'Below zero no more bets' and (chintu_wealth <= 0 or market_wealth <= 0):
            break

        # Create a new row and concatenate it to the results DataFrame
        new_row = pd.DataFrame({'Time Step': [step + 1], 'Bet Outcome': [outcome], 'Bet Size': [bet_size], 'Chintu Networth': [chintu_wealth], 'Market Networth': [market_wealth], 'Random Seed': [random_seed]}).astype(dtypes)
        results = pd.concat([results, new_row], ignore_index=True)

    # Summary of the results
    summary = {
        "Chintu Final Networth": chintu_wealth,
        "Market Final Networth": market_wealth,
        "Time to Zero for Chintu": chintu_zero_time if chintu_zero_time is not None else "Never reached zero"
    }

    return results, summary

def trials_with_summary(no_of_trials, market_initial_wealth=1000000, chintu_win_probability=0.5, chintu_initial_networth_ratio=0.01, bet_size_ratio=0.1, no_of_time_steps=100, bet_strategy='Bet size constant', below_zero_strategy='Below zero no more bets', capital_conservation_strategy='no capital realization'):
  
    trials_with_summary_input = {
        'no_of_trials': no_of_trials, 
        'chintu_win_probability': chintu_win_probability, 
        'chintu_initial_networth_ratio': chintu_initial_networth_ratio, 
        'bet_size_ratio': bet_size_ratio, 
        'no_of_time_steps': no_of_time_steps, 
        'bet_strategy': bet_strategy, 
        'below_zero_strategy': below_zero_strategy, 
        'capital_conservation_strategy': capital_conservation_strategy
    }
    print(trials_with_summary_input)

    # List to store results of each trial
    trial_results = []
    chintu_win_count = 0
    chintu_zero_count = 0
    total_profit_chintu = 0

    for trial in range(no_of_trials):
        # Run the simulation with the specified parameters
        _, summary = coin_toss_simulation_with_summary(market_initial_wealth, chintu_win_probability, chintu_initial_networth_ratio, bet_size_ratio, no_of_time_steps, bet_strategy, below_zero_strategy, capital_conservation_strategy)

        # Compute net profits
        chintu_initial_networth = chintu_initial_networth_ratio * market_initial_wealth
        net_profit_chintu = summary['Chintu Final Networth'] - chintu_initial_networth
        net_profit_market = summary['Market Final Networth'] - market_initial_wealth

        # Count wins and zero net worth occurrences for Chintu
        if net_profit_chintu > 0:
            chintu_win_count += 1
        if summary['Time to Zero for Chintu'] != 'Never reached zero':
            chintu_zero_count += 1

        # Total profit for Chintu
        total_profit_chintu += net_profit_chintu

        # Extract relevant information from the summary
        trial_result = {
            'Trial No': trial + 1,
            'Chintu Final Networth': summary['Chintu Final Networth'],
            'Market Final Networth': summary['Market Final Networth'],
            'Time to Zero for Chintu': summary['Time to Zero for Chintu'],
            'Net Profit Chintu': net_profit_chintu,
            'Net Profit Market': net_profit_market
        }

        # Append the result of this trial to the list
        trial_results.append(trial_result)

    # Convert list to DataFrame
    trial_results_df = pd.DataFrame(trial_results)

    # Calculate summary statistics
    chintu_percentage_win_times = (chintu_win_count / no_of_trials) * 100
    chintu_percentage_zero_times = (chintu_zero_count / no_of_trials) * 100
    chintu_expected_profit_overall = total_profit_chintu / no_of_trials

    summary = {
        'Chintu Percentage Win Times': chintu_percentage_win_times,
        'Chintu Percentage Zero Times': chintu_percentage_zero_times,
        'Chintu Expected Profit Overall': chintu_expected_profit_overall
    }

    return trial_results_df, summary

# # Example usage
# # Run 5 trials with custom parameters and get the summary
# custom_trial_results_with_summary, summary = trials_with_summary(market_initial_wealth=1000000, chintu_initial_networth_ratio=0.01,no_of_trials=1000, bet_size_ratio=0.1, chintu_win_probability=0.5)
# print(custom_trial_results_with_summary)
# print("\nSummary:")
# print(summary)


 