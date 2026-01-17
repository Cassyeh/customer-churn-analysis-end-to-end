import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils import download_file_from_google_drive, load_data_csv, save_data
from data_cleaning import clean_data, convert_yes_no_columns, impute_zero_tenure_values
from exploratory_analysis import plot_churn_counts, plot_service_vs_churn, plot_tenure_eda, plot_contract_eda
from feature_engineering_all import create_all_features, save_features_to_excel, feature_correlation

file_id = "1763OlxZ9Fun9-x3GYi6BUu_7ot9AfEkJ"   # replace with  file ID
destination = "./data/raw/telco_customer_churn_data.csv"  # local file name

download_file_from_google_drive(file_id, destination)

# Paths
RAW_DATA_PATH = destination
PROCESSED_DATA_PATH = "./data/processed/telco_customer_churn_data_cleaned.csv"

# Load Data
raw_df = load_data_csv(RAW_DATA_PATH)

# Transform Data
clean_df = clean_data(raw_df, "Churn")
zero_one_bool_df = convert_yes_no_columns(clean_df)
filled_total_charges_df = impute_zero_tenure_values(zero_one_bool_df, "TotalCharges")

save_data(filled_total_charges_df, PROCESSED_DATA_PATH)

#EDA
churn_visual_path = './visuals/eda/churn_count_eval.png'
plot_churn_counts(filled_total_charges_df, 'Churn', churn_visual_path)

service_col = ["PhoneService"]
phone_service_visual_path = './visuals/eda/phone_service_churned_eval.png'
phone_service_title = "Phone Service vs Churn Rate"
plot_service_vs_churn(filled_total_charges_df, service_col,title=phone_service_title,save_path=phone_service_visual_path)

service_col = ["InternetService"]
internet_service_visual_path = './visuals/eda/internet_service_churned_eval.png'
internet_service_title = "Internet Service vs Churn Rate"
plot_service_vs_churn(filled_total_charges_df, service_col,title=internet_service_title,save_path=internet_service_visual_path)

addon_cols = [
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies"
]
add_ons_service_visual_path = './visuals/eda/add_ons_service_churned_eval.png'
add_ons_service_title = f"{addon_cols} Service vs Churn Rate"
plot_service_vs_churn(filled_total_charges_df, service_col=addon_cols, eligible_condition = "InternetService != 'No'", title=add_ons_service_title,save_path=add_ons_service_visual_path)

tenure_visual_path = './visuals/eda/tenure_count_eval.png'
plot_tenure_eda(filled_total_charges_df, title="Count by Tenure", save_path=tenure_visual_path)

contract_visual_path = './visuals/eda/contract_churned_eval.png'
plot_contract_eda(filled_total_charges_df, title="Contract vs Churn Rate", save_path=contract_visual_path)

# Feature Engineering
FEATURES_DATA_PATH = "./data/processed/telco_customer_churn_features_data.xlsx"
df_features, columns_to_add, sheet_names = create_all_features(filled_total_charges_df)

save_features_to_excel(df_features, columns_to_add, FEATURES_DATA_PATH, sheet_names)

ALL_FEATURES_DATA_PATH = "./data/processed/telco_customer_churn_all_features_data.csv"
save_data(df_features, ALL_FEATURES_DATA_PATH)

corr_cols = ["Churn", "tenure_normalized", "avg_monthly_spend", 
             "lifetime_value", "num_active_services", "fiber_customer_flag",
             "household_size", "is_month_to_month", "payment_auto_flag"]
weighted_features_df = df_features[corr_cols]
features_visual_path = './visuals/eda/features_correlation_eval.png'
feature_correlation (weighted_features_df, features_visual_path)