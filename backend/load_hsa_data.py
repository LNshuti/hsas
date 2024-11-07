# Step-by-Step Plan:
# 1. Import necessary libraries.
# 2. Connect to the SQLite database and load the 'hsa_data' table into a pandas DataFrame.
# 3. Define and perform hypothesis tests:
#    a. Correlation between total_days_of_care and total_charges.
#    b. Difference in total_charges between different zip codes of residence.
#    c. Association between number of total_cases and total_days_of_care.

# Step 1: Import Libraries
import pandas as pd
import sqlite3
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

# Step 2: Load Data from SQLite
conn = sqlite3.connect('databases/hsas.db')
df = pd.read_sql_query("SELECT * FROM hsa_data", conn)
conn.close()

# Display first few rows
print(df.head())

# Step 3a: Correlation between total_days_of_care and total_charges
# Hypothesis:
# H0: There is no correlation between total_days_of_care and total_charges.
# H1: There is a significant correlation between total_days_of_care and total_charges.

corr, p_value = stats.pearsonr(df['total_days_of_care'], df['total_charges'])
print(f"Pearson Correlation: {corr}, P-value: {p_value}")

if p_value < 0.05:
    print("Reject the null hypothesis. There is a significant correlation.")
else:
    print("Fail to reject the null hypothesis. No significant correlation found.")

# Step 3b: Difference in total_charges between different zip codes of residence
# Hypothesis:
# H0: There is no difference in total_charges across different zip codes.
# H1: There is a significant difference in total_charges across different zip codes.

# Select top 2 most frequent zip codes for comparison
top_zip_codes = df['zip_cd_of_residence'].value_counts().nlargest(2).index.tolist()
df_top = df[df['zip_cd_of_residence'].isin(top_zip_codes)]

charges_zip1 = df_top[df_top['zip_cd_of_residence'] == top_zip_codes[0]]['total_charges']
charges_zip2 = df_top[df_top['zip_cd_of_residence'] == top_zip_codes[1]]['total_charges']

t_stat, p_val = stats.ttest_ind(charges_zip1, charges_zip2, equal_var=False)
print(f"T-test Statistic: {t_stat}, P-value: {p_val}")

if p_val < 0.05:
    print("Reject the null hypothesis. Significant difference found.")
else:
    print("Fail to reject the null hypothesis. No significant difference found.")

# Step 3c: Association between number of total_cases and total_days_of_care
# Hypothesis:
# H0: There is no association between total_cases and total_days_of_care.
# H1: There is an association between total_cases and total_days_of_care.

contingency_table = pd.crosstab(df['total_cases'], df['total_days_of_care'])
chi2, p, dof, ex = stats.chi2_contingency(contingency_table)
print(f"Chi-squared Statistic: {chi2}, P-value: {p}")

if p < 0.05:
    print("Reject the null hypothesis. There is an association.")
else:
    print("Fail to reject the null hypothesis. No association found.")

# Optional: Visualizations
# Scatter plot for correlation
sns.scatterplot(x='total_days_of_care', y='total_charges', data=df)
plt.title('Total Days of Care vs Total Charges')
plt.show()

# Box plot for difference in charges between zip codes
sns.boxplot(x='zip_cd_of_residence', y='total_charges', data=df_top)
plt.title('Total Charges by Zip Code')
plt.show()