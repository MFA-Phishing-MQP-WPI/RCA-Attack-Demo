# Malicious Network
Sends users looking for `login.microsoftonline.com` to a hardcoded IP

## Run
1. Terminal 1:
    - To Start
    ```bash
    sudo bash start_up.bash
    python3 malicious_network.py
    ```
    - To Reset
    ```bash
    sudo bash shut_down.bash
    ```

<br>

2. Terminal 2 (or another device)
     ```bash
     nslookup login.microsoftonline.com
     curl login.microsoftonline.com
     ```
     Or go to login.microsoftonline.com via a Web Browser
