# Guacamole

## Watch it work (YouTube Video)
[![YouTube Video of the attack working](https://img.youtube.com/vi/T32AdTxmNLg/0.jpg)](https://youtu.be/T32AdTxmNLg)

<br>

##### The following assumes you already have `Docker` installed.

<br>

## Set it up

### Set Up `GuacD` and `MySQL` in Docker
```bash
docker run --name guacd --network guac-net -e GUACD_LOG_LEVEL=debug -d guacamole/guacd
docker run --name mysql-server --network guac-net -v $HOME/mysql_init:/docker-entrypoint-initdb.d -v $HOME/mysql_data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=guacamole_root -e MYSQL_USER=guacamole -e MYSQL_PASSWORD=guacamole_password -d mysql:latest
```
```bash
docker exec -it mysql-server /bin/bash
```
* In `mysql-server`
  ```bash
  mysql -p
  // (password="guacamole_root")
  ```
    * In `root`
      ```bash
      GRANT ALL ON guacamole.* TO 'guacamole'@'%';
      exit;
      ```
* In `mysql-server`
  ```bash
  mysql -u guacamole -p
  // (password="guacamole_root")
  ```
    * In `root` as `guacamole`
      ```bash
      use guacamole
      show tables;
      exit;
      ```
* In `mysql-server`
  ```bash
  exit
  ```

<br>

### Set Up `Guacamole` in Docker
```bash
docker run --name guacamole --network guac-net -e MYSQL_DATABASE=guacamole -e MYSQL_USER=guacamole -e GUACD_HOSTNAME=172.18.0.2 -e MYSQL_HOSTNAME=mysql-server -e MYSQL_PASSWORD=guacamole_password -e LOG_LEVEL=debug -d -p 443:8443 guacamole/guacamole
```

<br>

### Optional
```bash
// to leave gui so guac can work run ...
sudo init 3

// this might be an issue for ec2 as it will boot into gui
# 4ec2 -> sudo systemctl set-default multi-user
```

<br>

### Connect Via `SSH` (Native terminal)
```bash
// IP_ADDRESS can be found by running `ip addr` in the vm
ssh <USERNAME>@<IP_ADDRESS>
```

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
