# Customer Churn Analysis – End-to-End Case Study

## Project Overview

Customer churn is one of the most critical business problems in subscription-based and usage-driven companies. This project presents a **complete, end-to-end churn analysis case study**, covering everything from problem framing and data preparation to modeling, evaluation, and business recommendations.
This project also assesses the reliability of churn predictions to ensure the trained model can support real-world retention decisions.

---

## Problem Statement

What is Churn in This Business Context?
In this business context, customer churn refers to customers who discontinue their subscription or stop using the company’s services.
A customer is considered *churned* if they have formally ended their relationship with the company during the observed period.

The ```Churn``` variable in the dataset captures this outcome:
 - Yes → Customer has churned.
 - No → Customer remains an active customer.

Why is churn important to measure and reduce?
Churn represents a loss of customers, usage, and recurring revenue.

In the marketing environment, churn is important because:
- Acquiring new customers is significantly more expensive than retaining existing ones.
- High churn directly impacts revenue, growth, and long-term sustainability.
- Understanding churn drivers enables targeted retention strategies.
- Early Warning Signal: Measuring churn helps identify early behavioral and engagement signals that indicate dissatisfaction, allowing proactive intervention.

## Business Objectives

### 1. Transform Raw Customer Data into Churn-Explaining Features *(Primary Focus)*
Convert raw demographic, usage, and billing data into meaningful features that reflect real customer behavior and engagement.  
This includes engineering features related to customer tenure, service adoption, activity levels, and pricing exposure to better explain *why* customers churn.
**Key Question:** Which customer behaviors and characteristics are most strongly associated with churn?

### 2. Identify High-Risk Customers and Churn Patterns
Leverage engineered features and exploratory analysis to compare churned vs non-churned customers, uncovering patterns related to tenure, usage intensity, and engagement levels.
**Key Question:** Which customer segments are at the highest risk of churning, and what patterns distinguish them?

### 3. Build an Interpretable Churn Prediction Model
Train classification model (Logistic Regression) to predict churn while maintaining interpretability, enabling stakeholders to understand the drivers behind model predictions.
**Key Question:** Can we reliably predict churn using behavior-driven features rather than raw data alone?

### 4. Translate Insights into Actionable Retention Strategies
Use model outputs and postdictive analysis to recommend targeted business actions, prioritizing customers most at risk and identifying practical interventions to reduce churn.
**Key Question:** How can the business proactively reduce churn using data-driven insights?

---

## Dataset

- **Source:** Provided dataset shared for this project  
- **Link:** https://drive.google.com/file/d/1763OlxZ9Fun9-x3GYi6BUu_7ot9AfEkJ/view

The dataset used in this project contains 7,044 customer records with 21 features, capturing customer demographics, subscription details, service usage, billing information, and churn status.

**Dataset Shape**
Rows: 7,044 (customers)
Columns: 21 (features + target)

The dataset includes:
**Columns Overview**

| Category | Features |
|--------|---------|
| **Customer Information** | `customerID`, `gender`, `SeniorCitizen`, `Partner`, `Dependents` |
| **Tenure & Subscription** | `tenure`, `Contract` |
| **Services** | `PhoneService`, `MultipleLines`, `InternetService` |
| **Add-on Services** | `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport` |
| **Entertainment** | `StreamingTV`, `StreamingMovies` |
| **Billing & Payment** | `PaperlessBilling`, `PaymentMethod`, `MonthlyCharges`, `TotalCharges` |
| **Target Variable** | `Churn` |

---
## Target Variable
**Churn**
- **Yes** → Customer has churned  
- **No** → Customer is retained

The dataset provided closely resembles real-world telecom and subscription-based business data, making it ideal for demonstrating practical churn analytics skills.

---

## Project Structure

```
customer-churn-analysis-end-to-end/
│
├── data/
│   ├── raw/                       # Original dataset
│   └── processed/                 # Cleaned and feature-engineered data
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_churn_modeling.ipynb
│
├── scripts/
│   ├── data_cleaning.py           # Python version of data cleaning notebook
│   ├── 02_exploratory_analysis.py # Python version of EDA notebook
│   ├── 03_feature_engineering.py  # Python version of feature engineering notebook
│   └── 04_churn_modeling.py       # Python version of modeling notebook
│   └── churn_main.py              # Entry point of code
│
├── src/
│   ├── data_preprocessing.py      # Reusable data preparation functions
│   ├── feature_engineering.py     # Feature creation logic
│   ├── modeling.py                # Model training and evaluation
│   └── utils.py                   # Helper functions
│
├── visuals/
│   ├── eda/                       # EDA plots and charts
│   └── model/                     # Model evaluation visuals
│
├── images/                        # Images used in README or documentation
│
├── dashboard/                     # Power BI / Tableau dashboard files
│
├── reports/
│   ├── churn_analysis_report.pdf  # Final analytical report
│   └── churn_analysis_slides.pptx # Executive presentation
│
├── requirements.txt
└── README.md
```

## 👤 Author

**Ebubechukwu Chigozie Ijezie**
- GitHub: [@Cassyeh](https://github.com/Cassyeh)
- LinkedIn: [Ebube Ijezie](https://www.linkedin.com/in/ebube-ijezie-68a9a4173/)
- Email: cassandraijezie@gmail.com

##  Acknowledgments

- Dr. Okunola Orogon, PhD for providing the dataset

---

⭐ If you found this project helpful, please consider giving it a star!
