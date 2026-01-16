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
                    ha='center', va='bottom', fontsize=12, color='green')

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
    service_col(str/list): Column name for the service column
    churn_col(str, default 'Churn'): Column name for churn labels
    eligible_condition(str): The condition that the service meets
    title(str): Title of the visual
    save_path(str, default):'visuals/eda': Path to save the plot image
    """

    data = df.copy()

    if type(service_col) == list:
        service_col_str = ", ".join(service_col)
        if eligible_condition is not None:
            data = data.query(eligible_condition)

        service_list = []

        for col in service_col:
            total_service_counts = data.groupby(col).size()
            service_churn_total = (
                data.groupby(col)[churn_col].apply(lambda x: (x == 1).sum())
            ) # x == 1, represents 'Churn' == 'Yes'
            # Compute churn rate, mean applies avg
            churn_rate = service_churn_total / total_service_counts
            churn_service_summary = pd.DataFrame({
                "TotalCustomers": total_service_counts,
                "ChurnedCustomers": service_churn_total,
                "ChurnRate": churn_rate
            })
            # Get unique non-null values
            unique_vals = set(data[col].dropna().unique())
            for val in unique_vals:
                service_list.append({
                    "Service": col,
                    "Status": val,
                    "ChurnedCustomers": service_churn_total[val],
                    "ChurnRate": churn_rate[val]
                })

    service_df = pd.DataFrame(service_list)
    service_df["ChurnRatePct"] = service_df["ChurnRate"] * 100
    #pd.DataFrame(service_list).to_csv("output.csv", index=False, encoding='utf-8')
    #--- Plot ---
    fig, ax1 = plt.subplots(figsize=(12,8))

    # Primary axis: churn rate
    unique_vals = set(service_df["Service"].dropna().unique())
    if (len(unique_vals) > 1):
        sns.barplot(data=service_df, x="Service", hue="Status", y="ChurnRatePct",palette="Set2")
    else:
        sns.barplot(data=service_df, x="Status", y="ChurnRatePct",palette="Set2")
    plt.ylim(0, 100)
    # Set y-axis ticks from 0 to 100 at intervals of 10
    plt.yticks(range(0, 101, 10))
    plt.ylabel("Churn Rate", color="green", fontsize=14)
    plt.title(title, fontsize=14)
    plt.tight_layout()

    for container in ax1.containers:
        ax1.bar_label(container, fmt="%.2f%%", padding=3, color="green", fontsize=12)
    
    labels = [tick.get_text() for tick in ax1.get_xticklabels()]

    if '0' in labels and '1' in labels:
        ax1.set_xlabel(f"{service_col_str} (0 = No, 1 = Yes)", fontsize=16)

    # --- Create folder if it doesn't exist ---
    os.makedirs(os.path.dirname(save_path), exist_ok=True) 
    # --- Save plot ---
    plt.savefig(save_path, dpi=500, bbox_inches='tight')
    print(f"{service_col} Plot saved to {save_path}")
    # # Apply eligibility filter if provided
    # if eligible_condition is not None:
    #     data = data.query(eligible_condition)

    # total_service_counts = data.groupby(service_col).size()
    # print(total_service_counts)
    # service_churn_total = (
    #     data.groupby(service_col)[churn_col].apply(lambda x: (x == 1).sum())
    # ) # x == 1, represents 'Churn' == 'Yes'
    # print(service_churn_total)
    # # Compute churn rate, mean applies avg
    # churn_rate = service_churn_total / total_service_counts

    # print(churn_rate)

    # #The proportion of customers who churned (1) in that group Churn == 1/total number of customers in service_col
    # churn_service_summary = pd.DataFrame({
    #     "TotalCustomers": total_service_counts,
    #     "ChurnedCustomers": service_churn_total,
    #     "ChurnRate": churn_rate
    # })

    # print(churn_service_summary)
    # # --- Plot ---
    # fig, ax1 = plt.subplots(figsize=(8,6))

    # # Primary axis: churn rate
    # sns.barplot(x=churn_service_summary.index, y=churn_service_summary["ChurnRate"],palette="Set2",ax=ax1)
    # ax1.set_ylim(0, 1)
    # ax1.set_ylabel("Churn Rate", color="green", fontsize=12)
    # ax1.set_xlabel(f"{service_col} (0 = No, 1 = Yes)")
    # ax1.set_title(title)

    # # Annotate churn rate on bars
    # for i, rate in enumerate(churn_service_summary["ChurnRate"]):
    #     ax1.text(i, rate + 0.01, f"{rate:.2%}", ha="center", fontsize=10, color="green")

    # # Secondary axis: total customers
    # ax2 = ax1.twinx()
    # sns.lineplot(x=churn_service_summary.index,y=churn_service_summary["ChurnedCustomers"],marker="o",color="blue",linewidth=2,ax=ax2)
    # ax2.set_ylabel("Churned Customers", color="blue", fontsize=12)

    # # Annotate total customers
    # for i, count in enumerate(churn_service_summary["ChurnedCustomers"]):
    #     ax2.text(i, count + 10, f"{count}", ha="center", fontsize=10, color="blue")

    # # --- Create folder if it doesn't exist ---
    # os.makedirs(os.path.dirname(save_path), exist_ok=True) 
    # # --- Save plot ---
    # plt.savefig(save_path, dpi=500, bbox_inches='tight')
    # print(f"{service_col} Plot saved to {save_path}")

def plot_tenure_eda(df, tenure_col="tenure", churn_col="Churn", title=None, save_path='visuals/eda/eval.png'):
    """
    Exploratory Data Analysis for tenure.
    Parameters:
    df(pd.DataFrame): DataFrame containing the columns
    tenure_col(str): Column name for the tenure column
    churn_col(str, default 'Churn'): Column name for churn labels
    save_path(str, default):'visuals/eda': Path to save the plot image
    """
    df = df.sort_values(by=tenure_col, ascending=True)
    # ---------------------------
    # Count plot: churn by tenure
    # ---------------------------
    plt.figure(figsize=(24,8))
    sns.countplot(data=df, x=tenure_col, palette="Set2")
    plt.title(title)
    plt.xlabel(f"{tenure_col}(Months)")
    plt.ylabel("Total Number of Customers")
    plt.tight_layout()
    
    # --- Create folder if it doesn't exist ---
    os.makedirs(os.path.dirname(save_path), exist_ok=True) 
    # --- Save plot ---
    plt.savefig(save_path, dpi=500, bbox_inches='tight')
    print(f"{tenure_col} Plot saved to {save_path}")

    # Group tenure by 6-month intervals using integer division
    df['tenure_group'] = (df['tenure'] // 6) * 6
    df['tenure_group'] = df['tenure_group'].astype(str) + "-" + (df['tenure_group'] + 5).astype(str)
    df = df.sort_values(by=tenure_col, ascending=True)
    # --- Order the groups ascending ---
    ordered_groups = sorted(df['tenure_group'].unique(), key=lambda x: int(x.split('-')[0]))
    df['tenure_group'] = pd.Categorical(df['tenure_group'], categories=ordered_groups, ordered=True)

    plt.figure(figsize=(12,8))
    sns.countplot(data=df, x="tenure_group", palette="Set2")
    plt.title(title)
    plt.xlabel(f"{tenure_col}(6 Months Range)")
    plt.ylabel("Total Number of Customers")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # --- Save plot ---
    plt.savefig(os.path.dirname(save_path)+"/tenure_range.png", dpi=500, bbox_inches='tight')
    print(f"{tenure_col} range Plot saved to {save_path}")

    # --- Calculate churn rate per tenure group ---
    churn_rate_by_group = df.groupby('tenure_group')[churn_col].apply(lambda x: (x == 1).mean())
    #df["ChurnRatePct"] = df["ChurnRate"] * 100

    total_tenure_counts = df.groupby("tenure_group").size()
    tenure_churn_total = (df.groupby("tenure_group")[churn_col].apply(lambda x: (x == 1).sum())) # x == 1, represents 'Churn' == 'Yes'
    # Compute churn rate, mean applies avg
    churn_rate = tenure_churn_total / total_tenure_counts
    churn_service_summary = pd.DataFrame({
        "TotalCustomers": total_tenure_counts,
        "ChurnedCustomers": tenure_churn_total,
        "ChurnRate": churn_rate
    })
    #print(churn_service_summary)
    # --- Plot churn rate ---
    plt.figure(figsize=(12,8))
    ax = sns.barplot(x=churn_rate_by_group.index,y=(churn_rate_by_group.values)*100,palette='Set2')
    plt.title("Churn Rate by Tenure 6 months Group")
    plt.xlabel("Tenure Group (6 Months)")
    plt.ylabel("Churn Rate")
    plt.ylim(0,100)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    for i, rate in enumerate(churn_service_summary["ChurnRate"]):
       ax.text(i, (rate + 0.01)*100, f"{rate:.2%}", ha="center", fontsize=12, color="green")

    plt.tight_layout()
    # --- Save plot ---
    plt.savefig(os.path.dirname(save_path)+"/tenure_range_churned_eval.png", dpi=500, bbox_inches='tight')
    print(f"{tenure_col} range Plot saved to {save_path}")



