import os
import pandas as pd
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

    ax = sns.countplot(x=target_col, data=df, palette='Set2')

    # --- Annotate counts on top of bars ---
    for p in ax.patches:
        count = int(p.get_height())
        ax.annotate(f'{count}', 
                    (p.get_x() + p.get_width()/2., count), 
                    ha='center', va='bottom', fontsize=12, color='black')

    sns.countplot(x=target_col, data=df, palette='Set2')
    # --- Add title and explanation ---
    plt.title(f"{target_col} vs Non-{target_col} Customers\n(Yes = 1: Churned, No = 0: Retained)", fontsize=12)

    # --- Create folder if it doesn't exist ---
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # --- Save plot ---
    plt.savefig(save_path, dpi=500, bbox_inches='tight')
    
    print(f"{target_col} Plot saved to {save_path}")


# Hierarchical service dependencies:
def plot_service_vs_churn(df, service_col, churn_col="Churn",eligible_condition=None, title=None, save_path='visuals/eda/eval.png'):
    """
    Plots churn rate for a given service among eligible customers only.
    Parameters:
    df(pd.DataFrame): DataFrame containing the columns
    service_col(str): Column name for the service column
    churn_col(str, default 'Churn'): Column name for churn labels
    eligible_condition(str): The condition that the service meets
    title(str): Title of the visual
    """

    data = df.copy()

    # Apply eligibility filter if provided
    if eligible_condition is not None:
        data = data.query(eligible_condition)

    total_service_counts = data.groupby(service_col).size()
    print(total_service_counts)
    service_churn_total = (
        data.groupby(service_col)[churn_col].apply(lambda x: (x == 1).sum())
    ) # x == 1, represents 'Churn' == 'Yes'
    print(service_churn_total)
    # Compute churn rate, mean applies avg
    churn_rate = service_churn_total / total_service_counts

    print(churn_rate)

    #The proportion of customers who churned (1) in that group Churn == 1/total number of customers in service_col
    churn_service_summary = pd.DataFrame({
        "TotalCustomers": total_service_counts,
        "ChurnedCustomers": service_churn_total,
        "ChurnRate": churn_rate
    })

    print(churn_service_summary)
    # --- Plot ---
    fig, ax1 = plt.subplots(figsize=(8,6))

    # Primary axis: churn rate
    sns.barplot(x=churn_service_summary.index, y=churn_service_summary["ChurnRate"],palette="Set2",ax=ax1)
    ax1.set_ylim(0, 1)
    ax1.set_ylabel("Churn Rate", color="green", fontsize=12)
    ax1.set_xlabel("Phone Service (0 = No, 1 = Yes)")
    ax1.set_title(title)

    # Annotate churn rate on bars
    for i, rate in enumerate(churn_service_summary["ChurnRate"]):
        ax1.text(i, rate + 0.01, f"{rate:.2%}", ha="center", fontsize=10, color="green")

    # Secondary axis: total customers
    ax2 = ax1.twinx()
    sns.lineplot(x=churn_service_summary.index,y=churn_service_summary["ChurnedCustomers"],marker="o",color="blue",linewidth=2,ax=ax2)
    ax2.set_ylabel("Churned Customers", color="blue", fontsize=12)

    # Annotate total customers
    for i, count in enumerate(churn_service_summary["ChurnedCustomers"]):
        ax2.text(i, count + 10, f"{count}", ha="center", fontsize=10, color="blue")

    # --- Create folder if it doesn't exist ---
    os.makedirs(os.path.dirname(save_path), exist_ok=True) 
    # --- Save plot ---
    plt.savefig(save_path, dpi=500, bbox_inches='tight')
    print(f"{service_col} Plot saved to {save_path}")
