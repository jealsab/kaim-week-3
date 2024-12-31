import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# Load the dataset (replace 'data.csv' with your actual file path)
# data = pd.read_csv('data.csv')
def data_clean(data):
    # =======================
    # Data Preparation
    # =======================
    # 1. Handling Missing Data
    # Numerical Columns: Impute missing values with the median
    num_cols = data.select_dtypes(include=['float64', 'int64']).columns
    num_imputer = SimpleImputer(strategy='median')
    data[num_cols] = num_imputer.fit_transform(data[num_cols])

    # Categorical Columns: Impute missing values with the mode
    cat_cols = data.select_dtypes(include=['object', 'category']).columns
    cat_imputer = SimpleImputer(strategy='most_frequent')
    data[cat_cols] = cat_imputer.fit_transform(data[cat_cols])

    # =======================
    # Feature Engineering
    # =======================
    # Example 1: Create 'VehicleAge' from 'RegistrationYear' (assuming current year is 2024)
    if 'RegistrationYear' in data.columns:
        data['VehicleAge'] = 2024 - data['RegistrationYear']

    # Example 2: Create 'ClaimRate' as a ratio of 'TotalClaims' to 'SumInsured'
    if 'TotalClaims' in data.columns and 'SumInsured' in data.columns:
        data['ClaimRate'] = data['TotalClaims'] / (data['SumInsured'] + 1e-6)  # Avoid division by zero

    # =======================
    # Encoding Categorical Data
    # =======================
    print(data.columns)
    # One-Hot Encoding for nominal categorical variables
    nominal_cols = ['MainCrestaZone', 'CoverType', 'Bank']  # Replace with your nominal columns
    data = pd.get_dummies(data, columns=nominal_cols, drop_first=True)

    # Label Encoding for binary/ordinal categorical variables
    binary_cols = ['Gender', 'MaritalStatus', 'IsVATRegistered']  # Replace with your binary columns
    label_encoder = LabelEncoder()

    for col in binary_cols:
        # Ensure consistent data types (convert bool to int and str to string)
        if data[col].dtype == 'bool':
            data[col] = data[col].astype(int)  # Convert boolean to integers (True -> 1, False -> 0)
        else:
            data[col] = data[col].astype(str)  # Convert other types to string

        # Apply label encoding after ensuring the column is consistent
        data[col] = label_encoder.fit_transform(data[col])

    # =======================
    # Train-Test Split
    # =======================
    # Define the feature set (X) and target variables (y)
    X = data.drop(columns=['TotalPremium', 'TotalClaims'])  # Features
    y = data[['TotalPremium', 'TotalClaims']]  # Targets

    # Split the data into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Output dataset shapes to verify
    print("Train Features Shape:", X_train.shape)
    print("Test Features Shape:", X_test.shape)
    print("Train Target Shape:", y_train.shape)
    print("Test Target Shape:", y_test.shape)
