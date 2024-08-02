import os
import pandas as pd
from LongitudeAdjuster import LonAdjuster
from MetricsCalculator import MetCalculator
from ClimateExtractor import ClimExtractor

def data_extraction_from_dataset(input_csv, climate_file, ERA5Land_file, IMERGFinalRun_file, COMPRH_file, GloRESatE_file):
    
    """
    Extract and process data from various climate datasets and calculate percentage bias.
    
    Parameters:
    - input_csv (str): Path to the input CSV file.
    - climate_file (str): Path to the climate TIFF file.
    - ERA5Land_file (str): Path to the ERA5Land TIFF file.
    - IMERGFinalRun_file (str): Path to the IMERGFinalRun TIFF file.
    - COMPRH_file (str): Path to the CMORPH TIFF file.
    - GloRESatE_file (str): Path to the GloRESatE TIFF file.
    
    Returns:
    - DataFrame: Processed DataFrame with percentage bias calculations.
    """
    
    # Initialize the necessary objects
    adjuster = LonAdjuster()
    
    calculator = MetCalculator()
    
    climate = ClimExtractor()
    
    # Read the input CSV file
    df_filtered = pd.read_csv(input_csv)
    
    # Extract climate values and add them to the DataFrame
    df_filtered = climate.extract_climate_values(climate_file, df_filtered)
    
    # Get current working directory
    cwd = os.getcwd()
    
    # Adjust longitude and save TIFF file for ERA5Land
    output_ERA5Land_file = os.path.join(cwd, 'ERA5_land.tiff')
    adjuster.adjust_longitude_and_save_tiff(ERA5Land_file, output_ERA5Land_file)
    
    # Apply inverse distance weighting for ERA5Land
    calculator.inverse_distance_weighted(df_filtered, output_ERA5Land_file, "ERA5Land", 0)
    
    # Apply inverse distance weighting for IMERGFinalRun
    calculator.inverse_distance_weighted(df_filtered, IMERGFinalRun_file, "IMERGFinalRun", 0)
    
    # Adjust longitude and save TIFF file for CMORPH
    output_CMORPH_file = os.path.join(cwd, 'CMORPH.tiff')
    
    adjuster.adjust_longitude_and_save_tiff(COMPRH_file, output_CMORPH_file)
    
    # Apply inverse distance weighting for CMORPH
    calculator.inverse_distance_weighted(df_filtered, output_CMORPH_file, "COMPRHFile", 0)
    
    # Apply inverse distance weighting for GloRESatE
    calculator.inverse_distance_weighted(df_filtered, GloRESatE_file, "GloRESatEfile", 0)
    
    # Adjust ERA5Land values
    df_filtered["ERA5Land"] = df_filtered["ERA5Land"] * 1.5597
    
    # Filter out rows where any of the specified columns are below threshold or NaN
    df_filtered = df_filtered[(df_filtered['GloRESatEfile'] >= 1) & (df_filtered['GloRESatEfile'].notna()) &
                     
                     (df_filtered['COMPRHFile'] >= 1) & (df_filtered['COMPRHFile'].notna()) &
                     
                     (df_filtered['IMERGFinalRun'] >= 1) & (df_filtered['IMERGFinalRun'].notna()) &
                     
                     (df_filtered['ERA5Land'] >= 1) & (df_filtered['ERA5Land'].notna())]
    
    # Reset index of the DataFrame
    df_filtered.reset_index(drop=True, inplace=True)
    
    # Calculate percentage bias for each dataset
    df_filtered["PercentCMORPH"] = ((df_filtered["COMPRHFile"] - df_filtered["R_Final"]) / df_filtered["R_Final"]) * 100
    
    df_filtered["PercentIMERG"] = ((df_filtered["IMERGFinalRun"] - df_filtered["R_Final"]) / df_filtered["R_Final"]) * 100
    
    df_filtered["PercentERA5"] = ((df_filtered["ERA5Land"] - df_filtered["R_Final"]) / df_filtered["R_Final"]) * 100
    
    df_filtered["PercentGloRESatE"] = ((df_filtered["GloRESatEfile"] - df_filtered["R_Final"]) / df_filtered["R_Final"]) * 100
    
    # Save the filtered DataFrame to a CSV file
    df_filtered.to_csv("Percetage_bias.csv")
    
    return df_filtered
    
    
def calculate_metrics_for_climate_datasets(df_filtered, output_csv):
    
    """
    Calculate metrics for different climate datasets based on the climate type.
    
    Parameters:
    - df_filtered (DataFrame): DataFrame with filtered climate data.
    - output_csv (str): Path to save the metrics CSV file.
    """
    
    calculator = MetCalculator()
    
    metrics_dfs = []
    
    
    # Iterate through each dataset and climate type
    for dataset in ['COMPRHFile', 'IMERGFinalRun', 'ERA5Land', 'GloRESatEfile']:
        
        metrics = {}

        for climate_type in df_filtered['ClimateType'].unique():
            
            df_climate = df_filtered[df_filtered['ClimateType'] == climate_type]
            
            simulated_values = df_climate[dataset]
            
            observed_values = df_climate['R_Final']
            
            # Calculate metrics
            mean_pbias, std_pbias, ubrmse = calculator.ubrmse(observed_values, simulated_values)
            
            nse = calculator.nse(observed_values, simulated_values)
            
            correlation = calculator.correlation(observed_values, simulated_values)
            
            metrics[climate_type] = {
                
                'metrics for' : dataset,
                
                'Mean_PBIAS': mean_pbias,
                
                'Std_PBIAS': std_pbias,
                
                'UBRMSE': ubrmse,
                
                'NSE': nse,
                
                'Correlation': correlation
            }
            
            # Convert metrics to DataFrame
            metrics_df = pd.DataFrame(metrics).T
            
            metrics_df.index.name = 'ClimateType'
            
            metrics_dfs.append(metrics_df)
    
    # Concatenate all metrics DataFrames and save to CSV
    final_df = pd.concat(metrics_dfs, axis=1)

    final_df.to_csv(output_csv)

    
def calculate_metrics_for_all_datasets(df_filtered, output_csv):
    
    """
     Calculate metrics for all datasets combined.
    
     Parameters:
     - df_filtered (DataFrame): DataFrame with filtered climate data.
     - output_csv (str): Path to save the metrics CSV file.
     """
    calculator = MetCalculator()
    
    metrics = {}
    
    # Iterate through each dataset
    for dataset in ['COMPRHFile', 'IMERGFinalRun', 'ERA5Land', 'GloRESatEfile']:

        simulated_values = df_filtered[dataset]
        
        observed_values = df_filtered['R_Final']
        
        # Calculate metrics
        mean_pbias, std_pbias, ubrmse = calculator.ubrmse(observed_values, simulated_values)
        
        nse = calculator.nse(observed_values, simulated_values)
        
        correlation = calculator.correlation(observed_values, simulated_values)
        
        metrics[dataset] = {
            'Mean_PBIAS': mean_pbias,
            
            'Std_PBIAS': std_pbias,
            
            'UBRMSE': ubrmse,
            
            'NSE': nse,
            
            'Correlation': correlation
        }
    
    # Convert metrics to DataFrame and save to CSV
    df_metrics_all = pd.DataFrame(metrics).T
    
    df_metrics_all.to_csv(output_csv)


def main():
    
    # Define file paths
    input_csv = '.../df_filtered.csv'
    
    ERA5Land_file = '.../ERA5Land_mean_2001_2020.tif'
    
    IMERGFinalRun_file = '../IMERGFinalRun_mean_2001_2020.tif'
    
    COMPRH_file = '..../CMORPH_mean_2021_2020.tif'
    
    GloRESatE_file = '.../GloRESatE.tif'
    
    climate_file = '.../Beck_KG_V1_present_0p0083.tif'
    
    # Perform data extraction and processing
    df_filtered = data_extraction_from_dataset(input_csv, climate_file, ERA5Land_file, IMERGFinalRun_file, COMPRH_file, GloRESatE_file)
    
    # Calculate metrics for climate datasets and save to CSV
    calculate_metrics_for_climate_datasets(df_filtered, 'metrics_climate.csv')
    
    # Calculate metrics for all datasets and save to CSV
    calculate_metrics_for_all_datasets(df_filtered, 'metrics_all.csv')

if __name__ == "__main__":
    
    main()











