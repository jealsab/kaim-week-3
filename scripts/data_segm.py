import pandas as pd
from scipy import stats

# Assuming 'data' is the DataFrame with the relevant columns
def segmentation(data):
# 1. Define the feature for segmentation (e.g., CoverCategory or CoverType)
    feature_column = 'CoverCategory'

    # If the feature has more than two classes, choose two categories to create the groups
    categories_to_use = ['Standard', 'Premium']  # Replace with the categories you want to compare

    # Split the data into Group A (Control) and Group B (Test)
    group_a = data[data[feature_column] == categories_to_use[0]]
    group_b = data[data[feature_column] == categories_to_use[1]]

    # 2. Check statistical equivalence between Group A and Group B for client attributes, car properties, and plan information
    attributes = [
        'IsVATRegistered', 'Citizenship', 'LegalType', 'Title', 'Language', 'Bank', 'AccountType', 
        'MaritalStatus', 'Gender', 'Country', 'Province', 'PostalCode', 'MainCrestaZone', 'SubCrestaZone',
        'ItemType', 'mmcode', 'VehicleType', 'RegistrationYear', 'make', 'Model', 'Cylinders', 
        'cubiccapacity', 'kilowatts', 'bodytype', 'NumberOfDoors', 'VehicleIntroDate', 'CustomValueEstimate',
        'AlarmImmobiliser', 'TrackingDevice', 'CapitalOutstanding', 'NewVehicle', 'WrittenOff', 'Rebuilt', 
        'Converted', 'CrossBorder', 'NumberOfVehiclesInFleet', 'SumInsured', 'TermFrequency', 
        'CalculatedPremiumPerTerm', 'ExcessSelected', 'CoverCategory', 'CoverType', 'CoverGroup', 
        'Section', 'Product', 'StatutoryClass', 'StatutoryRiskType', 'TotalPremium', 'TotalClaims'
    ]

    # Perform equivalence checks for each attribute
    for attribute in attributes:
        # For categorical variables, perform Chi-Square test
        if data[attribute].dtype == 'category' or data[attribute].dtype == 'object':  
            contingency_table = pd.crosstab(data[attribute], data[feature_column])
            chi2, p_value, _, _ = stats.chi2_contingency(contingency_table)
            print(f"Chi-Square test for {attribute}: p-value = {p_value:.4f}")
            if p_value < 0.05:
                print(f"{attribute} is statistically different between the two groups!")
        else:  # For continuous variables, use T-test
            group_a_attr = group_a[attribute]
            group_b_attr = group_b[attribute]
            t_stat, p_value = stats.ttest_ind(group_a_attr, group_b_attr, nan_policy='omit')
            print(f"T-test for {attribute}: p-value = {p_value:.4f}")
            if p_value < 0.05:
                print(f"{attribute} is statistically different between the two groups!")

    # 3. If there are significant differences in any attribute, we should reconsider how we split the groups
