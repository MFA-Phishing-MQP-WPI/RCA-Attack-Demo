# What Has Changed?

#### Everything except for `shut_down.bash` and all `.conf` files

<br>

## How to Run

Terminal 1:
```bash
sudo bash start_up.bash
sudo python3 smart_dns.py

 ... packet interception here

^C^C
sudo bash shut_down.bash
```

<br>

Terminal 2 (during packet interception)
```bash
nslookup login.microsoft.com
```
