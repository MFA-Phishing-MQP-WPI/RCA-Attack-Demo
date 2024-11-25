# Rogue Wi-Fi Access Point (RWAP)

## Kali setup

### Get Linux base library
```bash
sudo apt install libnetfilter-queue-dev
sudo apt install -y hostapd
sudo apt install -y dnsmasq
sudo apt install -y aircrack-ng iptables-persistent net-tools
```
### Set Up Virtual Env
```bash
python3 -m venv netfilter_env
source netfilter_env/bin/activate
```
### Install python lib
```bash
pip install NetfilterQueue
pip install scapy
```

### Run the code
```bash
sudo -E python3 network.py
```

### Leave the Virtual Environment
```bash
deactivate
```

```bash
sudo pip3 install NetfilterQueue --break-system-packages
```
