# ngrok-bootup-twilio
Notification for ngrok bootup using twilio.  

I created this project for my traveling RaspberryPi project so that I could have a publicly available SSH port for your RaspberryPi, when you didn't know the SSID.

## Installation

1. Install ngrok

To download on a RaspberryPi, follow steps below.  Otherwise, download via https://ngrok.com/download and copy to `/opt/ngrok` directory.

```shell
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
unzip ngrok-stable-linux-arm.zip
sudo mkdir /opt/ngrok
sudo mv ngrok /opt/ngrok/ngrok
```

2. Install ngrok-notify

```
git clone https://github.com/lastcoolnameleft/ngrok-notify.git
cd ngrok-notify
cp env.sh.template env.sh
cp ngrok.yaml.template ngrok.yaml
# Modify env.sh and ngrok.yaml with relevant values
sudo pip3 install -r requirements.txt
sudo ./install.sh
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
