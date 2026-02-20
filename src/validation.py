# Imports
import pandas as pd

# Validaciones relacionales
# Accounts con customer inexistente
def validate_account_customer_relationship(accounts_df, customers_df):

    invalid_accounts = accounts_df[
        ~accounts_df["customer_id"].isin(customers_df["customer_id"])
    ]

    return invalid_accounts

# Transactions con account inexistente
def validate_transaction_account_relationship(transactions_df, accounts_df):

    invalid_transactions = transactions_df[
        ~transactions_df["account_id"].isin(accounts_df["account_id"])
    ]

    return invalid_transactions

# Reglas financieras
# Inconsistencia signo vs tipo
def validate_transaction_sign(transactions_df):

    mask = (
        ((transactions_df["transaction_type"] == "debit") &
         (transactions_df["amount"] > 0)) |
        ((transactions_df["transaction_type"] == "credit") &
         (transactions_df["amount"] < 0))
    )

    return transactions_df[mask]

# Outliers extremos
def detect_extreme_outliers(transactions_df, threshold=100000):

    return transactions_df[
        transactions_df["amount"].abs() > threshold
    ]

# Validaciones temporales
# Transacciones futuras
def validate_future_transactions(transactions_df):

    return transactions_df[
        transactions_df["transaction_date"] > pd.Timestamp.today()
    ]

#Fechas inválidas (NaT)
def validate_invalid_dates(df, column_name):

    return df[df[column_name].isna()]

# Validacion de dominio 
# Validar status accounts
def validate_account_status(accounts_df):

    valid_status = ["active", "closed", "suspended"]

    return accounts_df[
        ~accounts_df["status"].isin(valid_status)
    ]

# Validar risk_segment
def validate_risk_segment(customers_df):

    valid_segments = ["low", "medium", "high"]

    return customers_df[
        ~customers_df["risk_segment"].isin(valid_segments)
    ]

# Resumen de calidad global
def build_quality_report(customers_df, accounts_df, transactions_df):

    report = {
        "duplicate_customers": customers_df["customer_id"].duplicated().sum(),
        "duplicate_accounts": accounts_df["account_id"].duplicated().sum(),
        "duplicate_transactions": transactions_df["transaction_id"].duplicated().sum(),
        "invalid_account_links": len(
            validate_account_customer_relationship(accounts_df, customers_df)
        ),
        "invalid_transaction_links": len(
            validate_transaction_account_relationship(transactions_df, accounts_df)
        ),
        "future_transactions": len(
            validate_future_transactions(transactions_df)
        ),
        "sign_inconsistencies": len(
            validate_transaction_sign(transactions_df)
        )
    }

    return pd.Series(report)







