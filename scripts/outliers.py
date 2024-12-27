import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Example dataset
# Replace 'data.csv' with the actual path to your dataset
# data = pd.read_csv('data.csv')
def outliers(data):
# Numerical columns to check for outliers
    numerical_columns = ['TotalPremium', 'TotalClaim']  # Replace with relevant columns in your dataset

    # Iterate through each numerical column and create a box plot
    for column in numerical_columns:
        if column not in data.columns:
            print(f"Column {column} not found in the dataset. Skipping.")
            continue
        
        # Box plot for outlier detection
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=data, y=column, palette='Set2')
        plt.title(f'Box Plot for {column}')
        plt.ylabel(column)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

        # Calculate interquartile range (IQR)
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1

        # Define lower and upper bounds for outlier detection
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Identify outliers
        outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
        print(f"Number of outliers detected in {column}: {outliers.shape[0]}")
        print(outliers)
