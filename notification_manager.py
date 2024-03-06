import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import dotenv_values

config = dotenv_values(".env")
# MY_PASSWORD = config.get('MY_PASSWORD_VARIABLE')
MY_PASSWORD = os.environ['MY_PASSWORD_VARIABLE']
# print("MY_PASSWORD", MY_PASSWORD)
# MY_EMAIL = config.get('MY_EMAIL')
MY_EMAIL = os.environ['MY_EMAIL']


# print("MY_EMAIL", MY_EMAIL)

class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    def send_email(self, email, name,message):
        # with open("./quotes.txt", "r") as data:
        #   quotes = data.readlines()

        # quote_of_day = random.choice(quotes)
        # print(quotes)
        # print(quote_of_day)
        # msg = MIMEMultipart()
        # msg.attach(MIMEText(message.encode('utf-8'), 'plain', 'utf-8'))

        msg = MIMEText(message, 'plain', 'utf-8')
        msg['Subject'] = f"{name} !! We got lower flight ticket!"
        msg['From'] = MY_EMAIL
        msg['To'] = email

        print("message", message)
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=email,
                # msg=f"Subject:We got lower flight ticket!\n\n Lower ticket is as below\n{msg.as_string()}"
                msg=msg.as_string()
            )
