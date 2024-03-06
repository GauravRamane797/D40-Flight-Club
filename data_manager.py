from dotenv import dotenv_values
import requests
import os

config = dotenv_values(".env")
SHEET_ENDPOINT = "https://api.sheety.co/67d792eba2b7670867546691dbcb375c/flightDeals/prices"
EDIT_ENDPOINT = "https://api.sheety.co/67d792eba2b7670867546691dbcb375c/flightDeals/prices/"
SHEETY_USERS_ENDPOINT = "https://api.sheety.co/67d792eba2b7670867546691dbcb375c/flightDeals/users"

APP_ID = os.environ['ENV_APP_ID']
API_KEY = os.environ['ENV_API_KEY']
# APP_ID = config.get('ENV_APP_ID')
# API_KEY = config.get('ENV_API_KEY')
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

print(headers)


class DataManager:

  def __init__(self):
    self.destination_data = {}

  # This class is responsible for talking to the Google Sheet.

  def get_data_from_sheet(self):
    response = requests.get(SHEET_ENDPOINT, headers=headers).json()
    print("response", response)
    return response['prices']

  def edit_sheet(self):
    for row in self.destination_data:
      if row['iataCode'] != "":
        body = {'price': {'iataCode': row['iataCode']}}
        print(body)
        endpoint = f"{EDIT_ENDPOINT}{row['id']}"
        print(endpoint)
        response = requests.put(url=endpoint, json=body)
        if response.status_code == 200:
          print("PUT request successful")
        else:
          print("PUT request failed with status code:", response.status_code)
          print("PUT request failed with status code:", response.json())

  def get_customer_emails(self):
    customers_endpoint = SHEETY_USERS_ENDPOINT
    response = requests.get(url=customers_endpoint)
    data = response.json()
    self.customer_data = data["users"]
    return self.customer_data
