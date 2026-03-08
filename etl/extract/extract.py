import pandas as pd

def extract_data():

    users = pd.read_csv("data/synthetic/users.csv")
    merchants = pd.read_csv("data/synthetic/merchants.csv")
    locations = pd.read_csv("data/synthetic/locations.csv")
    transactions = pd.read_csv("data/synthetic/transactions.csv")

    print("Data extracted successfully")

    return users, merchants, locations, transactions