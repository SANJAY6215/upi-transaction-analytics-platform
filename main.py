from etl.extract.extract import extract_data
from etl.transform.transform import transform_data
from etl.load.load import load_data


def run_pipeline():

    users, merchants, locations, transactions = extract_data()

    users, merchants, locations, transactions = transform_data(
        users, merchants, locations, transactions
    )

    load_data(users, merchants, locations, transactions)


if __name__ == "__main__":
    run_pipeline()