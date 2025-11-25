# Data Preparation

### This section prepares the Online Retail II dataset to make it reliable and usable for all project analyses (cohorts, RFM, CLV, and Streamlit simulations). Since the raw dataset contains anomalies (missing values, returns, negative prices, duplicates), a full cleaning pipeline was applied.

#### The main steps are:

Harmonization of column names.

Type conversion (dates, numeric formats).

Removal of incomplete records (e.g., missing dates).

Processing of negative quantities and returns.

Calculation of the Amount variable.

Generation of several cleaned datasets:

transactions_including_returns

transactions_excluding_returns

transactions_customers

This cleaning ensures consistency across the following analyses (RFM, retention, CLV) and provides a reliable foundation for the Streamlit application and marketing decisions.


# Data Exploration

### This part of the project consists of analyzing and exploring the Online Retail II dataset to understand its structure, verify data quality, and produce the first useful indicators for the upcoming steps (modeling, segmentation, Streamlit application).

The notebook used is: 02_data_exploration.ipynb.

#### Work content

Loading raw data and integrating Member 2’s cleaning.

Descriptive analysis (dimensions, types, missing values, inconsistencies).

Main visualizations: sales evolution, price/quantity distributions, country-level analysis.


# Cohort analysis

### This step builds acquisition cohorts and measures customer retention over time to understand post-acquisition behavior. The resulting matrices are then used for empirical CLV calculation and the Streamlit application.

#### Work content

Temporal preparation: creation of InvoiceMonth, AcqMonth (acquisition month), and CohortAge (M+0, M+1, ...).

Cohort matrices:

cohort_counts: number of active customers per cohort and cohort age,

cohort_revenue: revenue per cohort and cohort age.

Retention: retention rate calculation = active at M+t / initial cohort size (M+0).

Main visualizations:

retention heatmap,

cohort-age revenue heatmap,

density curve of average revenue by cohort age.

Key insights:

strong retention drop between M+0 and M+1,

stabilization of a loyal core after M+3,

majority of value generated within the first three months,

2009–2010 cohorts are larger and more profitable.

Generated exports:

cohort_counts.csv,

cohort_revenue.csv,

figures for the Streamlit presentation in docs/.


# clv empirical

### This part of the project computes the Customer Lifetime Value (CLV) empirically, both at the individual customer level and at the cohort level. It also produces the visualizations needed to analyze how customer value evolves over time.

#### Work content

Data preparation

Cleaning of transactions

Calculation of line amount: Amount = Quantity × UnitPrice

Customer-level CLV

Aggregation of total spending per customer

Export: clv_customer.csv

Cohort-level CLV

Determination of the acquisition month (AcqMonth)

Calculation of cohort age (CohortAge, in months)

Calculation of average CLV by cohort

Export: clv_cohort.csv

Visualizations

CLV heatmap by cohort (clv_cohort_heatmap.png)

Cumulative revenue by cohort (clv_cumulative_trend.png)

CLV distributions (linear and log scales)

Count of customers with zero CLV

Generated exports (folder output_clv/)

clv_customer.csv — CLV per customer

clv_cohort.csv — CLV per cohort

Visualizations:

clv_cohort_heatmap.png

clv_cumulative_trend.png

clv_customer_distribution_linear.png

clv_customer_distribution_log.png


# rfm clv formulated

### This step builds the complete RFM table, segments customers according to their purchase behavior, and estimates Customer Lifetime Value (CLV) using a closed-form formula. The notebook uses the cleaned data provided by Member 2.

#### Work content

Data preparation: deduplicated transactions, returns excluded, corrected amounts.

RFM calculation:

Recency (days since last purchase),

Frequency (number of distinct invoices),

Monetary (total spending per customer).

RFM scoring: assignment of 1–5 scores (quintiles), then creation of the combined score RFM_Score = R*100 + F*10 + M.

Marketing segmentation: identification of operational segments (Champions, Loyal, At-risk, Promising, Others).

Key metrics:

ARPU (average revenue per active customer),

r (monthly retention rate).

Closed-form CLV formula:
CLV = ARPU × r / (1 + d − r)
with a discount rate d = 1%.
Results produced: overall CLV and CLV by RFM segment.

Final export: file clean_data/customers_rfm.xlsx containing RFM metrics, scores, segments, ARPU, and CLV for use in the Streamlit app.


