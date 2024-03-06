# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from pprint import pprint
import json
import os
import sheety

import requests

from notification_manager import NotificationManager
from data_manager import DataManager
from flight_search import FlightSearch

from dotenv import dotenv_values
from datetime import datetime, timedelta

config = dotenv_values(".env")

SHEETY_ENDPOINT = "https://api.sheety.co/67d792eba2b7670867546691dbcb375c/flightDeals/prices"
APP_ID = os.environ['ENV_APP_ID']
API_KEY = os.environ['ENV_API_KEY']
# APP_ID = config.get('ENV_APP_ID')
# API_KEY = config.get('ENV_API_KEY')
#
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

# I want to enroll user with below call:
# sheety.enroll_user()

response = requests.get(SHEETY_ENDPOINT, headers=headers)
# print(response.json())
# pprint(response.json())
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()
ORIGIN_CITY_IATA = "BOM"

sheet_data = data_manager.get_data_from_sheet()
pprint(sheet_data)

for row in sheet_data:
  if row['iataCode'] == "":
    row['iataCode'] = flight_search.city_iataCode(row['city'])

data_manager.destination_data = sheet_data
pprint(sheet_data)
data_manager.edit_sheet()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

users = data_manager.get_customer_emails()
emails = [row["email"] for row in users]
names = [row["firstName"] for row in users]

for destination in sheet_data:
  flight = flight_search.check_flights(ORIGIN_CITY_IATA,
                                       destination["iataCode"],
                                       from_time=tomorrow,
                                       to_time=six_month_from_today)
  if flight is None:
    continue

  if flight.price < destination["lowestPrice"]:
    message = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
    for num in range(len(emails)):
      notification_manager.send_email(emails[num], names[num], message)

print("Done")
