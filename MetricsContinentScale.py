import pandas as pd
from MetricsCalculator import MetCalculator

def calculate_metrics_by_continent(input_csv, output_csv):
    
    """
    Calculate metrics by continent and save the results to a CSV file.
    
    Parameters:
    - input_csv (str): Path to the input CSV file containing the data.
    - output_csv (str): Path to the output CSV file where metrics will be saved.
    """
    
    # Instantiate the MetCalculator
    calculator = MetCalculator()

    # Load the filtered DataFrame
    df_filtered = pd.read_csv(input_csv)

    # Group by 'Continent' and initialize dictionary to store metrics
    grouped = df_filtered.groupby('Continent')

    metrics_by_continent = {}

    # Calculate metrics for each continent
    for continent, group_df in grouped:
       
        simulated = group_df['GloRESatE']
        
        r_final = group_df['R_Final']

        # Calculate metrics
        mean_pbias_r_final, std_pbias_r_final, ubrmse_r_final = calculator.ubrmse(r_final, simulated)
        
        nse_r_final = calculator.nse(r_final, simulated)
        
        correlation_r_final = calculator.correlation(r_final, simulated)

        # Store metrics in dictionary
        metrics_by_continent[continent] = {
            'Mean Percent Bias': mean_pbias_r_final,
            
            'Std Percent Bias': std_pbias_r_final,
            
            'NSE': nse_r_final,
            
            'Correlation Coefficient': correlation_r_final,
            
            'ubRMSE': ubrmse_r_final
        }

    # Convert metrics dictionary to DataFrame and save to CSV
    metrics_df = pd.DataFrame(metrics_by_continent).T

    metrics_df.to_csv(output_csv)

def main():
    """
    Main function to execute the metrics calculation and saving process.
    """
    input_csv = 'df_filtered.csv'
    
    output_csv = 'metrics_by_continent.csv'
    
    calculate_metrics_by_continent(input_csv, output_csv)

if __name__ == "__main__":
    
    main()
