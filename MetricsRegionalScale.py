import pandas as pd
from MetricsCalculator import MetCalculator


def calculate_metrics_from_regional_dataset(input_csv, output_csv, countries, india_tif, china_tif, usa_tif):
    
    """
    Calculate metrics for specified countries using regional datasets and save results to a CSV file.
    
    Parameters:
    - input_csv (str): Path to the input CSV file containing the data.
    - output_csv (str): Path to the output CSV file where metrics will be saved.
    - countries (list): List of countries to calculate metrics for.
    - india_tif (str): Path to the TIFF file for India.
    - china_tif (str): Path to the TIFF file for China.
    - usa_tif (str): Path to the TIFF file for the United States.
    """

    calculator = MetCalculator()
    
    df_filtered = pd.read_csv(input_csv)
    
    # Process regional data
    calculator.inverse_distance_weighted(df_filtered, india_tif, 'R_India', nodata_value=0)
    
    calculator.inverse_distance_weighted(df_filtered, china_tif, 'R_China', nodata_value=0)
    
    calculator.inverse_distance_weighted(df_filtered, usa_tif, 'R_United States', nodata_value=0)
    
    
    metrics_by_country = {}
    
    metrics_dfs = []

    for country in countries:
        
        country_df = df_filtered[df_filtered['Country'] == country]
        
        # Drop rows with missing values in the current metric column
        country_df = country_df.dropna(subset=[f'R_{country}'])
        
        # Filter rows with values greater than 1
        country_df = country_df[country_df[f'R_{country}'] > 1]
        
        simulated = country_df['GloRESatE']
        
        # Determine the multiplier factor for China
        if country == "China":
            
            multiplocation_factor = 0.7496
            
        else:
            
            multiplocation_factor = 0.8716
        
        metric_data = country_df[f'R_{country}'] * multiplocation_factor

        mean_pbias, std_pbias, ubrmse = calculator.ubrmse(metric_data, simulated)
        
        nse = calculator.nse(metric_data, simulated)
        
        correlation = calculator.correlation(metric_data, simulated)
        
        metrics_by_country[country] = {
            'Mean Percent Bias': mean_pbias,
            
            'Std Percent Bias': std_pbias,
            
            'NSE': nse,
            
            'Correlation Coefficient': correlation,
            
            'ubRMSE': ubrmse
        }
        
        metrics_df = pd.DataFrame(metrics_by_country).T
        
        metrics_dfs.append(metrics_df)
    
    final_df = pd.concat(metrics_dfs, axis=1)
    
    final_df.index.name = 'Country'

    final_df.to_csv(output_csv)


def main():
    
    """
    Main function to execute the metrics calculation and saving process.
    """

    input_csv = 'df_filtered.csv'
    
    output_csv = 'metrics_by_Region.csv'
    
    countries = ['India', 'China', 'United States']
    
    india_tif = 'path/to/India_tif_file.tif'
    
    china_tif = 'path/to/China_tif_file.tif'
    
    usa_tif = 'path/to/USA_tif_file.tif'
    
    calculate_metrics_from_regional_dataset(input_csv, output_csv, countries, india_tif, china_tif, usa_tif)


if __name__ == "__main__":
    main()
