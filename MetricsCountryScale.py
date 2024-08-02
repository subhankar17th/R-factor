import pandas as pd
from MetricsCalculator import MetCalculator


def calculate_metrics_by_countries(input_csv, output_csv, countries):

    """
    Calculate metrics for specified countries and save the results to a CSV file.
    
    Parameters:
    - input_csv (str): Path to the input CSV file containing the data.
    - output_csv (str): Path to the output CSV file where metrics will be saved.
    - countries (list): List of country names to calculate metrics for.
    """
    calculator = MetCalculator()
    
    df_filtered = pd.read_csv(input_csv)
    
    metrics_dfs = []
    
    # Metrics to be calculated
    metrics = ['R_Final', 'GloREDa', 'GloREDa1.2']
    
    for metric in metrics:
        
        metrics_by_country = {}
        
        for country in countries:
            
            country_df = df_filtered[df_filtered['Country'] == country]
            
            metric_data = country_df[metric]
            
            simulated = country_df['GloRESatE']
            
            # Calculate metrics
            mean_pbias, std_pbias, ubrmse = calculator.ubrmse(metric_data, simulated)
            
            nse = calculator.nse(metric_data, simulated)
            
            correlation = calculator.correlation(metric_data, simulated)
            
            metrics_by_country[country] = {
                
                'metrics for' : metric,
                
                'Mean Percent Bias': mean_pbias,
                
                'Std Percent Bias': std_pbias,
                
                'NSE': nse,
                
                'Correlation Coefficient': correlation,
                
                'ubRMSE': ubrmse
            }
        
        # Create DataFrame for current metric
        metrics_df = pd.DataFrame(metrics_by_country).T
        
        metrics_df.index.name = 'Country'
        
        metrics_dfs.append(metrics_df)
    
    # Combine metrics DataFrames and save to CSV
    final_df = pd.concat(metrics_dfs, axis=1)
    
    final_df.to_csv(output_csv)


def main():
    
    """
    Main function to execute the metrics calculation and saving process.
    """

    input_csv = 'df_filtered.csv'
    
    output_csv = 'metrics_by_countries.csv'
    
    countries = ['India', 'United States', 'China', 'Italy']
    
    calculate_metrics_by_countries(input_csv, output_csv, countries)


if __name__ == "__main__":
    main()
