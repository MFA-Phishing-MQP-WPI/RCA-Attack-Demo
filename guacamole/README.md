# Guacamole

[![YouTube Video of the attack working](https://youtu.be/T32AdTxmNLg)](https://youtu.be/T32AdTxmNLg)

```bash
sudo apt install openjdk-11-jdk -y
which keytool

openssl pkcs12 -export \
    -in /etc/ssl/guacamole.crt \
    -inkey /etc/ssl/guacamole.key \
    -out /etc/ssl/guacamole.p12 \
    -name guacamole \
    -CAfile /etc/ssl/myCA.pem -caname root
> INERT_YOUR_PASSWORD_HERE

sudo keytool -importkeystore \
    -deststorepass changeit -destkeypass changeit -destkeystore /etc/ssl/guacamole.jks \
    -srckeystore /etc/ssl/guacamole.p12 -srcstoretype PKCS12 -srcstorepass <<INERT_YOUR_PASSWORD_HERE>> \
    -alias guacamole

// check to make sure keystore file exists in guacamole
ls -l /etc/ssl/guacamole.jks

// if keystore missing, import it
sudo docker cp /etc/ssl/guacamole.jks guacamole:/etc/ssl/guacamole.jks
sudo docker exec -it guacamole ls -l /etc/ssl/guacamole.jks

// update keystore permisions
sudo docker exec -it -u 0 guacamole chmod 644 /etc/ssl/guacamole.jks
sudo docker exec -it -u 0 guacamole chown root:root /etc/ssl/guacamole.jks
```

<br>

```bash
docker exec -it -u 0 guacamole /bin/bash
```
* ```bash
  apt update
  apt install net-tools
  netstat -tulpn
  exit
  ```

<br>

```bash
// copy the server.xml file from this github into your machine, replace "~/signing/server.xml" with it's location
sudo docker cp ~/signing/server.xml guacamole:/usr/local/tomcat/conf/server.xml
docker restart guacamole
docker logs -f guacamole

// LOCATIONS:
// /home/guacamole/tomcat/webapps/guacamole/WEB-INF/classes/logback.xml
// /home/guacamole/.guacamole/guacamole.properties
```





![image](https://github.com/user-attachments/assets/fa81fbad-f44e-40cf-9027-5d2ba4e4da59)
