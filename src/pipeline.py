# Diseño
import pandas as pd
from pathlib import Path

# Importar nuestros módulos
from cleaning import clean_customers, clean_accounts, clean_transactions
from business_rules import (
    enforce_transaction_sign,
    recalculate_account_balance,
    flag_high_risk_large_transactions,
    classify_transaction_size
)
from validation import (
    build_quality_report,
    validate_account_customer_relationship,
    validate_transaction_account_relationship
)

# Definir rutas
DATA_RAW = Path("../data/raw")
DATA_PROCESSED = Path("../data/processed")
DATA_PROCESSED.mkdir(exist_ok=True)

# Función central
def run_pipeline():

    # 1️⃣ Cargar datos crudos
    customers = pd.read_csv(DATA_RAW / "customers.csv")
    accounts = pd.read_csv(DATA_RAW / "accounts.csv")
    transactions = pd.read_csv(DATA_RAW / "transactions.csv")

    print("Datos cargados correctamente.")

    # 2️⃣ Limpieza
    customers_clean = clean_customers(customers)
    accounts_clean = clean_accounts(accounts)
    transactions_clean = clean_transactions(transactions)

    print("Datos limpiados correctamente.")

    # 3️⃣ Aplicar reglas de negocio
    transactions_clean = enforce_transaction_sign(transactions_clean)
    accounts_clean = recalculate_account_balance(accounts_clean, transactions_clean)
    transactions_clean = flag_high_risk_large_transactions(
        transactions_clean, accounts_clean, customers_clean
    )
    transactions_clean = classify_transaction_size(transactions_clean)

    print("Reglas de negocio aplicadas.")

    # 4️⃣ Validación de integridad
    invalid_accounts = validate_account_customer_relationship(accounts_clean, customers_clean)
    invalid_transactions = validate_transaction_account_relationship(transactions_clean, accounts_clean)

    quality_report = build_quality_report(customers_clean, accounts_clean, transactions_clean)

    print("Validación completada.")
    print("Reporte de calidad:\n", quality_report)

    # 5️⃣ Guardado de resultados
    customers_clean.to_csv(DATA_PROCESSED / "customers_clean.csv", index=False)
    accounts_clean.to_csv(DATA_PROCESSED / "accounts_clean.csv", index=False)
    transactions_clean.to_csv(DATA_PROCESSED / "transactions_clean.csv", index=False)

    print("Archivos procesados guardados en:", DATA_PROCESSED)

# Ejecutar el pipeline
if __name__ == "__main__":
    run_pipeline()


