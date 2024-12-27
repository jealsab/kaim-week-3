import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def univariate_analysis(data):

    # Numerical columns
    num_columns = [
        'TotalPremium', 'TotalClaims', 'SumInsured', 'TermFrequency', 
        'CalculatedPremiumPerTerm', 'ExcessSelected', 'kilowatts', 
        'cubiccapacity', 'NumberOfDoors', 'CustomValueEstimate', 
        'CapitalOutstanding', 'NumberOfVehiclesInFleet'
    ]

    # Categorical columns
    cat_columns = [
        'PolicyID', 'TransactionMonth', 'IsVATRegistered', 'Citizenship', 'LegalType', 
        'Language', 'Bank', 'AccountType', 'MaritalStatus', 'Gender', 'Country', 
        'Province', 'VehicleType', 'RegistrationYear', 'make', 'Model', 'CoverType', 
        'CoverGroup', 'Product'
    ]


    for col in num_columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    # Univariate analysis - Histograms for numerical columns
    plt.figure(figsize=(15, 10))
    for i, col in enumerate(num_columns, 1):
        plt.subplot(3, 4, i)
        data[col].dropna().hist(bins=30, edgecolor='black')
        plt.title(f'Histogram of {col}')
        plt.tight_layout()

    plt.show()

    ## Univariate analysis - Bar charts for categorical columns
    # s= data.head()

    categorical_columns = data.select_dtypes(include=['object', 'category']).columns

    # # Univariate Analysis for Numerical Columns
    # plt.figure(figsize=(15, len(numerical_columns) * 2.5))
    # for i, col in enumerate(numerical_columns, 1):
    #     plt.subplot(len(numerical_columns), 1, i)
    #     sns.histplot(data[col], kde=True, bins=30, color="blue")
    #     plt.title(f'Distribution of {col}')
    #     plt.xlabel(col)
    #     plt.ylabel('Frequency')
    #     plt.tight_layout()
    # plt.show()

    # Univariate Analysis for Categorical Columns
    # Function to plot top N categories for better visualization
    def plot_top_categories(data, col, top_n=10):
        top_categories = data[col].value_counts().nlargest(top_n)
        sns.barplot(x=top_categories.index, y=top_categories.values, palette="Set2")
        plt.title(f'Top {top_n} Categories in {col}')
        plt.xlabel(col)
        plt.ylabel('Count')
        plt.xticks(rotation=90, fontsize=10)

    # Improved Univariate Analysis for Categorical Columns
    rows = len(categorical_columns)
    cols = 3  # Set a fixed number of columns for subplot grid
    plot_rows = (rows // cols) + 1

    plt.figure(figsize=(15, plot_rows * 3))
    for i, col in enumerate(categorical_columns, 1):
        plt.subplot(plot_rows, cols, i)
        # Show top 10 categories if the column has many unique values
        if data[col].nunique() > 10:
            plot_top_categories(data, col, top_n=10)
        else:
            sns.countplot(x=data[col], palette="Set2")
            plt.title(f'Bar Chart of {col}')
            plt.xlabel(col)
            plt.ylabel('Count')
            plt.xticks(rotation=90, fontsize=10)
        plt.tight_layout()
    plt.show()
    
def bivariate_analysis(data):

    # Check if the equivalent of 'ZipCode' is 'PostalCode'
    zip_code_col = 'PostalCode'

    # Ensure TransactionMonth is in datetime format
    data['TransactionMonth'] = pd.to_datetime(data['TransactionMonth'], errors='coerce')

    # Sort by ZipCode and TransactionMonth for consistency
    data.sort_values(by=[zip_code_col, 'TransactionMonth'], inplace=True)

    # Calculate monthly changes for TotalPremium and TotalClaims
    data['Change_TotalPremium'] = data.groupby(zip_code_col)['TotalPremium'].diff()
    data['Change_TotalClaims'] = data.groupby(zip_code_col)['TotalClaims'].diff()

    # Drop rows with NaN values in the change columns
    data = data.dropna(subset=['Change_TotalPremium', 'Change_TotalClaims'])

    # Descriptive statistics for monthly changes
    print("\nDescriptive Statistics for Monthly Changes:")
    print(data[['Change_TotalPremium', 'Change_TotalClaims']].describe())

    # Correlation analysis
    corr_matrix = data[['Change_TotalPremium', 'Change_TotalClaims']].corr()
    print("\nCorrelation Matrix:")
    print(corr_matrix)

    # Plot the correlation matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix')
    plt.show()

    # Scatter plot to explore relationships
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x='Change_TotalPremium', 
        y='Change_TotalClaims', 
        hue=zip_code_col, 
        palette='viridis', 
        data=data
    )
    plt.title('Monthly Changes: TotalPremium vs TotalClaims (by ZipCode)')
    plt.xlabel('Change in TotalPremium')
    plt.ylabel('Change in TotalClaims')
    plt.legend(title=zip_code_col, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

