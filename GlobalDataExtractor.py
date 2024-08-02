from MetricsCalculator import MetricsCalculator
import pandas as pd
import os

def main(input_csv, GloRESatE_tif, GloREDa_tif, GloREDa1_2_dir, output_csv):
    
    """
    Main function to perform data extraction and processing.
    
    Parameters:
    - input_csv (str): Path to the input CSV file.
    - GloRESatE_tif (str): Path to the GloRESatE TIFF file.
    - GloREDa_tif (str): Path to the GloREDa TIFF file.
    - GloREDa1_2_dir (str): Directory containing GloREDa1.2 TIFF files.
    - output_csv (str): Path to save the output CSV file.
    """

    calculator = MetricsCalculator()
    
    # Read the input CSV file
    df = pd.read_csv(input_csv)
    
    # Apply inverse distance weighting for GloRESatE and GloREDa
    df = calculator.inverse_distance_weighted(df, GloRESatE_tif, 'GloRESatE', 0)
    
    df = calculator.inverse_distance_weighted(df, GloREDa_tif, 'GloREDa', 0)
    
    # Calculate R factors and add them to the DataFrame
    df = calculate_r_factors(df, calculator, GloREDa1_2_dir)

    # Filter rows based on criteria
    df_filtered = filter_rows(df)
    
    # Save the filtered DataFrame to a CSV file
    save_to_csv(df_filtered, output_csv)


def calculate_r_factors(df, calculator, GloREDa1_2_dir):
    
    """
    Calculate R factors from TIFF files and add them as new columns to the DataFrame.
    
    Parameters:
    - df (DataFrame): Input DataFrame to be updated.
    - calculator (MetricsCalculator): MetricsCalculator object for distance weighting.
    - GloREDa1_2_dir (str): Directory containing GloREDa1.2 TIFF files.
    
    Returns:
    - DataFrame: Updated DataFrame with R factors and GloREDa1.2 column.
    """


    for map_file in os.listdir(GloREDa1_2_dir):
        
        if map_file.endswith('.tif'):
            
            # Extract month name from the file name
            month_name = map_file.split('_')[-1].split('.')[0]
            
            new_col_name = f'Rfactor_{month_name}'
            
            # Construct path to the TIFF file
            tif_file = os.path.join(GloREDa1_2_dir, map_file)
            
            new_col_name = new_col_name
            
            # Apply inverse distance weighting and add the result as a new column
            df = calculator.inverse_distance_weighted(df, tif_file, new_col_name, 0)
    
    # Calculate GloREDa1.2 as the sum of all R factor columns
    rfactor_columns = [col for col in df.columns if col.startswith('Rfactor_')]
    
    df['GloREDa1.2'] = df[rfactor_columns].sum(axis=1)

    # Drop the individual R factor columns
    df = df.drop(columns=rfactor_columns)
            
    return df


def filter_rows(df):
    
    """
    Filter rows in the DataFrame based on specific criteria.
    
    Parameters:
    - df (DataFrame): Input DataFrame to be filtered.
    
    Returns:
    - DataFrame: Filtered DataFrame.
    """

    df_filtered = df[(df['GloRESatE'] >= 1) & (df['GloRESatE'].notna()) &
                     
                     (df['GloREDa'] >= 1) & (df['GloREDa'].notna()) &
                     
                     (df['GloREDa1.2'] >= 1) & (df['GloREDa1.2'].notna()) &
                     
                     (df['R_Final'] >= 1) & (df['R_Final'].notna())]
    
    # Reset index after filtering
    df_filtered.reset_index(drop=True, inplace=True)
    
    return df_filtered


def save_to_csv(df, output_csv):
    
    """
    Save the DataFrame to a CSV file.
    
    Parameters:
    - df (DataFrame): DataFrame to be saved.
    - output_csv (str): Path to save the output CSV file.
    """


    df.to_csv(output_csv, index=False)


if __name__ == "__main__":
    
    # Define file paths
    input_csv = 'path_to_input_csv.csv'
    
    GloRESatE_tif = 'path_to_GloRESatE.tif'
    
    GloREDa_tif = 'path_to_GloREDa.tif'
    
    GloREDa1_2_dir = 'path_to_GloREDa1.2_directory'
    
    output_csv = 'path_to_output_csv.csv'
    
    # Execute the main function
    main(input_csv, GloRESatE_tif, GloREDa_tif, GloREDa1_2_dir, output_csv)
