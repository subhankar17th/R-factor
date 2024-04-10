import rasterio
import numpy as np

class MetCalculator:
    def __init__(self):
        pass
    
    def ubrmse(self, observed, predicted):

        if len(observed) != len(predicted):
            raise ValueError("Both arrays must have the same length.")
        
        n = len(observed)

        percentage_bias = ((predicted - observed) / observed) * 100
        
        mean_percentage_bias = np.mean(percentage_bias)
        
        squared_diff = (percentage_bias - mean_percentage_bias)**2
        
        sum_squared_diff = np.sum(squared_diff)
        
        std_percentage_bias = np.sqrt(sum_squared_diff / n)
        
        ubrmse = np.sqrt(np.mean(((predicted - np.mean(predicted)) - (observed - np.mean(observed)))**2))
        
        return mean_percentage_bias, std_percentage_bias, ubrmse


    def nse(self, observed, simulated):

        observed = np.array(observed)
        
        simulated = np.array(simulated)

        numerator = np.sum((observed - simulated)**2)
        
        denominator = np.sum((observed - np.mean(observed))**2)
        
        nse = 1 - (numerator / denominator)
        
        return nse

    def correlation(self, observed, simulated):

        correlation = observed.corr(simulated)
        
        return correlation


    def inverse_distance_weighted(self, df, tif_file, new_col_name, nodata_value):
        
        with rasterio.open(tif_file) as src:
            
            tiff_array = src.read(1)
            
            tiff_array = tiff_array.astype("float")
            
            tiff_array[tiff_array < nodata_value] = np.nan

            transform = src.transform

            for index, row in df.iterrows():
                lat, lon = row['Lat'], row['Lon']
                
                col, row = ~transform * (lon, lat)
                
                col, row = int(round(col)), int(round(row))

                pixel_values = []
                
                distances = []

                for r in range(row - 1, row + 2):
                    
                    for c in range(col - 1, col + 2):
                        
                        if 0 <= r < tiff_array.shape[0] and 0 <= c < tiff_array.shape[1]:
                            
                            pixel_value = tiff_array[r, c]
                            
                            if not np.isnan(pixel_value):
                                
                                pixel_values.append(pixel_value)
                                
                                pixel_lat, pixel_lon = transform * (c, r)
                                
                                distance = np.sqrt((lat - pixel_lat) ** 2 + (lon - pixel_lon) ** 2)
                                
                                distances.append(distance)

                if len(pixel_values) > 0:
                    
                    weights = [1 / distance for distance in distances]
                    
                    weighted_average = np.average(pixel_values, weights=weights)
                    
                    df.loc[index, new_col_name] = weighted_average
                    
                else:
                    df.loc[index, new_col_name] = float('NaN')

        return df
