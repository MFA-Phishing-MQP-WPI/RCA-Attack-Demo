#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root."
   exit 1
fi

# Stop hostapd
echo "Stopping hostapd..."
pkill hostapd

# Clear iptables rules
echo "Clearing iptables rules..."
iptables -F
iptables -t nat -F

# Disable IP forwarding
echo "Disabling IP forwarding..."
echo 0 > /proc/sys/net/ipv4/ip_forward

# Reset wireless interface
echo "Resetting wireless interface..."
ifconfig wlan0 down
iw wlan0 set type managed
ifconfig wlan0 up

echo "Shutdown complete. System restored."
