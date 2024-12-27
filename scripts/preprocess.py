def preprocess(data):
# Display basic information about the dataset
    print("Dataset Info:")
    print(data.info())

    # Preview the dataset 
    print("\nFirst 5 Rows:")
    print(data.head())

    num_col=['TotalPremium',
        'TotalClaims']

    # # Generate descriptive statistics for numerical columns
    numerical_stats = data[num_col].describe()
    print(numerical_stats)
    print("\nData Types of Columns:")
    print(data.dtypes)


    # Check for missing values in each column
    missing_values = data.isnull().sum()

    # Display the results
    print("\nMissing Values in Each Column:")
    print(missing_values)

