# Copyright 2023 Shawn Oster, Inc. or its affiliates. All Rights Reserved.

import logging
import os
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
CLIENT_ID = os.environ.get("client_id")
CLIENT_SECRET = os.environ.get("client_secret")

splitwise = SplitwiseAPI(CLIENT_ID, CLIENT_SECRET)


def split_expense(date, description, amount):
    owed_to_me = amount / 2

    date_obj = datetime.strptime(date, "%m/%d/%Y")
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


split_expense("3/11/2023", "McDonald's", 17.58)
