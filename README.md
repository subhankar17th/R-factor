**Rainfall erosivity**, often denoted as the R-factor, is one of the most critical factors influencing erosion processes. Estimating the R-factor from high-resolution satellite and reanalysis datasets requires the identification of erosive events and subsequent computation of erosivity for each time interval.

The MATLAB code provided in this repository effectively computes rainfall erosivity values for each grid using 30-minute and 60-minute rainfall data. However, users are requested to first prepare all datasets in array format before utilizing the MATLAB function to estimate rainfall erosivity. 

The code uses the proposed method of Renard et al. (1997) for the identification of erosive storms and McGregor et al. (1995 & 1976) method for the rainfall erosivity estimation.
The estimated rainfall erosivity from the three datasets using the MATLAB codes has been provided in the https://doi.org/10.5281/zenodo.8406086. 

The **MetricsCalculator** is a Python class built to estimate metrics such as Percentage Error, Unbiased Root Mean Squared Error, Pearson Correlation Coefficient, and Nash–Sutcliffe Efficiency between observed and predicted datasets using the formula of Moriasi et al. (2007) and Ma et al. (2019).


**References**:

Renard, K., Foster, G., Weesies, G., McCool, D. & Yoder, D. Predicting soil erosion by water: a guide to conservation planning with the Revised Universal Soil Loss Equation (RUSLE). Agric. Handb. No. 703 404 (1997).

McGregor, K. C., Bingner, R. L., Bowie, A. J. & Foster, G. R. Erosivity index values for northern Mississippi. Trans. - Am. Soc. Agric. Eng. 38, 1039–1047 (1995).

McGregor, K. C. & Mutchler, C. K. Status of the R factor in northern Mississippi. Soil Eros. Predict. Control 135–142 (1976).

Moriasi, D. N. et al. Model evaluation guidelines for systematic quantification of accuracy in watershed simulations. Trans. ASABE 50, 885–900 (2007).

Ma, H. et al. Satellite surface soil moisture from SMAP, SMOS, AMSR2, and ESA CCI: A comprehensive assessment using global ground-based observations. Remote Sens. Environ. 231, 111215 (2019).
