"""
This module provides a Python client for the Splitwise API.

The SplitwiseAPI class provides methods for retrieving and creating expenses
for Splitwise groups.
"""

import json
import logging
import os.path

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


class SplitwiseAPI:
    """
    A Python client for the Splitwise API.

    Usage:
    # Replace with your own API key and secret
    client_key = 'YOUR_API_KEY'
    client_secret = 'YOUR_API_SECRET'

    # Create an instance of the SplitwiseAPI client
    splitwise = SplitwiseAPI(client_key, client_secret)

    # Get expenses for a group
    expenses = splitwise.get_expenses(group_id=12345)

    # Create an expense
    expense = splitwise.create_expense(
        group_id=12345,
        description='Dinner at Joe\'s',
        cost=50.0,
        users=[
            {'user_id': 123, 'owed_share': 25.0},
            {'user_id': 456, 'owed_share': 25.0}
        ],
        details={'category': 'Food', 'notes': 'Had a great time!'}
    )
    """

    def __init__(self, client_key, client_secret):
        """
        Initialize the SplitwiseAPI client.

        Args:
        - client_key (str): The API key for your Splitwise account.
        - client_secret (str): The API secret for your Splitwise account.
        """
        self.base_url = "https://secure.splitwise.com/api/v3.0/"
        self.session = OAuth2Session(client_key, token=self._get_access_token(client_key, client_secret))
        self.session.headers = {
            "Content-Type": "application/json",
        }

    def _get_access_token(self, client_key, client_secret):
        """
        Get an access token for the Splitwise API.

        Args:
        - api_key (str): The API key for your Splitwise account.
        - api_secret (str): The API secret for your Splitwise account.

        Returns:
        - access_token (str): The access token for the Splitwise API.
        """
        credentials_path = os.path.expanduser("~/.splitwise-credentials")
        if os.path.exists(credentials_path):
            logging.info("Loading credentials from disk")
            with open(credentials_path, "r", encoding="UTF-8") as stream:
                token = json.load(stream)
        else:
            token = None

        if not token:
            logging.info("Authenticating with Splitwise")

            # Set up OAuth 2.0 client
            client = BackendApplicationClient(client_id=client_key, scope=[""])
            oauth = OAuth2Session(client=client)
            token_url = "https://secure.splitwise.com/oauth/token"

            # Get access token
            try:
                token = oauth.fetch_token(
                    token_url=token_url,
                    client_id=client_key,
                    client_secret=client_secret,
                    include_client_id=True,
                )
            except Exception as exception:
                logging.error("Failed to authenticate: %s", str(exception))
                raise SplitwiseException("Failed to authenticate") from exception

            with open(credentials_path, "w", encoding="UTF-8") as stream:
                json.dump(token, stream)

        return token

    def get_current_user(self):
        """
        Get information about the current user.
        """
        url = self.base_url + "get_current_user"
        response = self.session.get(url)
        return response.json()

    def get_expenses_by_group_id(self, group_id):
        """
        Get expenses for a Splitwise group.

        Args:
        - group_id (int): The ID of the Splitwise group.

        Returns:
        - expenses (dict): The expenses for the Splitwise group.
        """
        url = self.base_url + f"get_expenses?group_id={group_id}"
        response = self.session.get(url)
        return response.json()

    def get_expenses_by_friend_id(self, friend_id):
        """
        Get expenses for a Splitwise friend.

        Args:
        - friend_id (int): The ID of the Splitwise friend.

        Returns:
        - expenses (dict): The expenses for the Splitwise group.
        """
        url = self.base_url + f"get_expenses?friend_id={friend_id}"
        response = self.session.get(url)
        return response.json()

    def create_expense(self, group_id, description, cost, users, details=None, currency_code="USD"):
        """
        Create an expense for a Splitwise group.

        Args:
        - group_id (int): The ID of the Splitwise group.
        - description (str): A description of the expense.
        - cost (float): The total cost of the expense.
        - users (list): A list of dictionaries representing the users and their owed shares.
            Each dictionary should have keys 'user_id' (int) and 'owed_share' (float).
        - details (dict): Optional details about the expense, such as category or notes.
        - currency_code (str): The ISO 4217 currency code for the expense.

        Returns:
        - expense (dict): The created expense.
        """
        logging.info("Creating an expense with Splitwise")

        url = self.base_url + "create_expense"
        payload = {
            "group_id": group_id,
            "description": description,
            "cost": cost,
            "currency_code": currency_code,
            "users__0__user_id": users[0]["user_id"],
            "users__0__owed_share": users[0]["owed_share"],
            "users__0__paid_share": users[0]["paid_share"],
        }
        if details:
            payload["details"] = json.dumps(details)
        if len(users) > 1:
            for i, user in enumerate(users[1:], start=1):
                payload[f"users__{i}__user_id"] = user["user_id"]
                payload[f"users__{i}__owed_share"] = user["owed_share"]
                payload[f"users__{i}__paid_share"] = user["paid_share"]
        response = self.session.post(url, data=json.dumps(payload))
        return response.json()


class SplitwiseException(Exception):
    """An exception class for Splitwise API errors."""

    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f"{self.status_code}: {self.message}"
