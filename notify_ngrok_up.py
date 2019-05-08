#!/usr/bin/python3

# Download the helper library from https://www.twilio.com/docs/python/install
import requests
from twilio.rest import Client
from retrying import retry
import os

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
from_phone_no = os.getenv('TWILIO_FROM_PHONE_NO')
to_phone_no = os.getenv('TWILIO_TO_PHONE_NO')

if (not (account_sid and auth_token and from_phone_no and to_phone_no)):
    print('Required env vars are not set.  Exiting.')
    exit(1)

def send_message(public_url):
    # splitting because python regex sucks
    # Assuming it looks like this:  'tcp://0.tcp.ngrok.io:19091'
    print('Parsing ' + public_url)
    [hostname, port] = public_url.split('tcp://')[1].split(':')
    body = "Your RPi ZeroW is ready: ssh pi@" + hostname + " -p " + port

    client = Client(account_sid, auth_token)
    message = client.messages.create(body=body, from_=from_phone_no, to=to_phone_no)
    print(message.sid)

@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
def get_public_url():
    # Get ngrok tunnel status info
    ngrok_api = 'http://localhost:4040/api/tunnels'
    print("Getting public URL from " + ngrok_api)
    response = requests.get(ngrok_api)
    print("code = " + str(response.status_code))
    print("response = " + response.text)
    response_json = response.json()
    # We only want the SSH tunnel for notification
    public_url = [x['public_url'] for x in response_json['tunnels'] if x['name'] == 'ssh'][0]
    #public_url = response.json()['tunnels'][0]['public_url']
    return public_url

public_url = get_public_url()
send_message(public_url)