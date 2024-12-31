import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
def stat_model(data):
    # task 3

# Load your data
# data = pd.read_csv("your_data.csv")

# Data Preprocessing

    # Handle missing values: Drop rows with missing values in relevant columns
    data.dropna(subset=['TotalPremium', 'TotalClaims', 'Gender', 'Province', 'PostalCode'], inplace=True)

    # Ensure data types are correct
    data['TotalPremium'] = pd.to_numeric(data['TotalPremium'], errors='coerce')
    data['TotalClaims'] = pd.to_numeric(data['TotalClaims'], errors='coerce')
    data['Gender'] = data['Gender'].astype('category')
    data['Province'] = data['Province'].astype('category')
    data['PostalCode'] = data['PostalCode'].astype('category')

    # Calculate margin as the difference between TotalPremium and TotalClaims
    data['Margin'] = data['TotalPremium'] - data['TotalClaims']

    # 1. Risk Differences Across Provinces
    # KPI: TotalClaims across different provinces
    provinces = data.groupby('Province')['TotalClaims'].mean()

    # Perform ANOVA (One-Way Analysis of Variance) for Risk Differences Across Provinces
    provinces_data = [data[data['Province'] == province]['TotalClaims'] for province in data['Province'].unique()]
    anova_provinces = stats.f_oneway(*provinces_data)
    print("ANOVA result for Risk Differences Across Provinces:", anova_provinces)

    # Visualize TotalClaims by Province
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Province', y='TotalClaims', data=data)
    plt.title("Risk Differences Across Provinces (Total Claims)")
    plt.xticks(rotation=90)
    plt.show()

    # 2. Risk Differences Between Zip Codes
    # KPI: TotalClaims across different PostalCodes
    zip_codes = data.groupby('PostalCode')['TotalClaims'].mean()

    # Perform ANOVA for Risk Differences Between Zip Codes
    zip_codes_data = [data[data['PostalCode'] == zip_code]['TotalClaims'] for zip_code in data['PostalCode'].unique()]
    anova_zip_codes = stats.f_oneway(*zip_codes_data)
    print("ANOVA result for Risk Differences Between Zip Codes:", anova_zip_codes)

    # Visualize TotalClaims by PostalCode
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='PostalCode', y='TotalClaims', data=data)
    plt.title("Risk Differences Between Zip Codes (Total Claims)")
    plt.xticks(rotation=90)
    plt.show()

    # 3. Margin (Profit) Differences Between Zip Codes
    # KPI: Calculate the margin as TotalPremium - TotalClaims and test if there are differences across PostalCodes
    zip_margin_data = [data[data['PostalCode'] == zip_code]['Margin'] for zip_code in data['PostalCode'].unique()]
    anova_zip_margin = stats.f_oneway(*zip_margin_data)
    print("ANOVA result for Margin Differences Between Zip Codes:", anova_zip_margin)

    # Visualize Margin Differences by PostalCode
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='PostalCode', y='Margin', data=data)
    plt.title("Margin Differences Across Zip Codes (Profit)")
    plt.xticks(rotation=90)
    plt.show()

    # 4. Risk Differences Between Women and Men
    # KPI: Compare TotalClaims between Gender categories (Women and Men)
    female_claims = data[data['Gender'] == 'Female']['TotalClaims']
    male_claims = data[data['Gender'] == 'Male']['TotalClaims']

    # Perform a t-test for differences in TotalClaims between Women and Men
    t_test_gender = stats.ttest_ind(female_claims, male_claims)
    print("t-test result for Risk Differences Between Women and Men:", t_test_gender)

    # Visualize TotalClaims by Gender
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Gender', y='TotalClaims', data=data)
    plt.title("Risk Differences Between Women and Men (Total Claims)")
    plt.show()

    # Summary of Hypothesis Test Results
    def interpret_result(test_result, test_name):
        p_value = test_result.pvalue
        if p_value < 0.05:
            print(f"{test_name}: Reject the null hypothesis (p-value = {p_value:.4f})")
        else:
            print(f"{test_name}: Fail to reject the null hypothesis (p-value = {p_value:.4f})")

    # Interpret results
    interpret_result(anova_provinces, "Risk Differences Across Provinces")
    interpret_result(anova_zip_codes, "Risk Differences Between Zip Codes")
    interpret_result(anova_zip_margin, "Margin Differences Between Zip Codes")
    interpret_result(t_test_gender, "Risk Differences Between Women and Men")
