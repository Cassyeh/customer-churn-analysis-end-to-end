import pandas as pd
import numpy as np

def create_tenure_lifecycle_features(df):
    """
    Create tenure and customer lifecycle related features.
    Assumes tenure is in months.
    Parameters:
    df(pd.DataFrame): DataFrame containing the data
    """

    df = df.copy()

    # Tenure grouped in 6-month bins: 0–6, 7–12, ...
    df["tenure_group_6m"] = (
        (df["tenure"] // 6) * 6
    ).astype(int)

    # Make it human-readable (e.g., "0-6", "6-12")
    df["tenure_group_6m_label"] = (
        df["tenure_group_6m"].astype(str)
        + "-"
        + (df["tenure_group_6m"] + 6).astype(str)
    )

    # New customer flag (early churn risk)
    df["is_new_customer"] = (df["tenure"] <= 6).astype(int)

    # Loyal customer flag
    df["is_loyal_customer"] = (df["tenure"] >= 24).astype(int)

    # Normalize tenure (useful for linear models): rescales tenure values so that all values fall between 0 and 1
    # tenure of 2 months = 2/72, 72 is maximum tenure in data
    df["tenure_normalized"] = df["tenure"] / df["tenure"].max()

    # Average monthly spend (guard against division by zero), if tenure == 0, no division, default to MonthlyChrges
    df["avg_monthly_spend"] = np.where(
        df["tenure"] > 0,
        df["TotalCharges"] / df["tenure"],
        df["MonthlyCharges"]
    )

    # Lifetime value
    df["lifetime_value"] = df["MonthlyCharges"] * df["tenure"]

    return df

""" # EXAMPLE USAGE
df_lifecycle_features = create_tenure_lifecycle_features(df)
"""


def create_pricing_features(df, avg_monthly_spend_col="avg_monthly_spend"):
    """
    Create pricing and financial features for churn prediction.
    
    Parameters:
    df(pd.DataFrame):customer dataset
    avg_monthly_spend_col: name of precomputed average monthly spend column
    
    Returns:
    df(pd.DataFrame): with added pricing/financial features
    """
    df = df.copy()
    
    # High monthly charge flag (above median), 1 if MonthlyCharges above median, else 0
    median_monthly_charge = df["MonthlyCharges"].median()
    df["high_monthly_charge_flag"] = (df["MonthlyCharges"] > median_monthly_charge).astype(int)
    
    # Monthly vs average spend ratio (to detect sudden increases), sudden price jumps if > 1
    df["monthly_vs_avg_ratio"] = df["MonthlyCharges"] / df[avg_monthly_spend_col]
    
    # Replace inf or NaN if avg_monthly_spend was 0
    df["monthly_vs_avg_ratio"].replace([float("inf"), -float("inf")], 0, inplace=True)
    df["monthly_vs_avg_ratio"].fillna(0, inplace=True)
    
    return df

""" #EXAMPLE USAGE
df_financial_features = create_pricing_features(df, avg_monthly_spend_col="avg_monthly_spend") """

def create_service_engagement_features(df):
    """
    Create service usage and engagement features, including fiber-optic internet risks.
    
    Parameters:
    df(pd.DataFrame): customer dataset
    
    Returns:
    df(pd.DataFrame): with added service/engagement features
    """
    df = df.copy()

    # List of core services
    service_cols = ["PhoneService", "MultipleLines", "InternetService"]
    addon_cols = ["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport"]
    streaming_cols = ["StreamingTV", "StreamingMovies"]
    
    # Convert Yes/No columns to 1/0 for numeric aggregation if not already
    yes_no_cols = service_cols + addon_cols + streaming_cols
    yes_no_cols.remove("InternetService")  # remove it

    for col in yes_no_cols:
        if col in df.columns and df[col].dtype == "object":
            df[col + "_num"] = df[col].apply(lambda x: 1 if x == "Yes" else 0)
    
    # Total number of active services (excluding InternetService=No)
    df["num_active_services"] = df[["PhoneService", "MultipleLines_num"]].sum(axis=1)
    # Count InternetService as active if not 'No'
    df["num_active_services"] += (df["InternetService"] != "No").astype(int)
    
    # Total number of add-ons
    df["num_active_addons"] = df[[col + "_num" for col in addon_cols]].sum(axis=1)
    
    # Streaming engagement
    df["streaming_engagement"] = df[[col + "_num" for col in streaming_cols]].sum(axis=1)

    # Count internet-dependent services
    internet_services_cols = [col + "_num" for col in addon_cols] + [col + "_num" for col in streaming_cols]
    df["num_active_internet_services"] = df[internet_services_cols].sum(axis=1)
        
    # Fiber optics specific features
    fiber_mask = df["InternetService"] == "Fiber optic"

    median_monthly_charge = df["MonthlyCharges"].median()
    
    # If fiber_customer, 1 else 0
    df["fiber_customer_flag"] = fiber_mask.astype(int)

    # Fiber customers paying too much
    df["fiber_high_cost_flag"] = ((fiber_mask) & (df["MonthlyCharges"] > median_monthly_charge)).astype(int)

    # Fiber customers not using a good number of internet services
    df["fiber_low_engagement_flag"] = ((fiber_mask) & (df["num_active_internet_services"] <= 2)).astype(int)  # threshold of 2
    
    return df

""" # EXAMPLE USAGE
df_service_usage_features = create_service_engagement_features(df) """

def create_household_demographic_features(df):
    """
    Create household and demographic features for churn prediction.
    Parameters:
    df(pd.DataFrame): customer dataset
    
    Returns:
    df(pd.DataFrame): with added demographic features
    """
    df = df.copy()
    
    # Senior citizen flag
    if "SeniorCitizen" in df.columns:
        df["is_senior_citizen"] = df["SeniorCitizen"].apply(lambda x: 1 if x == 1 else 0)
    
    # Partner flag
    if "Partner" in df.columns:
        df["has_partner"] = df["Partner"].apply(lambda x: 1 if x == 1 else 0)
    
    # Dependents flag
    if "Dependents" in df.columns:
        df["has_dependents"] = df["Dependents"].apply(lambda x: 1 if x == 1 else 0)
    
    # Household size (1 + partner + dependents)
    df["household_size"] = 1 + df.get("has_partner", 0) + df.get("has_dependents", 0)
    
    # Gender flag (can be used if relevant)
    if "gender" in df.columns:
        df["gender_flag"] = df["gender"].apply(lambda x: 1 if x == "Male" else 0)
        # Males with dependents
        df['male_with_dependents'] = ((df['gender_flag']==1) & (df['household_size']>1)).astype(int)

        # Check churn rate for this group
        churn_rate = df[df['male_with_dependents']==1]['Churn'].mean()
        #print(f"Churn rate for males with dependents: {churn_rate:.2%}")

    return df

""" # EXAMPLE USAGE
df_household_demographics_features = create_household_demographic_features(df) """

def create_contract_payment_features(df):
    """
    Create contract and payment risk features for churn prediction.
    Parameters:
    df(pd.DataFrame): customer dataset
    
    Returns:
    df(pd.DataFrame): with added contract/payment features
    """
    df = df.copy()
    
    # Paperless billing flag
    if "PaperlessBilling" in df.columns:
        df["is_paperless"] = df["PaperlessBilling"].apply(lambda x: 1 if x== 1 else 0)
    
    # Contract type flags
    if "Contract" in df.columns:
        df["is_month_to_month"] = (df["Contract"] == "Month-to-month").astype(int)
        df["is_one_year_contract"] = (df["Contract"] == "One year").astype(int)
        df["is_two_year_contract"] = (df["Contract"] == "Two year").astype(int)
    
    # Payment method flags
    if "PaymentMethod" in df.columns:
        auto_methods = ["Credit card (automatic)", "Bank transfer (automatic)"]
        df["payment_auto_flag"] = df["PaymentMethod"].isin(auto_methods).astype(int)
        df["payment_manual_flag"] = (~df["PaymentMethod"].isin(auto_methods)).astype(int)
    
    return df

""" # EXAMPLE USAGE
df_contract_features = create_contract_payment_features(df) """