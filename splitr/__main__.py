# Copyright 2023 Shawn Oster, Inc. or its affiliates. All Rights Reserved.

import logging
import os
import argparse
import csv
from datetime import datetime

from dotenv import load_dotenv

from splitr.splitwise import SplitwiseAPI

USER_ID_SHAWN = 13065056
USER_ID_SHANNON = 13065035

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

load_dotenv()
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

splitwise = SplitwiseAPI(CLIENT_ID, CLIENT_SECRET)


def split_expense(date: str, description: str, amount: float):
    owed_to_me = amount / 2

    date_obj = datetime.strptime(date, "%Y-%m-%d")
    iso_date = date_obj.isoformat()

    expense = splitwise.create_expense(
        group_id=0,
        description=description,
        cost=amount,
        date=iso_date,
        users=[
            {"user_id": USER_ID_SHAWN, "owed_share": f"{amount - owed_to_me}", "paid_share": f"{amount}"},
            {"user_id": USER_ID_SHANNON, "owed_share": f"{owed_to_me}", "paid_share": "0"},
        ],
    )


def main():
    parser = argparse.ArgumentParser(description="Read a CSV file")
    parser.add_argument("filename", type=str, help="Path to the CSV file")
    args = parser.parse_args()

    with open(args.filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["Custom Name"] or row["Name"]
            split_expense(row["Date"], name, float(row["Amount"]))


if __name__ == "__main__":
    main()
