import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

from src.feature_engineering import create_tenure_lifecycle_features, create_pricing_features, create_service_engagement_features,create_household_demographic_features, create_contract_payment_features

def create_all_features(df):
    """
    Apply all feature engineering functions and return a combined dataframe.
    Parameters:
    df(pd.DataFrame): customer dataset
    
    Returns:
    df(pd.DataFrame): with all features added
    """
    df = df.copy()
    sheet_names = []
    feature_cols = []
    
    # --- Tenure & Customer Lifecycle ---
    df_lifecycle_features = create_tenure_lifecycle_features(df)
    sheet_names.append("Lifecycle Features")
    lifecycle_cols = list(set(df_lifecycle_features.columns))
    feature_cols.append(lifecycle_cols)

    # Pricing
    df_financial_features = create_pricing_features(df_lifecycle_features)
    sheet_names.append("Financial Features")
    financial_cols = list(set(df_financial_features.columns) - set(df_lifecycle_features.columns))
    feature_cols.append(financial_cols)

    # --- Service Usage & Engagement ---
    df_service_usage_features = create_service_engagement_features(df_financial_features)
    sheet_names.append("Service_Usage Features")
    service_cols = list(set(df_service_usage_features.columns) - set(df_financial_features.columns))
    feature_cols.append(service_cols)
    
    # --- Household & Demographics ---
    df_household_demographics_features = create_household_demographic_features(df_service_usage_features)
    sheet_names.append("Household_Demographic Features")
    demographic_cols = list(set(df_household_demographics_features.columns) - set(df_service_usage_features.columns))
    feature_cols.append(demographic_cols)
    
    # --- Contract & Payment ---
    df_contract_payment_features = create_contract_payment_features(df_household_demographics_features)
    sheet_names.append("Contract_PaymentType Features")
    contract_payment_cols = list(set(df_contract_payment_features.columns) - set(df_household_demographics_features.columns))
    feature_cols.append(contract_payment_cols)
    
    return df_contract_payment_features, feature_cols, sheet_names

""" # EXAMPLE USAGE
# Generate all features
df_features = create_all_features(raw_df, file_path) """


def save_features_to_excel(df, columns_to_add, feature_file_path, sheet_names):
    """
    Save each feature group to a separate Excel sheet.
    
    Parameters:
    df(pd.DataFrame): full dataframe with features
    columns_to_add: list of columns to add
    feature_file_path(str): path to save Excel with feature
    sheet_names(list): list of names of sheet
    """
    os.makedirs(os.path.dirname(feature_file_path), exist_ok=True)
    
    with pd.ExcelWriter(feature_file_path) as writer:
        for i in range(0, len(sheet_names)):
            df[columns_to_add[i]].to_excel(writer, sheet_name=sheet_names[i], index=False)
            print(f"{sheet_names[i]} saved to Excel at {feature_file_path}")


def feature_correlation (numeric_features_df, save_path):
    """
    Correlation heatmap for important features
    
    Parameters:
    numeric_features_df(pd.DataFrame): dataframe with select features
    save_path(str, default):'visuals/eda': Path to save the plot image
    """
    corr = numeric_features_df.corr()

    # --- Plot ---
    fig, ax1 = plt.subplots(figsize=(12,9))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap="coolwarm", center=0, linewidths=0.5, vmin=-1, vmax=1)
    plt.title("Feature Correlation Heatmap")

    plt.tight_layout()
    
    # --- Create folder if it doesn't exist ---
    os.makedirs(os.path.dirname(save_path), exist_ok=True) 
    # --- Save plot ---
    plt.savefig(save_path, dpi=500, bbox_inches='tight')
    print(f"Features HeatMap saved to {save_path}")
