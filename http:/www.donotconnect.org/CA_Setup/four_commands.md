1. `sudo nano /etc/apache2/ssl/openssl-san.cnf`
2. `sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048     -keyout /etc/apache2/ssl/demo-private-key.pem     -out /etc/apache2/ssl/demo-certificate.pem     -config /etc/apache2/ssl/openssl-san.cnf`
3. `openssl x509 -in /etc/apache2/ssl/demo-certificate.pem -text -noout`
4. `sudo systemctl reload apache2`
