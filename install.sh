#!/usr/bin/env bash

if (( $EUID != 0 )); then
    echo "Please run as root"
    exit 1
fi

cp ngrok.service /lib/systemd/system/
cp ngrok_notify.service /lib/systemd/system/

mkdir -p /opt/ngrok
cp ngrok.yaml /opt/ngrok
cp env.sh /opt/ngrok
cp ngrok_notify.py /opt/ngrok

systemctl enable ngrok.service
systemctl restart ngrok.service
systemctl enable ngrok_notify.service
systemctl restart ngrok_notify.service