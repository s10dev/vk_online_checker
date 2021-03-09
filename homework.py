import requests
import os
import time
from twilio.rest import Client
from dotenv import load_dotenv
import datetime
load_dotenv()


def get_status(user_id):
    url = 'https://api.vk.com/method/users.get'
    data = {
        'access_token' : os.getenv('token'),
        'user_ids': user_id,
        'v': os.getenv('ver'),
        'fields': 'online',
    }

    try:
        response = requests.post(url, params = data).json().get('response')
    except requests.exceptions.RequestException:
        logger.error(f'Ошибка: {requests.exceptions.RequestException}')
    status = response[0]['online']

    return status


def sms_sender(text):
    account_sid = os.getenv('sid')
    auth_token = os.getenv('sms_token')
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=text,
                        from_=os.getenv('from'),
                        to=os.getenv('to')
                    )

    return message.sid


if __name__ == "__main__":
    user_id = 436744680

    while True:
        if get_status(user_id):
            sms_sender(f"Tracking user is online. Enter date: {datetime.datetime.now()}")
            break
        time.sleep(1)