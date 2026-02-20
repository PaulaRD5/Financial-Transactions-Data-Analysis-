# Imports y configuración
import pandas as pd
import numpy as np
import re

# FUNCIONES AUXILIARES INTERNAS 
# Conversión robusta a datetime
def _parse_dates(series):
   return pd.to_datetime(series, errors="coerce")

# Limpieza de columnas monetarias
def _clean_currency_column(series):

    cleaned = (
        series.astype(str)
        .str.replace("£", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    return pd.to_numeric(cleaned, errors="coerce")

# Normalización de strings
def _standardise_string(series):
    return (
        series.astype(str)
        .str.strip()
        .str.lower()
    )

# LIMPIEZA DE CUSTOMERS 
def clean_customers(df):

    df = df.copy()

    # Eliminar duplicados por ID
    df = df.drop_duplicates(subset="customer_id")

    # Normalizar email
    df["email"] = _standardise_string(df["email"])

    # Validar email básico
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    invalid_mask = ~df["email"].str.match(email_pattern, na=False)
    df.loc[invalid_mask, "email"] = np.nan

    # Parsear fechas
    df["signup_date"] = _parse_dates(df["signup_date"])

    # Normalizar risk_segment
    df["risk_segment"] = _standardise_string(df["risk_segment"])

    valid_segments = ["low", "medium", "high"]
    df.loc[~df["risk_segment"].isin(valid_segments), "risk_segment"] = np.nan

    return df

# LIMPIZA DE ACCOUNTS 
def clean_accounts(df):

    df = df.copy()

    df = df.drop_duplicates(subset="account_id")

    # Balance
    df["balance"] = _clean_currency_column(df["balance"])

    # Parsear fechas
    df["opened_date"] = _parse_dates(df["opened_date"])

    # Normalizar status
    df["status"] = _standardise_string(df["status"])

    valid_status = ["active", "closed", "suspended"]
    df.loc[~df["status"].isin(valid_status), "status"] = np.nan

    # Normalizar account_type
    df["account_type"] = _standardise_string(df["account_type"])

    valid_types = ["savings", "checking"]
    df.loc[~df["account_type"].isin(valid_types), "account_type"] = np.nan

    return df
# LIMPIEZA DE TRANSACTIONS
def clean_transactions(df):

    df = df.copy()

    df = df.drop_duplicates(subset="transaction_id")

    # Amount
    df["amount"] = _clean_currency_column(df["amount"])

    # Fechas
    df["transaction_date"] = _parse_dates(df["transaction_date"])

    # Normalizar transaction_type
    df["transaction_type"] = _standardise_string(df["transaction_type"])

    valid_types = ["debit", "credit"]
    df.loc[~df["transaction_type"].isin(valid_types), "transaction_type"] = np.nan

    # is_fraud_flag a entero
    df["is_fraud_flag"] = pd.to_numeric(df["is_fraud_flag"], errors="coerce")

    return df



