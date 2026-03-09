from sqlalchemy import create_engine

DB_USER = "upi_user"
DB_PASS = "upi_password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "upi_analytics"

engine = create_engine(
"postgresql://upi_user:upi_password@host.docker.internal:5432/upi_analytics"
)
def load_data(users, merchants, locations, transactions):

    users.to_sql("dim_user", engine, if_exists="append", index=False)
    merchants.to_sql("dim_merchant", engine, if_exists="append", index=False)
    locations.to_sql("dim_location", engine, if_exists="append", index=False)
    transactions.to_sql("fact_transactions", engine, if_exists="append", index=False)

    print("Data loaded into PostgreSQL successfully")