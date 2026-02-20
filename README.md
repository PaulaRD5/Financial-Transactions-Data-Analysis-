# Financial Transactions Data Analysis  
**Data Cleaning, Risk Detection & Business Insights**

---

## Project Overview

This project simulates a real-world financial dataset containing bank customers, accounts and transactions.  

The objective is to build a reproducible data pipeline and extract meaningful business insights from cleaned and validated financial data.

The project focuses on:

- Data quality assessment  
- Data cleaning and transformation  
- Business rule enforcement  
- Risk detection  
- Financial performance analysis  

---

## Objectives

- Identify and correct inconsistencies in transactional data  
- Recalculate and validate account balances  
- Detect high-risk transactions  
- Analyse customer behaviour by segment  
- Produce actionable financial insights  

---

## Project Structure
bank-transactions-data-analysis/
│
├── data/


│ ├── raw/
│ └── processed/
│


├── notebooks/
│ └── 02_financial_analysis.ipynb
│


├── src/
│ ├── cleaning.py
│ ├── business_rules.py
│ ├── validation.py
│ └── pipeline.py
│


├── requirements.txt


└── README.md


---

## Methodology

### Data Generation  
Synthetic financial datasets were generated to simulate a banking environment.

### Data Cleaning  
- Handling missing values  
- Standardising formats  
- Removing inconsistencies  
- Type corrections  

### Business Rules Enforcement  
- Transaction sign validation  
- Balance recalculation  
- High-risk transaction flagging  
- Transaction size classification  

### Data Validation  
- Referential integrity checks  
- Balance consistency checks  
- Data quality reporting  

### Financial Analysis  

The cleaned dataset was analysed to extract KPIs and behavioural insights:

- Transaction volume analysis  
- Risk exposure evaluation  
- Customer segmentation insights  
- Distribution analysis of balances and transaction sizes  

---

## Key Insights

- A small percentage of transactions exceeded predefined high-risk thresholds.  
- Corporate accounts concentrated the largest share of total transaction volume.  
- Initial data quality checks revealed inconsistencies in account balances, which were corrected during cleaning.  
- After validation, referential integrity reached near-complete consistency.  

---

## How to Run the Project

From the root directory:

```bash
python -m src.pipeline

Then open:
notebooks/02_financial_analysis.ipynb

## Technologies Used

- Python

- Pandas

- NumPy

- Matplotlib

- Seaborn

## Business Impact

- This project demonstrates the ability to:

- Build structured and reproducible data pipelines

- Apply financial logic to transactional datasets

- Detect risk patterns

- Translate raw data into business insights
