import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import numpy as np

fake = Faker("en_IN")

NUM_USERS = 500
NUM_MERCHANTS = 100
NUM_LOCATIONS = 50
NUM_TRANSACTIONS = 5000

START_DATE = datetime(2026, 2, 1)
END_DATE = datetime(2026, 3, 31)

# USERS
users = []
for i in range(1, NUM_USERS + 1):
    users.append({
        "user_id": i,
        "name": fake.name(),
        "city": fake.city(),
        "state": fake.state(),
        "risk_score": round(random.uniform(0, 1), 2)
    })
df_users = pd.DataFrame(users)

# MERCHANTS
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

# LOCATIONS
locations = []
for i in range(1, NUM_LOCATIONS + 1):
    locations.append({
        "location_id": i,
        "city": fake.city(),
        "state": fake.state(),
        "pincode": fake.postcode()
    })
df_locations = pd.DataFrame(locations)

# TRANSACTIONS
transactions = []
payment_methods = ["UPI","Wallet","Card"]
statuses = ["SUCCESS","FAILED","PENDING"]

for i in range(1, NUM_TRANSACTIONS + 1):

    transaction_time = START_DATE + timedelta(
        seconds=random.randint(0,int((END_DATE - START_DATE).total_seconds()))
    )

    amount = round(np.random.exponential(scale=500),2)

    fraud = False

    if amount > 5000:
        fraud = True

    merchant_id = random.randint(1,NUM_MERCHANTS)

    if merchant_id < 5 and random.random() < 0.3:
        fraud = True

    transactions.append({
        "transaction_id": i,
        "user_id": random.randint(1,NUM_USERS),
        "merchant_id": merchant_id,
        "location_id": random.randint(1,NUM_LOCATIONS),
        "amount": amount,
        "transaction_time": transaction_time,
        "status": random.choice(statuses),
        "payment_method": random.choice(payment_methods),
        "device_id": fake.uuid4(),
        "fraud_flag": fraud
    })

df_transactions = pd.DataFrame(transactions)

# SAVE FILES
df_users.to_csv("data/synthetic/users.csv", index=False)
df_merchants.to_csv("data/synthetic/merchants.csv", index=False)
df_locations.to_csv("data/synthetic/locations.csv", index=False)
df_transactions.to_csv("data/synthetic/transactions.csv", index=False)

print("Synthetic data generated successfully")