from MetricsCalculator import MetCalculator
import pandas as pd

def calculate_metrics(df_filtered):
    """
    Calculate metrics comparing simulated data to observed data and save results to a CSV file.

    Parameters:
    - df_filtered (DataFrame): DataFrame containing observed and simulated values.
    """
    
    # Instantiate the MetricsCalculator
    calculator = MetCalculator()

    # Extract columns for comparison
    simulated = df_filtered['GloRESatE']
    
    observed_a = df_filtered['GloREDa']
    
    observed_a_1_2 = df_filtered['GloREDa1.2']
    
    r_final = df_filtered['R_Final']

    # Calculate metrics
    mean_pbias_a, std_pbias_a, ubrmse_a = calculator.ubrmse(observed_a, simulated)
    nse_a = calculator.nse(observed_a, simulated)
    
    correlation_a = calculator.correlation(observed_a, simulated)

    mean_pbias_a_1_2, std_pbias_a_1_2, ubrmse_a_1_2 = calculator.ubrmse(observed_a_1_2, simulated)
    nse_a_1_2 = calculator.nse(observed_a_1_2, simulated)
    
    correlation_a_1_2 = calculator.correlation(observed_a_1_2, simulated)

    mean_pbias_r_final, std_pbias_r_final, ubrmse_r_final = calculator.ubrmse(r_final, simulated)
    nse_r_final = calculator.nse(r_final, simulated)
    
    correlation_r_final = calculator.correlation(r_final, simulated)

    # Create a DataFrame to store metrics
    metrics_data = {
        'Metric': ['Percent Bias (mean)', 'Percent Bias (std)', 'NSE', 'Correlation Coefficient', 'ubRMSE'],
        
        'R_Final': [mean_pbias_r_final, std_pbias_r_final, nse_r_final, correlation_r_final, ubrmse_r_final],
        
        'GloREDa': [mean_pbias_a, std_pbias_a, nse_a, correlation_a, ubrmse_a],
        
        'GloREDA1.2': [mean_pbias_a_1_2, std_pbias_a_1_2, nse_a_1_2, correlation_a_1_2, ubrmse_a_1_2],    
    }

    # Convert to DataFrame and save to CSV
    metrics_df = pd.DataFrame(metrics_data)
    
    metrics_df.to_csv('metrics.csv', index=False)

def main():
    """
    Main function to execute the metric calculation process.
    """
    try:
        # Load filtered DataFrame
        df_filtered = pd.read_csv('df_filtered.csv')
        
        # Calculate and save metrics
        calculate_metrics(df_filtered)
        
    except FileNotFoundError as e:
        
        print(f"Error: {e}")
        
    except Exception as e:
        
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
