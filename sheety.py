import requests
import os

BEARER = os.getenv("BEARER")
USERNAME = os.getenv("USERNAME")

PROJECT = "flightDeals"
SHEET = "users"

base_url = "https://api.sheety.co"

def enroll_user():
  print("Welcome to Angela's Flight Club.\n \
  We find the best flight deals and email them to you.")
  
  first_name = input("What is your first name? ").title()
  last_name = input("What is your last name? ").title()
  
  email1 = "email1"
  email2 = "email2"
  while email1 != email2:
      email1 = input("What is your email? ")
      if email1.lower() == "quit" \
              or email1.lower() == "exit":
          exit()
      email2 = input("Please verify your email : ")
      if email2.lower() == "quit" \
              or email2.lower() == "exit":
          exit()
  
  print("OK. You're in the club!")
  
  post_new_row(first_name, last_name, email1)


def post_new_row(first_name, last_name, email):
  endpoint_url = f"/{USERNAME}/{PROJECT}/{SHEET}"
  url = base_url + endpoint_url

  headers = {
      "Authorization": f"Bearer {BEARER}",
      "Content-Type": "application/json",
  }

  body = {
      "user": {
          "firstName": first_name,
          "lastName": last_name,
          "email": email,
      }
  }

  response = requests.post(url=url, headers=headers, json=body)
  response.raise_for_status()
  print(response.text)
  