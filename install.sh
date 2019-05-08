#!/usr/bin/env bash

if (( $EUID != 0 )); then
    echo "Please run as root"
    exit 1
fi

cp ngrok.service /lib/systemd/system/
cp notify_ngrok_up.service /lib/systemd/system/

mkdir -p /opt/ngrok
cp ngrok.yaml /opt/ngrok
cp env.sh /opt/ngrok
cp notify_ngrok_up.py /opt/ngrok

systemctl enable ngrok.service
systemctl start ngrok.service
systemctl enable notify_ngrok_up.service
systemctl start notify_ngrok_up.service