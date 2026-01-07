"""
Data Cleaning and Preparation for Customer Churn Analysis
- Handle missing values
- Fix data types
- Validate target variable
- Save cleaned data to 'data/processed/'
"""
import os
import pandas as pd

def clean_data(raw_df, target_variable):
    """
    Perform data cleaning, type fixes, validates target variable.
    Parameters:
    raw_df(pd.DataFrame): A pandas DataFrame containing the data to be cleaned.
    target_variable(str): Column name of the target variable to be validated
    
    Returns:
    cleaned_df(pd.DataFrame): The cleaned pandas dataframe.
    """
    # Print original datatypes
    print("📊 Column Data Types Before Cleaning:")
    print(raw_df.dtypes)
    print("-" * 50)

    # 1. Strip column names of extra spaces
    raw_df.columns = raw_df.columns.str.strip()
    
    # 2. Validate Target variable
    if target_variable not in raw_df.columns:
        raise ValueError("Target variable 'Churn' is missing from the dataset")
    # Check that it contains both 'Yes' and 'No'
    unique_values = set(raw_df[target_variable].dropna().unique())
    if not unique_values.issuperset({'Yes', 'No'}):
        raise ValueError(f"Target variable 'Churn' must contain 'Yes' and 'No'. Found: {unique_values}")
    
    # 3. Drop duplicates
    cleaned_df = raw_df.drop_duplicates(keep='first')  # no subset specified

    # 4. Print only columns with missing values
    missing_summary = cleaned_df.isnull().sum()
    missing_summary = missing_summary[missing_summary > 0]
    print(missing_summary)
    if missing_summary.empty:
        # Count empty strings in each column
        empty_counts = cleaned_df.apply(
            lambda col: (col.str.strip() == '').sum() if col.dtype == 'object' else 0
        ) #only columns with dtype object (strings) can contain empty strings ('')
        empty_counts = empty_counts[empty_counts > 0]  # only show columns with >0 empty strings
        print(empty_counts)

    print("Data cleaning complete.")
    return cleaned_df

# 2. Turn Booleans into 0 and 1 values as this is mandatory for modeling
def convert_yes_no_columns(cleaned_df):
    """
    Convert columns containing ONLY 'Yes' and 'No' values to binary (1/0).
    Parameters
    cleaned_df(pd.DataFrame): Input DataFrame

    Returns
    zero_one_df(pd.DataFrame): DataFrame with Yes/No columns converted to 1/0
    """
    zero_one_df = cleaned_df.copy()

    for col in zero_one_df.columns:
        # Get unique non-null values
        unique_vals = set(zero_one_df[col].dropna().unique())

        # Check if column contains ONLY Yes/No
        if unique_vals == {'Yes', 'No'}:
            zero_one_df[col] = zero_one_df[col].map({'Yes': 1, 'No': 0})
            print(f"Converted '{col}' to binary")

    return zero_one_df
#Yes/No features were mapped to binary numeric values, allowing pandas to infer integer types.

def impute_zero_tenure_values(df, target_col, tenure_col='tenure', threshold=0.1):
    """
    Impute missing values in a numeric column based on zero-tenure logic.
    - Converts the target column to numeric
    - Sets target column = 0 where tenure = 0
    - Raises an error if more than `threshold` fraction of values are non-numeric
    - Validates no missing values remain after imputation

    Parameters
    df(pd.DataFrame): Input DataFrame
    target_col(str): Column to be cleaned and imputed (e.g. 'TotalCharges')
    tenure_col(str, optional): Tenure column name (default is 'tenure')
    threshold(float, optional): Maximum fraction of non-numeric values allowed before raising an error (default 0.1)
    
    Returns
    filled_df(pd.DataFrame): Filled DataFrame
    """
    filled_df = df.copy()

    # Check columns exist
    if target_col not in filled_df.columns:
        raise KeyError(f"Column '{target_col}' not found in DataFrame.")
    if tenure_col not in filled_df.columns:
        raise KeyError(f"Tenure column '{tenure_col}' not found in DataFrame.")

    # --- Step 1: Convert column to numeric, invalid values become NaN
    numeric_conversion = pd.to_numeric(filled_df[target_col], errors='coerce')

    # --- Step 2: Identify which values are NaN after conversion
    is_nan_after_conversion = numeric_conversion.isna()

    # --- Step 3: Identify values that were originally present
    not_missing_originally = filled_df[target_col].notna()

    # --- Step 4: Combine masks to find non-numeric values
    non_numeric_mask = is_nan_after_conversion & not_missing_originally

    # --- Step 5: Calculate fraction of non-numeric values
    non_numeric_fraction = non_numeric_mask.sum() / len(filled_df)

    if non_numeric_fraction > threshold:
        raise ValueError(
            f"❌ Column '{target_col}' contains {non_numeric_fraction:.2%} "
            f"non-numeric values, which exceeds the threshold of {threshold:.2%}."
        )

    # --- Step 6: Convert column to numeric
    filled_df[target_col] = numeric_conversion

    # --- Step 7: Impute values where tenure = 0
    zero_tenure_mask = filled_df[tenure_col] == 0
    filled_df.loc[zero_tenure_mask, target_col] = 0

    # --- Step 8: Validate no missing values remain
    if filled_df[target_col].isna().sum() > 0:
        raise ValueError(
            f"❌ Column '{target_col}' still contains missing values after imputation."
        )

    print(f"'{target_col}' cleaned and imputed using {tenure_col} logic.")
    print(filled_df.dtypes)

    return filled_df
# These customers of 0 tenure have blank total charges in original df, may affect ML model, no charges = 0