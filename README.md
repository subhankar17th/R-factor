**Rainfall erosivity**, often denoted as the R-factor, is one of the most critical factors influencing erosion processes. Estimating the R-factor from high-resolution satellite and reanalysis datasets requires the identification of erosive events and subsequent computation of erosivity for each time interval.

The **MATLAB** code provided in this repository effectively computes rainfall erosivity values for each grid using 30-minute and 60-minute rainfall data. However, users are requested to first prepare all datasets in array format before utilizing the *MATLAB* function to estimate rainfall erosivity. 

Data Source: *CMORPH* (https://doi.org/10.25921/w9va-q159), *IMERG Final Run* (https://disc.gsfc.nasa.gov/datasets) and *ERA5-Land* (https://cds.climate.copernicus.eu/cdsapp).

The code uses the proposed method of *Renard et al. (1997)* for the identification of erosive storms and *McGregor et al. (1995 & 1976)* method for the rainfall erosivity estimation.
The estimated rainfall erosivity from the three datasets using the MATLAB codes has been provided in the Zenodo (https://doi.org/10.5281/zenodo.8406086). The **global rainfall erosivity station dataset** and the prepared merged **GloRESatE** dataset have also been provided in the same repository.

Python Modules Overview
1. **MetCalculator**

Purpose: Estimate metrics such as *Percentage Error*, *Unbiased Root Mean Squared Error*, *Pearson Correlation Coefficient*, and *Nash–Sutcliffe Efficiency* between observed and predicted datasets.
Methods: Based on the formulae of Moriasi et al. (2007) and Ma et al. (2019).

2. **GPR (Gaussian Process Regression)**

Purpose: Build an optimized model for estimating a merged rainfall erosivity product.
Methods: Utilizes the *sklearn* library for Gaussian Process Regression and the *BayesianOptimization* library for hyperparameter tuning.

3. **GlobalDataExtractor**

Purpose: Extract rainfall erosivity data from the existing two global datasets (*GloREDa* and *GloREDa v1.2*) and the *GloRESatE* dataset prepared in this study to compare different metrics.

4. **MetricsContinentScale**

Purpose: Estimate the metrics at the continent scale between *GloRESatE* and the *global rainfall erosivity station dataset*.

Data Source: Zenodo (https://doi.org/10.5281/zenodo.8406086).

5. **MetricsCountryScale**

Purpose: Estimate the metrics at the country scale between the *GloRESatE* estimates and other global datasets.

6. **MetricsEstimationClimate**

Purpose: Estimate the metrics for different climatic regions between the *global rainfall erosivity station dataset* and satellite/reanalysis-based erosivity estimates.

7. **MetricsGlobalData**

Purpose: Estimate the metrics at the global scale between *GloRESatE* and *GloREDa* datasets.

8. **MetricsRegionalScale**

Purpose: Estimate the metrics at the regional scale between the *GloRESatE* dataset and regional-level datasets for four countries (India, China, United States, and Italy).

**References**:

Renard, K., Foster, G., Weesies, G., McCool, D. & Yoder, D. Predicting soil erosion by water: a guide to conservation planning with the Revised Universal Soil Loss Equation (RUSLE). Agric. Handb. No. 703 404 (1997).

McGregor, K. C., Bingner, R. L., Bowie, A. J. & Foster, G. R. Erosivity index values for northern Mississippi. Trans. - Am. Soc. Agric. Eng. 38, 1039–1047 (1995).

McGregor, K. C. & Mutchler, C. K. Status of the R factor in northern Mississippi. Soil Eros. Predict. Control 135–142 (1976).

Moriasi, D. N. et al. Model evaluation guidelines for systematic quantification of accuracy in watershed simulations. Trans. ASABE 50, 885–900 (2007).

Ma, H. et al. Satellite surface soil moisture from SMAP, SMOS, AMSR2, and ESA CCI: A comprehensive assessment using global ground-based observations. Remote Sens. Environ. 231, 111215 (2019).

Snoek, J., Larochelle, H., & Adams, R. P. (2012). Practical bayesian optimization of machine learning algorithms. Advances in neural information processing systems, 25.

Edward, C. (2006). Rasmussen and Christopher KI Williams. Gaussian processes for machine learning. MIT Press, 211, 212.
