#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root."
   exit 1
fi

# Stop hostapd
echo "Stopping hostapd..."
pkill hostapd

# Stop dnsmasq
echo "Stopping dnsmasq..."
pkill dnsmasq

# Clear all iptables rules
echo "Clearing iptables rules..."
iptables -F
iptables -t nat -F
iptables -t mangle -F
iptables -X
iptables -t nat -X
iptables -t mangle -X

# Remove any NetfilterQueue rules
echo "Removing NetfilterQueue rules..."
iptables -D INPUT -p udp --dport 53 -j NFQUEUE --queue-num 1 2>/dev/null
iptables -D OUTPUT -p udp --sport 53 -j NFQUEUE --queue-num 1 2>/dev/null
iptables -D FORWARD -p udp --dport 53 -j NFQUEUE --queue-num 1 2>/dev/null
iptables -D FORWARD -p udp --sport 53 -j NFQUEUE --queue-num 1 2>/dev/null

# Disable IP forwarding
echo "Disabling IP forwarding..."
echo 0 > /proc/sys/net/ipv4/ip_forward

# Reset wireless interface
echo "Resetting wireless interface..."
ifconfig wlan0 down
iw wlan0 set type managed
ifconfig wlan0 up

# Kill processes using port 53
echo "Killing processes using port 53..."
fuser -k 53/udp 2>/dev/null
fuser -k 53/tcp 2>/dev/null

echo "Shutdown complete. System restored."
