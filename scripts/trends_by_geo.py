import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
def trends(data):

    # Example dataset
    # Replace 'data.csv' with the actual path to your dataset
    # data = pd.read_csv('data.csv')

    # Ensure 'TransactionMonth' is in datetime format
    data['TransactionMonth'] = pd.to_datetime(data['TransactionMonth'], errors='coerce')

    # Verify relevant columns for analysis
    columns_of_interest = ['PostalCode', 'TransactionMonth', 'CoverType', 'TotalPremium', 'make']
    for col in columns_of_interest:
        if col not in data.columns:
            raise ValueError(f"Column {col} is missing in the dataset.")

    # Group data by geographical region (PostalCode) and cover type
    cover_type_trends = data.groupby(['PostalCode', 'CoverType'])['TotalPremium'].mean().reset_index()

    # Plot premium trends by cover type over geography
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=cover_type_trends, 
        x='PostalCode', 
        y='TotalPremium', 
        hue='CoverType', 
        palette='tab10'
    )
    plt.title('Average Premium by Cover Type Across Postal Codes')
    plt.xlabel('Postal Code')
    plt.ylabel('Average Premium')
    plt.xticks(rotation=45)
    plt.legend(title='Cover Type')
    plt.tight_layout()
    plt.show()

    # Analyze trends in auto makes by geography
    auto_make_trends = data.groupby(['PostalCode', 'make'])['TotalPremium'].mean().reset_index()

    # Filter top 10 most common auto makes for clarity
    top_auto_makes = data['make'].value_counts().head(10).index
    filtered_auto_make_trends = auto_make_trends[auto_make_trends['make'].isin(top_auto_makes)]

    # Plot premium trends by auto make over geography
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=filtered_auto_make_trends, 
        x='PostalCode', 
        y='TotalPremium', 
        hue='make', 
        palette='viridis'
    )
    plt.title('Average Premium by Auto Make Across Postal Codes')
    plt.xlabel('Postal Code')
    plt.ylabel('Average Premium')
    plt.xticks(rotation=45)
    plt.legend(title='Auto Make', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    # Time series analysis of premium trends over geography
    data['YearMonth'] = data['TransactionMonth'].dt.to_period('M')

    # Group data by YearMonth and PostalCode for time trends
    time_trends = data.groupby(['YearMonth', 'PostalCode'])['TotalPremium'].mean().reset_index()

    # Ensure 'YearMonth' is in string format for plotting
    time_trends['YearMonth'] = time_trends['YearMonth'].astype(str)

    # Verify 'TotalPremium' contains valid numeric data
    time_trends['TotalPremium'] = pd.to_numeric(time_trends['TotalPremium'], errors='coerce')

    # Drop rows with NaN values in critical columns (if any)
    time_trends.dropna(subset=['TotalPremium', 'YearMonth'], inplace=True)

    # Plot the line graph for monthly premium trends
    plt.figure(figsize=(12, 6))
    sns.lineplot(
        data=time_trends,
        x='YearMonth',
        y='TotalPremium',
        hue='PostalCode',
        palette='tab20',
        marker='o'
    )
    plt.title('Monthly Premium Trends Across Postal Codes')
    plt.xlabel('Year-Month')
    plt.ylabel('Average Premium')
    plt.xticks(rotation=45)
    plt.legend(title='Postal Code', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
