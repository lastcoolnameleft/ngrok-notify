# ngrok-notify

Notification for ngrok bootup using gmail to notify me when the device is up and ready

I created this project for my traveling RaspberryPi project so that I could have a publicly available SSH port for my RaspberryPi, when you didn't know the SSID.  It's usually tethered to my phone, so I'll have a "reliable" internet connection

## Installation

1. Install ngrok

To download on a RaspberryPi, follow steps below.  Otherwise, download via https://ngrok.com/download and copy to `/opt/ngrok` directory.

```shell
# https://ngrok.com/download/raspberry-pi
./ngrok --version
# ngrok version 2.3.41 (last verified)
sudo mv ngrok /usr/local/bin/ngrok
```

1. Install ngrok-notify

```
git clone https://github.com/lastcoolnameleft/ngrok-notify.git
cd ngrok-notify
cp env.sh.template env.sh
cp ngrok.yaml.template ngrok.yaml 
# Modify env.sh and ngrok.yaml with relevant values
sudo pip install -r requirements.txt
# https://developers.google.com/workspace/gmail/api/quickstart/python (not sure why it needs to be separate, but I tried adding to requirements and kept having issues)
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# Copy / Build credentials.json
```

1. Verify ngrok + ngrok-notify
```
# Verify ngrok
/usr/local/bin/ngrok start --all --config /home/pi/ngrok-notify/ngrok.yaml

# Verify ngrok-notify
/usr/bin/python /home/pi/ngrok-notify/ngrok-notify.py

# https://github.com/googleworkspace/python-samples/blob/main/gmail/quickstart/quickstart.py
# Run python ./helpers/gmail.py (might need on desktop and then transfer file to RPi)

# After everything works fine and email comes through, install the services
sudo ./install.sh

sudo service ngrok status
journalctl --unit ngrok
sudo service ngrok-notify status
journalctl --unit ngrok-notify
```

## Validation

Verify ngrok tunnels are running:
```shell
curl http://127.0.0.1:4040/api/tunnels
```

Should see something like:

```shell
{"tunnels":[{"name":"ssh","uri":"/api/tunnels/ssh","public_url":"tcp://0.tcp.ngrok.io:15640","proto":"tcp","config":{"addr":"localhost:22","inspect":false},"metrics":{"conns":{"count":0,"gauge":0,"rate1":0,"rate5":0,"rate15":0,"p50":0,"p90":0,"p95":0,"p99":0},"http":{"count":0,"rate1":0,"rate5":0,"rate15":0,"p50":0,"p90":0,"p95":0,"p99":0}}}],"uri":"/api/tunnels"}
```

To validate the notify service is working as expected, start it:
`sudo service ngrok-notify start`

## Debugging

Use these two commands to view the logs from the systemd service that was installed:

`journalctl --unit ngrok`
`journalctl --unit ngrok-notify`
