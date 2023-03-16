# Copyright 2023 Shawn Oster, Inc. or its affiliates. All Rights Reserved.

import logging
import os

from dotenv import load_dotenv

from splitr.splitwise import SplitwiseAPI

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

user = splitwise.get_current_user()
print(user)

expense = splitwise.create_expense(
    group_id=0,
    description="Pizza",
    cost=50.0,
    users=[
        {"user_id": 13065056, "owed_share": "25", "paid_share": "50"},
        {"user_id": 13065035, "owed_share": "25", "paid_share": "0"},
    ],
)

print(expense)
