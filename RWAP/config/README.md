# Config

These files are needed to run the `rwap` malicious network

**Make sure [prerequisite packages](#Prerequisite-Packages) are up to date.**

<br>

## To run
```bash
sudo bash start_up.bash
sudo python3 malicious_network.py
```

<br>

## To stop
```bash
^C
sudo bash shut_down.bash
```

<br>

## Prerequisite Packages
```
sudo apt install libnetfilter-queue-dev
sudo apt install -y hostapd
sudo apt install -y dnsmasq
sudo apt install -y aircrack-ng iptables-persistent net-tools

sudo pip3 install NetfilterQueue --break-system-packages
```
