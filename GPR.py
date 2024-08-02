import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from bayes_opt import BayesianOptimization
import pandas as pd
from MetricsCalculator import MetCalculator

class GPRModel:
    
    def __init__(self, X, y):
        
        # Split data into training and testing sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Initialize hyperparameters
        self.best_length_scale = None
        
        self.best_alpha = None
        
        self.best_gpr = None

    def gpr_cv(self, length_scale, alpha):
        
        # Define the kernel with the given length_scale
        kernel = RBF(length_scale=length_scale)
        
        # Initialize Gaussian Process Regressor with the given alpha
        gpr = GaussianProcessRegressor(kernel=kernel, alpha=alpha, n_restarts_optimizer=10, random_state=42)
        
        # Initialize K-Fold cross-validation
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        
        # Compute cross-validation score
        scores = cross_val_score(gpr, self.X_train, self.y_train, cv=kf, scoring='r2')
        
        # Return the mean of the cross-validation scores
        return np.mean(scores)

    def optimize_hyperparameters(self):
        
        # Define the optimizer for Bayesian optimization
        optimizer = BayesianOptimization(
            
            f=self.gpr_cv,
            
            pbounds={'length_scale': (1e-5, 1e5), 'alpha': (1e-5, 1e5)},
            
            random_state=42,
        )
        
        # Perform optimization
        optimizer.maximize(init_points=500, n_iter=20)
        
        # Extract the best hyperparameters
        self.best_length_scale = optimizer.max['params']['length_scale']
        
        self.best_alpha = optimizer.max['params']['alpha']
        
        print(f"Optimized length_scale: {self.best_length_scale}")
        
        print(f"Optimized alpha: {self.best_alpha}")

    def train(self):
        
        # Define the kernel with the optimized length_scale
        kernel = RBF(length_scale=self.best_length_scale)
        
        # Initialize Gaussian Process Regressor with the optimized alpha
        self.best_gpr = GaussianProcessRegressor(kernel=kernel, alpha=self.best_alpha, n_restarts_optimizer=10, random_state=42)
        
        # Fit the model on the training data
        self.best_gpr.fit(self.X_train, self.y_train)
        
        # Predict on the training data
        self.y_train = pd.Series(self.y_train)
        
        y_train_pred = self.best_gpr.predict(self.X_train)
        
        self.y_train_pred = pd.Series(y_train_pred)
        
        # Predict on the test data
        self.y_test = pd.Series(self.y_test)
        
        y_test_pred = self.best_gpr.predict(self.X_test)
        
        self.y_test_pred = pd.Series(y_test_pred)

    def evaluate(self):
        
        # Initialize the metrics calculator
        met_calculator = MetCalculator()
        
        # Evaluate training performance
        mean_percentage_bias_train, std_percentage_bias_train, ubrmse_train = met_calculator.ubrmse(self.y_train, self.y_train_pred)
        
        nse_train = met_calculator.nse(self.y_train, self.y_train_pred)
        
        correlation_train = met_calculator.correlation(self.y_train, self.y_train_pred)

        print(f"UBMRMSE (Training): {ubrmse_train:.3f}")
        
        print(f"Mean Percentage Bias (Training): {mean_percentage_bias_train:.3f} ± {std_percentage_bias_train:.3f}")
        
        print(f"NSE (Training): {nse_train:.3f}")
        
        print(f"Correlation (Training): {correlation_train:.3f}")
        
        # Evaluate testing performance
        mean_percentage_bias_test, std_percentage_bias_test, ubrmse_test = met_calculator.ubrmse(self.y_test, self.y_test_pred)
        
        nse_test = met_calculator.nse(self.y_test, self.y_test_pred)
        
        correlation_test = met_calculator.correlation(self.y_test, self.y_test_pred)

        print(f"UBMRMSE (Testing): {ubrmse_test:.3f}")
        
        print(f"Mean Percentage Bias (Testing): {mean_percentage_bias_test:.3f} ± {std_percentage_bias_test:.3f}")
        
        print(f"NSE (Testing): {nse_test:.3f}")
        
        print(f"Correlation (Testing): {correlation_test:.3f}")
