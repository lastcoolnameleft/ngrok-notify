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

def send_message():
    ssh_public_url, other_public_urls = get_public_urls()
    # splitting because python regex sucks
    # Assuming it looks like this:  'tcp://0.tcp.ngrok.io:19091'
    print('Parsing ' + ssh_public_url)
    [ngrok_hostname, port] = ssh_public_url.split('tcp://')[1].split(':')
    hostname = os.uname().nodename
    body = hostname + " is ready: ssh pi@" + ngrok_hostname + " -p " + port
    if other_public_urls:
        body += " Other Endpoints: " + other_public_urls

    print('Sending: ' + body)
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=body, from_=from_phone_no, to=to_phone_no)
    print(message.sid)

@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
def get_public_urls():
    # Get ngrok tunnel status info
    ngrok_api = 'http://localhost:4040/api/tunnels'
    print("Getting public URL from " + ngrok_api)
    response = requests.get(ngrok_api)
    print("code = " + str(response.status_code))
    print("response = " + response.text)
    response_json = response.json()
    # We only want the SSH tunnel for notification
    ssh_public_url = [x['public_url'] for x in response_json['tunnels'] if x['name'] == 'ssh'][0]
    other_public_urls = ', '.join(['(' + x['name'] + ') ' + x['public_url'] for x in response_json['tunnels'] if x['name'] != 'ssh'])
    #public_url = response.json()['tunnels'][0]['public_url']
    return ssh_public_url, other_public_urls

send_message()
