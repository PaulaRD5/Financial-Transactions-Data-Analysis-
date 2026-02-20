# Imports
import pandas as pd
import numpy as np

# Forzar coherencia signo vs tipo
def enforce_transaction_sign(transactions_df):

    df = transactions_df.copy()

    df.loc[df["transaction_type"] == "debit", "amount"] = -df.loc[
        df["transaction_type"] == "debit", "amount"
    ].abs()

    df.loc[df["transaction_type"] == "credit", "amount"] = df.loc[
        df["transaction_type"] == "credit", "amount"
    ].abs()

    return df

# Recalcular balance desde transacciones
def recalculate_account_balance(accounts_df, transactions_df):

    df_accounts = accounts_df.copy()
    df_transactions = transactions_df.copy()

    recalculated = (
        df_transactions
        .groupby("account_id")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "recalculated_balance"})
    )

    df_accounts = df_accounts.merge(
        recalculated,
        on="account_id",
        how="left"
    )

    df_accounts["recalculated_balance"] = df_accounts[
        "recalculated_balance"
    ].fillna(0)

    return df_accounts

# Flag de alto riesgo
def flag_high_risk_large_transactions(
    transactions_df,
    accounts_df,
    customers_df,
    threshold=50000
):

    df = transactions_df.copy()

    df = df.merge(
        accounts_df[["account_id", "customer_id"]],
        on="account_id",
        how="left"
    )

    df = df.merge(
        customers_df[["customer_id", "risk_segment"]],
        on="customer_id",
        how="left"
    )

    df["high_risk_alert"] = (
        (df["risk_segment"] == "high") &
        (df["amount"].abs() > threshold) &
        (df["is_fraud_flag"] == 0)
    )

    return df

# Eliminar transacciones posteriores a cierre de cuenta
def remove_transactions_after_account_closure(
    transactions_df,
    accounts_df
):

    df = transactions_df.copy()

    closed_accounts = accounts_df[
        accounts_df["status"] == "closed"
    ][["account_id", "opened_date"]]

    df = df.merge(
        closed_accounts,
        on="account_id",
        how="left"
    )

    mask_invalid = (
        (df["status"] == "closed") &
        (df["transaction_date"] > df["opened_date"])
    )

    df = df[~mask_invalid]

    return df.drop(columns=["opened_date"], errors="ignore")

# Clasificación de tamaño de transacción
def classify_transaction_size(transactions_df):

    df = transactions_df.copy()

    conditions = [
        df["amount"].abs() < 100,
        df["amount"].abs().between(100, 1000),
        df["amount"].abs() > 1000
    ]

    categories = ["small", "medium", "large"]

    df["transaction_size"] = np.select(
        conditions,
        categories,
        default="unknown"
    )

    return df

