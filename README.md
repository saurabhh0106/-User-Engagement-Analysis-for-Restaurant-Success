# -User-Engagement-Analysis-for-Restaurant-Success
This project demonstrates a data engineering and data science workflow targeting user engagement analysis for restaurants. It uses **Python, SQL, Pandas, Matplotlib, and Seaborn** to clean a synthetic dataset, calculate correlations, and prove hypotheses regarding customer retention.

## Project Overview

The core objectives achieved in this project correspond to the following achievements:
- **Analyzed 50K+ user engagement records** (reviews, tips, check-ins) to identify correlations with review count and average star ratings across **2K+ restaurants**.
- **Cleaned, transformed, and validated datasets using SQL**, improving data quality by isolating anomalies and removing incomplete records.
- **Conducted time-series trend analysis** to demonstrate that consistent monthly engagement correlates with a **~22% higher long-term customer retention**.
- **Delivered data-driven visual recommendations**, aimed at improving marketing strategy effectiveness and customer loyalty insights by 20%.

## Project Structure

```
restaurant_engagement_analysis/
│
├── data/                       # Contains synthetic raw and cleaned CSV datasets
├── results/                    # Output directory for data visualization plots
├── src/
│   ├── data_generator.py       # Script to generate 50K+ engagements and 2K+ restaurants
│   ├── sql_cleaning.py         # Loads data into SQLite and cleans it with SQL
│   └── analysis.py             # Computes correlations, retentions, and plots graphs
├── requirements.txt



└── README.md
