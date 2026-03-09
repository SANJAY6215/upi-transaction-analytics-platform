import pandas as pd
import random
import time
from faker import Faker
from datetime import datetime
import numpy as np
from sqlalchemy import create_engine

fake = Faker("en_IN")

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

engine = create_engine(
"postgresql://upi_user:upi_password@localhost:5432/upi_analytics"
)

# -----------------------------------
# CONFIG
# -----------------------------------

NUM_USERS = 500
NUM_MERCHANTS = 100
NUM_LOCATIONS = 50

# -----------------------------------
# USERS
# -----------------------------------

users = []

for i in range(1, NUM_USERS + 1):

    users.append({
        "user_id": i,
        "name": fake.name(),
        "city": fake.city(),
        "state": fake.state(),
        "risk_score": round(random.uniform(0,1),2)
    })

df_users = pd.DataFrame(users)

# -----------------------------------
# MERCHANTS
# -----------------------------------

categories = [
"Groceries","Food","Electronics","Clothing",
"Fuel","Travel","Pharmacy","Entertainment"
]

merchants = []

for i in range(1, NUM_MERCHANTS + 1):

    merchants.append({
        "merchant_id": i,
        "merchant_name": fake.company(),
        "category": random.choice(categories),
        "city": fake.city(),
        "risk_level": random.choice(["LOW","MEDIUM","HIGH"])
    })

df_merchants = pd.DataFrame(merchants)

# -----------------------------------
# LOCATIONS
# -----------------------------------

locations = []

for i in range(1, NUM_LOCATIONS + 1):

    locations.append({
        "location_id": i,
        "city": fake.city(),
        "state": fake.state(),
        "pincode": fake.postcode()
    })

df_locations = pd.DataFrame(locations)

# -----------------------------------
# INSERT DIMENSION TABLES
# -----------------------------------

df_users.to_sql("dim_users", engine, if_exists="replace", index=False)
df_merchants.to_sql("dim_merchants", engine, if_exists="replace", index=False)
df_locations.to_sql("dim_locations", engine, if_exists="replace", index=False)

print("Dimension tables inserted successfully")

# -----------------------------------
# LIVE TRANSACTION GENERATOR
# -----------------------------------

payment_methods = ["UPI","Wallet","Card"]
statuses = ["SUCCESS","FAILED","PENDING"]

transaction_id = 1

while True:

    batch_size = random.randint(100,200)

    transactions = []

    for _ in range(batch_size):

        amount = round(np.random.exponential(scale=500),2)

        fraud = False

        if amount > 5000:
            fraud = True

        merchant_id = random.randint(1,NUM_MERCHANTS)

        if merchant_id < 5 and random.random() < 0.3:
            fraud = True

        transactions.append({

            "transaction_id": transaction_id,
            "user_id": random.randint(1,NUM_USERS),
            "merchant_id": merchant_id,
            "location_id": random.randint(1,NUM_LOCATIONS),
            "amount": amount,
            "transaction_time": datetime.now(),
            "status": random.choice(statuses),
            "payment_method": random.choice(payment_methods),
            "device_id": fake.uuid4(),
            "fraud_flag": fraud

        })

        transaction_id += 1

    df_transactions = pd.DataFrame(transactions)

    df_transactions.to_sql(
        "fact_transactions",
        engine,
        if_exists="append",
        index=False
    )

    print(f"{batch_size} transactions inserted at {datetime.now()}")

    # wait 10 minutes
    time.sleep(600)