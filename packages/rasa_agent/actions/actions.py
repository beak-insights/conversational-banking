import os
from typing import Any, Text, Dict, List

from httpx import AsyncClient
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

BANK_API = os.getenv('BANK_API')

async def bank_request(url, data):
    print("bank_request", url, data)
    async with AsyncClient(base_url=BANK_API) as client:
        try:
            response = await client.post(url, json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except Exception as err:
            print(f"Other error occurred: {str(err)}")
            return {"error": f"An unexpected error occurred: {str(err)}"}


class ActionVerifyTargetAccounts(Action):
    def name(self) -> Text:
        return "action_verify_target_accounts"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        source_account = tracker.get_slot("source_account")
        recipient_account = tracker.get_slot("recipient_account")
        user_id = tracker.sender_id
        response = await bank_request("/balance", {"user_id": user_id})
        if source_account == recipient_account:
            dispatcher.utter_message(
                template="utter_source_recipient_account_same"
            )
            return [SlotSet("correct_target_accounts", False)]
        return [SlotSet("correct_target_accounts", True)]


class ActionCheckBalance(Action):
    def name(self) -> Text:
        return "action_check_balance"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        accounts = tracker.get_slot("account_names")
        print("=========================================================")
        print(resp)
        print("=========================================================")
        return [SlotSet("accounts_balances", resp)]


class ActionCheckSufficientFunds(Action):
    def name(self) -> Text:
        return "action_check_sufficient_funds"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # hard-coded balance for tutorial purposes. in production this
        # would be retrieved from a database or an API
        user_id = tracker.sender_id
        try:
            msg_from = tracker.latest_message["metadata"]["message"]["from"]
        except KeyError:
            ...
        balance = 1000
        transfer_amount = tracker.get_slot("amount")
        # account_source = tracker.get_slot("account_source")
        response = await bank_request("/balance", {"user_id": user_id, "account_type": "savings"})
        print(response)
        has_sufficient_funds = transfer_amount <= balance
        return [SlotSet("has_sufficient_funds", has_sufficient_funds)]
