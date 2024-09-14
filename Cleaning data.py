# File: data_cleaning.py
import pandas as pd
import numpy as np

# Load dataset (JSON format)
df = pd.read_csv("menu.csv")

# 1. Inspect the dataset
print("Dataset Info:\n", df.info())
print("First few rows of the dataset:\n", df.head())
print("Dataset statistics:\n", df.describe(include='all'))

# 2. Handle Missing Data
# Checking for missing values
missing_values = df.isnull().sum()
print("Missing values in each column:\n", missing_values)

# Option 1: Impute missing values with mean (for numerical columns only)
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

# Option 2: Drop rows or columns with excessive missing data
# Uncomment the following line to drop rows with any missing data
# df.dropna(inplace=True)

# 3. Handle Unhashable Types
# Convert non-hashable types (like dictionaries) to strings
for col in df.columns:
    if df[col].apply(lambda x: isinstance(x, (dict, list))).any():
        df[col] = df[col].apply(str)

# 4. Remove Duplicates
print("Number of duplicates before removal: ", df.duplicated().sum())
df.drop_duplicates(inplace=True)
print("Number of duplicates after removal: ", df.duplicated().sum())

# 5. Standardization (Example: converting a 'date' column to a datetime type)
# Check if 'date' column exists and convert to datetime if present
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Example: Ensuring consistency in 'price' column (if present) by converting to float
if 'price' in df.columns:
    df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)

# 6. Detecting and Handling Outliers (Using Interquartile Range for numerical columns)
Q1 = df[numeric_cols].quantile(0.25)
Q3 = df[numeric_cols].quantile(0.75)
IQR = Q3 - Q1

# Removing outliers outside 1.5*IQR range for numerical columns only
df = df[~((df[numeric_cols] < (Q1 - 1.5 * IQR)) | (df[numeric_cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

# 7. Ensure Data Integrity
# Example: Remove negative values from 'age' column (if exists)
if 'age' in df.columns:
    df = df[df['age'] >= 0]

# Saving cleaned dataset
df.to_csv('cleaned_dataset.csv', index=False)
print("Data cleaning complete. Cleaned dataset saved as 'cleaned_dataset.csv'.")
