import os
import matplotlib.pyplot as plt
import seaborn as sns

def plot_churn_counts(df, target_col='Churn', save_path='visuals/eda/churn_count_eval.png'):
    """
    Plots the count of churn vs non-churn customers and saves the plot.
    
    Parameters:
    df(pd.DataFrame): DataFrame containing the target column
    target_col(str, default 'Churn'): Column name for churn labels
    save_path(str, default):'visuals/eda': Path to save the plot image
    """
    # --- Plot countplot ---
    plt.figure(figsize=(8,6))

    # Set y-axis ticks from 0 to 5000 at intervals of 500
    plt.yticks(range(0, 5001, 500))

    # Add grid
    plt.grid(axis='y', color='gray', linestyle='--', linewidth=1, alpha=0.7)

    sns.countplot(x=target_col, data=df, palette='Set2')
    plt.title(f"{target_col} vs Non-{target_col} Customers")

    # --- Create folder if it doesn't exist ---
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # --- Save plot ---
    plt.savefig(save_path, dpi=500, bbox_inches='tight')
    
    print(f"{target_col} Plot saved to {save_path}")
