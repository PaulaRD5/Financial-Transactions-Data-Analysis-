# Importación de librerías 
import pandas as pd
import numpy as np
from faker import Faker
import random
import os
from datetime import datetime, timedelta

#Inicialización y Configuración de Semillas (Seeds)
fake = Faker("en_GB")
np.random.seed(42)
random.seed(42)

#Definición de Constantes de Configuración
N_CUSTOMERS = 5000
N_ACCOUNTS = 8000
N_TRANSACTIONS = 120000

#Generacion de custormers 
def generate_customers(n):
    customers = [] 

    for i in range(n):
        customer_id = f"CUST_{i:05d}"
        full_name = fake.name()
        email = fake.email()
        country = fake.country()
        signup_date = fake.date_between(start_date="-5y", end_date="today")
        risk_segment = random.choice (["low", "medium", "high"])

        customers.append([
            customer_id, 
            full_name, 
            email, 
            country, 
            signup_date, 
            risk_segment 
        ])

    df = pd.DataFrame(customers, columns =[
        "customer_id", "full_name", "email", 
        "country", "signup_date", "risk_segment"
    ])

    return df 

#Introduccion de errores
def introduce_customer_errors(df):

    # Emails mal formados
    idx = np.random.choice(df.index, size=100, replace=False)
    df.loc[idx, "email"] = "invalid_email"

    # Fechas en string con formato distinto
    idx = np.random.choice(df.index, size=150, replace=False)
    df.loc[idx, "signup_date"] = df.loc[idx, "signup_date"].astype(str)

    # Riesgo fuera de dominio
    idx = np.random.choice(df.index, size=80, replace=False)
    df.loc[idx, "risk_segment"] = "unknown"

    return df 

# Generacion de accounts
def generate_accounts(n, customers_df):

    customer_ids = customers_df["customer_id"].tolist()

    accounts = []

    for i in range(n): 
        account_id = f"ACC_{i:06d}"
        customer_id = random.choice(customer_ids)
        account_type = random.choice(["savings", "checking"])
        currency = random.choice(["GBP", "EUR", "USD"])
        balance = round(np.random.normal(loc=5000, scale=3000), 2)
        opened_date = fake.date_between(start_date="-5y", end_date="today")
        status = random.choice(["active", "closed", "suspended"])

        accounts.append([
            account_id, 
            customer_id, 
            account_type,
            currency, 
            balance, 
            opened_date, 
            status 
        ])

    df = pd.DataFrame(accounts, columns=[
        "account_id", "customer_id", "account_type", 
        "currency", "balance", "opened_date", "status"
    ])

    return df 

#Introduccion de errores
def introduce_account_errors(df):

    # Balances como string con simbolo
    idx = np.random.choice(df.index, size=300, replace=False)
    df.loc[idx, "balance"] = "$" + df.loc[idx, "balance"].astype(str)

    #Customer_id inexistentes
    idx = np.random.choice(df.index, size=200, replace=False)
    df.loc[idx, "customer_id"] = "CUST_99999"

    #Fechas como string mal formateadas
    idx = np.random.choice(df.index, size=150, replace=False)
    df.loc[idx, "opened_date"] = "31-02-2020"

    #Status fuera de dominio
    idx = np.random.choice(df.index, size=100, replace=False)
    df.loc[idx, "status"] = "unknown"

    #duplicar algunos account_id
    duplicates = df.sample(50)
    df = pd.concat([df, duplicates], ignore_index=True)

    return df 


# Generacion de transactions
def generate_transactions(n, accounts_df):

    account_ids = accounts_df["account_id"].tolist()

    transactions = []

    for i in range(n):
        transaction_id = f"TX_{i:08d}"
        account_id = random.choice(account_ids)
        transaction_date = fake.date_between(start_date="-2y", end_date="today")
        transaction_type = random.choice(["debit", "credit"])
        if transaction_type == "debit":
            amount = -abs(np.random.normal(100,50))
        else:
            amount = abs(np.random.normal(1000, 500))
        merchant_name =  fake.company()
        category = random.choice([
            "groceries", "rent", "salary", 
            "transfer", "utilities"
        ])
        is_fraud_flag = random.choice([0, 0, 0, 0, 1])

        transactions.append([
            transaction_id, 
            account_id,
            transaction_date, 
            round(amount, 2), 
            transaction_type, 
            merchant_name, 
            category, 
            is_fraud_flag
        ])

    df = pd.DataFrame(transactions, columns=[
        "transaction_id", 
        "account_id", 
        "transaction_date", 
        "amount", 
        "transaction_type", 
        "merchant_name", 
        "category", 
        "is_fraud_flag"
    ])

    return df 

#Introduccion de errores financieros
def introduce_transaction_errors(df):

    # transaction_type inconsistente con signo
    idx = np.random.choice(df.index, size=500, replace=False)
    df.loc[idx, "transaction_type"] = "credit"

    # amount como string
    idx = np.random.choice(df.index, size= 400, replace=False)
    df.loc[idx, "amount"] = df.loc[idx, "amount"].astype(str)

    # fechas futuras
    idx = np.random.choice(df.index, size=300, replace=False)
    df.loc[idx, "transaction_date"] = datetime.now() + timedelta(days=365)

    #account_id inexistente
    idx = np.random.choice(df.index, size= 250, replace=False)
    df.loc[idx, "account_id"] = "ACC_99999"

    #outliers extremos
    idx = np.random.choice(df.index, size=150, replace=False)
    df.loc[idx, "amount"] = 1000000

    #duplicar transacciones
    duplicates = df.sample(100)
    df = pd.concat([df, duplicates], ignore_index=True)

    return df

# Previo a la creacion de tablas, creamos una carpeta data y subcarpeta raw
current_dir = os.path.dirname(os.path.abspath(__file__))

root_dir = os.path.dirname(current_dir)

data_raw_path = os.path.join(root_dir, 'data', 'raw')

os.makedirs(data_raw_path, exist_ok=True)



# Actualizacion de los tres bloques y guardado final 
if __name__ == "__main__":

    customers = generate_customers(N_CUSTOMERS)
    customers = introduce_customer_errors(customers)

    accounts = generate_accounts(N_ACCOUNTS, customers)
    accounts = introduce_account_errors(accounts)

    transactions = generate_transactions(N_TRANSACTIONS, accounts)
    transactions = introduce_transaction_errors(transactions)

    cust_file = os.path.join(data_raw_path, "customers.csv")
    acc_file = os.path.join(data_raw_path, "accounts.csv")
    trans_file = os.path.join(data_raw_path, "transactions.csv")
  
    customers.to_csv(cust_file, index=False)
    accounts.to_csv(acc_file, index=False)
    transactions.to_csv(trans_file, index=False)

print(f"✅ ¡Éxito! Archivos guardados en: {data_path}")

