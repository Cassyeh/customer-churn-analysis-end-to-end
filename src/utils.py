#Helper Functions
import requests
import os
import pandas as pd

def download_file_from_google_drive(file_id, destination):
    """
    Download a file from Google Drive.
    
    :param file_id: The file ID from Google Drive share link
    :param destination: Local path to save the CSV
    """
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)

    # Check for large files requiring confirmation
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            params = {'id': file_id, 'confirm': value}
            response = session.get(URL, params=params, stream=True)
            break
    
    # Simple validation: check if response is HTML (likely an error page)
    content_type = response.headers.get('Content-Type', '')
    if 'text/html' in content_type.lower():
        raise ValueError(f"Failed to download file. File ID may not exist or is not accessible: {file_id}")
    
    os.makedirs(os.path.dirname(destination), exist_ok=True)

    # Save the file locally
    with open(destination, "wb") as f: #wb for binary mode, some xls files
        for chunk in response.iter_content(chunk_size=32768): #write in chunk to help RAM
            if chunk:
                f.write(chunk)

    print(f"File downloaded successfully and saved to {destination}")


# -------------------------
# Example usage
# -------------------------
"""
# Your Google Drive share link: https://drive.google.com/file/d/FILE_ID/view?usp=sharing
file_id = "1763OlxZ9Fun9-x3GYi6BUu_7ot9AfEkJ"   # replace with  file ID
destination = "./data/raw/telco_customer_churn_data.csv"  # local file name

download_file_from_google_drive(file_id, destination)
"""

def load_data_csv(path):
    """
    Load a CSV file into a pandas DataFrame.
    Parameters:
    path(str): Path to the CSV file to be loaded. Must have a '.csv' extension.
    
    Returns:
    pd.DataFrame: A pandas DataFrame containing the data from the CSV file.
    
    Raises
    FileNotFoundError: If the specified file does not exist.
    ValueError: If the specified file does not have a '.csv' extension.
    """
    # Check if file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV data file not found at: {path}")
    
    # Check file extension
    if not path.lower().endswith(".csv"):
        raise ValueError(f"File must be a CSV file. Provided file: {path}")
    
    # Load the CSV into a DataFrame
    df = pd.read_csv(path)
    print(f"Data loaded successfully. Shape: {df.shape}")
    return df

# Example usage
# -------------------------
"""
# Paths
RAW_DATA_PATH = "./data/raw/telco_customer_churn_data.csv"
df = load_data(RAW_DATA_PATH)
"""

def save_data(df, path):
    """Save cleaned DataFrame to CSV"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Cleaned data saved to: {path}")

# Example usage
# -------------------------
"""
# Paths
PROCESSED_DATA_PATH = "./data/processed/telco_customer_churn_data_cleaned.csv"
save_data(clean_df, PROCESSED_DATA_PATH)
"""