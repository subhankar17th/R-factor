import rasterio
import numpy as np

class MetCalculator:
    def __init__(self):
        pass
    
    def ubrmse(self, observed, predicted):
        
        """
        Calculates the unbiased root mean square error (UBRMSE) and percentage bias statistics.
        
        Parameters:
        observed (array-like): Array of observed values.
        predicted (array-like): Array of predicted values.
        
        Returns:
        mean_percentage_bias (float): Mean percentage bias between observed and predicted values.
        std_percentage_bias (float): Standard deviation of percentage bias.
        ubrmse (float): Unbiased root mean square error.
        """
        
        # Check that observed and predicted arrays have the same length
        if len(observed) != len(predicted):
            raise ValueError("Both arrays must have the same length.")
        
        n = len(observed)

        # Calculate percentage bias
        percentage_bias = ((predicted - observed) / observed) * 100
        
        mean_percentage_bias = np.mean(percentage_bias)
        
        # Calculate standard deviation of percentage bias
        squared_diff = (percentage_bias - mean_percentage_bias)**2
        
        sum_squared_diff = np.sum(squared_diff)
        
        std_percentage_bias = np.sqrt(sum_squared_diff / n)
        
        ubrmse = np.sqrt(np.mean(((predicted - np.mean(predicted)) - (observed - np.mean(observed)))**2))
        
        return mean_percentage_bias, std_percentage_bias, ubrmse


    def nse(self, observed, simulated):
        
        """
        Calculates the Nash-Sutcliffe efficiency (NSE).
        
        Parameters:
        observed (array-like): Array of observed values.
        simulated (array-like): Array of simulated values.
        
        Returns:
        nse (float): Nash-Sutcliffe efficiency.
        """

        observed = np.array(observed)
        
        simulated = np.array(simulated)
        
        # Calculate NSE
        numerator = np.sum((observed - simulated)**2)
        
        denominator = np.sum((observed - np.mean(observed))**2)
        
        nse = 1 - (numerator / denominator)
        
        return nse

    def correlation(self, observed, simulated):
        
        """
        Calculates the Pearson correlation coefficient between observed and simulated values.
        
        Parameters:
        observed (array-like): Array of observed values.
        simulated (array-like): Array of simulated values.
        
        Returns:
        correlation (float): Pearson correlation coefficient.
        """
        
        # Ensure inputs are pandas Series for correlation calculation
        correlation = observed.corr(simulated)
        
        return correlation


    def inverse_distance_weighted(self, df, tif_file, new_col_name, nodata_value):
        
        """
        Applies inverse distance weighting interpolation to assign values from a raster to DataFrame points.
        
        Parameters:
        df (pandas.DataFrame): DataFrame with latitude and longitude columns.
        tif_file (str): Path to the raster file (TIFF).
        new_col_name (str): Name of the new column to store interpolated values.
        nodata_value (float): Value in the raster representing no data.
        
        Returns:
        df (pandas.DataFrame): DataFrame with new column containing interpolated values.
        """
        
        with rasterio.open(tif_file) as src:
            
            # Read raster data and handle no-data values
            tiff_array = src.read(1)
            
            tiff_array = tiff_array.astype("float")
            
            tiff_array[tiff_array < nodata_value] = np.nan
            
            # Get the transformation matrix
            transform = src.transform

            for index, row in df.iterrows():
                lat, lon = row['Lat'], row['Lon']
                
                # Convert latitude and longitude to raster coordinates
                col, row = ~transform * (lon, lat)
                
                col, row = int(round(col)), int(round(row))

                pixel_values = []
                
                distances = []
                
                # Loop over a 3x3 window around the target pixel
                for r in range(row - 1, row + 2):
                    
                    for c in range(col - 1, col + 2):
                        
                        if 0 <= r < tiff_array.shape[0] and 0 <= c < tiff_array.shape[1]:
                            
                            pixel_value = tiff_array[r, c]
                            
                            if not np.isnan(pixel_value):
                                
                                pixel_values.append(pixel_value)
                                
                                pixel_lat, pixel_lon = transform * (c, r)
                                
                                distance = np.sqrt((lat - pixel_lat) ** 2 + (lon - pixel_lon) ** 2)
                                
                                distances.append(distance)
                
                # Compute weighted average if there are valid pixel values
                if len(pixel_values) > 0:
                    
                    weights = [1 / distance for distance in distances]
                    
                    weighted_average = np.average(pixel_values, weights=weights)
                    
                    df.loc[index, new_col_name] = weighted_average
                    
                else:
                    df.loc[index, new_col_name] = float('NaN')

        return df
