#!/usr/bin/python3

# Download the helper library from https://www.twilio.com/docs/python/install
import google.auth, os, base64, requests, time
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def gmail_send_message():
  """Create and send an email message
  Print the returned  message id
  Returns: Message object, including message id

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  #creds, _ = google.auth.default()
  #if os.path.exists("token.json"):
  creds = None
  if os.path.exists("/home/pi/ngrok-notify/token.json"):
    creds = Credentials.from_authorized_user_file("/home/pi/ngrok-notify/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "/home/pi/ngrok-notify/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("/home/pi/ngrok-notify/token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    ssh_public_url, other_public_urls = get_public_urls()
    # splitting because python regex sucks
    # Assuming it looks like this:  'tcp://0.tcp.ngrok.io:19091'
    print('Parsing ' + ssh_public_url)
    [ngrok_hostname, port] = ssh_public_url.split('tcp://')[1].split(':')
    hostname = os.uname().nodename
    body = hostname + " is ready: ssh pi@" + ngrok_hostname + " -p " + port

    message.set_content(body)

    message["To"] = "tommy@lastcoolnameleft.com"
    message["From"] = "tommy@lastcoolnameleft.com"
    message["Subject"] = "NGROK NOTIFY"

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message


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

# Let things get settled
time.sleep(60)
gmail_send_message()