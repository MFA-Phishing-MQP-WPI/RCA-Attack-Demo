# Rogue Wi-Fi Access Point (RWAP)

## Kali setup

### Get Linux base library
```bash
sudo apt install libnetfilter-queue-dev
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
