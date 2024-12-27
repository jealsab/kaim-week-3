import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
def visualization(data):
    
    plt.figure(figsize=(12, 6))
    sns.violinplot(
        data=data, 
        x='CoverType', 
        y='TotalPremium', 
        palette='coolwarm', 
        inner='quartile'
    )
    plt.title('Distribution of Premiums by Cover Type', fontsize=16)
    plt.xlabel('Cover Type', fontsize=12)
    plt.ylabel('Total Premium', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    # Calculate the average premium for each auto make
    avg_premium_by_make = data.groupby('make')['TotalPremium'].mean().sort_values(ascending=False).head(10).reset_index()

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=avg_premium_by_make, 
        x='TotalPremium', 
        y='make', 
        palette='viridis'
    )
    plt.title('Top 10 Auto Makes by Average Premium', fontsize=16)
    plt.xlabel('Average Premium', fontsize=12)
    plt.ylabel('Auto Make', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
    time_trends = data.groupby(['YearMonth', 'PostalCode','CoverType'])['TotalPremium'].mean().reset_index()
    
    # Convert YearMonth to string for plotting
    time_trends['YearMonth'] = time_trends['YearMonth'].astype(str)

    plt.figure(figsize=(14, 7))
    sns.lineplot(
        data=time_trends, 
        x='YearMonth', 
        y='TotalPremium', 
        hue='CoverType', 
        marker='o', 
        palette='tab10'
    )
    plt.title('Premium Trends Over Time by Cover Type', fontsize=16)
    plt.xlabel('Year-Month', fontsize=12)
    plt.ylabel('Average Premium', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title='Cover Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
