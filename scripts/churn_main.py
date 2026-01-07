import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.utils import download_file_from_google_drive, load_data_csv, save_data
from data_cleaning import clean_data, convert_yes_no_columns, impute_zero_tenure_values
from exploratory_analysis import plot_churn_counts

file_id = "1763OlxZ9Fun9-x3GYi6BUu_7ot9AfEkJ"   # replace with  file ID
destination = "./data/raw/telco_customer_churn_data.csv"  # local file name

#download_file_from_google_drive(file_id, destination)

# Paths
RAW_DATA_PATH = "./data/raw/telco_customer_churn_data.csv"
PROCESSED_DATA_PATH = "./data/processed/telco_customer_churn_data_cleaned.csv"

raw_df = load_data_csv(RAW_DATA_PATH)

clean_df = clean_data(raw_df, "Churn")
zero_one_bool_df = convert_yes_no_columns(clean_df)
filled_total_charges_df = impute_zero_tenure_values(zero_one_bool_df, "TotalCharges")

#save_data(filled_total_charges_df, PROCESSED_DATA_PATH)

churn_visual_path = './visuals/eda/churn_count_eval.png'
plot_churn_counts(filled_total_charges_df, 'Churn', churn_visual_path)