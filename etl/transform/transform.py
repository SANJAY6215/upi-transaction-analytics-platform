import pandas as pd

def transform_data(users, merchants, locations, transactions):

    # remove duplicates
    users = users.drop_duplicates()
    merchants = merchants.drop_duplicates()
    locations = locations.drop_duplicates()
    transactions = transactions.drop_duplicates()

    # convert timestamp
    transactions["transaction_time"] = pd.to_datetime(
        transactions["transaction_time"]
    )

    # remove invalid transactions
    transactions = transactions[transactions["amount"] > 0]

    print("Data transformed successfully")

    return users, merchants, locations, transactions