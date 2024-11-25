#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root."
   exit 1
fi

# Define variables
WLAN_INTERFACE="wlan0"  # WLAN interface for the fake AP
INTERNET_INTERFACE="eth0"  # Internet-connected interface (update if needed)
GATEWAY="192.168.1.1"
SUBNET="255.255.255.0"
HOSTAPD_CONF="/home/jacob/ExecutablesByJacob/hostapd.conf"
DNSMASQ_CONF="/home/jacob/ExecutablesByJacob/dnsmasq.conf"

# Stop interfering services
echo "[*] Stopping interfering services..."
airmon-ng check kill

# Assign static IP to the WLAN interface
echo "[*] Configuring WLAN interface..."
ifconfig $WLAN_INTERFACE $GATEWAY netmask $SUBNET up

# Start hostapd to set up the access point
echo "[*] Starting hostapd to configure access point..."
hostapd $HOSTAPD_CONF &

# Enable IP forwarding
echo "[*] Enabling IP forwarding..."
echo 1 > /proc/sys/net/ipv4/ip_forward

# Set up NAT to forward traffic from WLAN to the internet
echo "[*] Configuring NAT for internet access..."
iptables -t nat -A POSTROUTING -o $INTERNET_INTERFACE -j MASQUERADE
iptables -A FORWARD -i $INTERNET_INTERFACE -o $WLAN_INTERFACE -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i $WLAN_INTERFACE -o $INTERNET_INTERFACE -j ACCEPT

# Start dnsmasq to provide DHCP services
echo "[*] Starting dnsmasq for DHCP..."
dnsmasq --conf-file=$DNSMASQ_CONF

echo "[*] Access point is running. Devices can now connect to SSID: FakeWifi"
