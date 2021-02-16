

[![CircleCI](https://circleci.com/gh/athanikos/CryptoUsersService.svg?style=shield&circle-token=9b6d27782cfdf91400ada3189a15ef83a22ef2d7)](https://app.circleci.com/pipelines/github/athanikos/CryptoUsersService)

### Crypto Users Service
A service for managing crypto user data 
Transactions /notifications / Settings


#### deployment instructions    (ubuntu 20.04)
based on https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04   

##### Add user , setup env and download code base
```shell

sudo useradd crypto        
sudo passwd crypto 
cd /opt     
mkdir /opt/cryptoUsersService/
chown -R crypto:crypto cryptoUsersService/
sudo apt update     
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install python3-venv   
cd opt/cryptoUsersService
sudo python3.8 -m venv CryptoUsersServiceEnv     
source CryptoUsersServiceEnv/bin/activate     
pip install wheel   
pip install gunicorn flask      
cd /opt/cryptoUsersService
git clone https://github.com/athanikos/CryptoUsersService       
cd CryptoUsersService/
chown -R crypto:crypto /opt/cryptoUsersService/
pip install --upgrade pip       
pip install -r requirements.txt     
```

set user name and password for mongo authentication 
```shell
python3   
import keyring    
from keyrings.alt.file import PlaintextKeyring    
keyring.set_keyring(PlaintextKeyring())   
keyring.set_password('CryptoUsersService', 'USERNAME', 'someusername') 
keyring.set_password('CryptoUsersService', 'someusername', 'somapass')    
```



open port for service 
```shell
sudo ufw allow 4999
```

##### install & configure mongo 
follow: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/ 

```mongo shell 
use admin;
db.createUser( { user: "", pwd: "", roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] } )
```

```shell 
sudo ufw enable 
sudo ufw allow 27017
```

``` shell 
sudo nano /etc/mongod.conf
```

enter in mongo.conf
```
security:   
    authorization: enabled
net:
    port: 27017 
    bindIp: 127.0.0.1, externalip
```

enter in mongo shell 
```
> use admin 
switched to db admin
> db.auth("crypto","crypto")
db.grantRolesToUser('crypto', [{ role: 'root', db: 'admin' }])
```

##### java, install kafka 
install java jre 
sudo apt-get install openjdk-8-jre

```
cd  /opt 
mkdir kafka
cd kafka
curl https://ftp.cc.uoc.gr/mirrors/apache/kafka/2.7.0/kafka_2.13-2.7.0.tgz -o kafka_2.13-2.7.0.tgz 
tar xvzf kafka_2.13-2.7.0.tgz 
```


##### start on boot,  update crontab 
```
crontab -e 
@reboot /opt/kafka/kafka_2.13-2.7.0/bin/zookeeper-server-start.sh /opt/kafka/kafka_2.13-2.7.0/config/zookeeper.properties
@reboot /opt/kafka/kafka_2.13-2.7.0/bin/kafka-server-start.sh /opt/kafka/kafka_2.13-2.7.0/config/server.properties
@reboot sudo service mongod restart 
```

check gunicorn ,  post with some http client to  and verify response
gunicorn --bind 0.0.0.0:4999 "wsgi:app()"

##### install  nginx 
```shell
https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04
sudo apt update
sudo apt install nginx
sudo ufw app list
sudo ufw allow 4999 
sudo ufw status
```

```shell
cd /etc/nginx/sites-available
sudo nano CryptoUsersService
```

paste the contents of CryptoUsersService.nginx to  /etc/systemd/system/CryptoUsersService 

``` /etc/systemd/system/CryptoUsersService.service 
server {
    listen 4999;
    location / {
        include proxy_params;
        proxy_pass http://unix:/opt/cryptoUsersService/CryptoUsersService/CryptoUsersService.sock;
    }
}
```

```shell
sudo ln -s /etc/nginx/sites-available/CryptoUsersService /etc/nginx/sites-enabled/
```

```shell
sudo nano /etc/systemd/system/CryptoUsersService.service
```
paste the contents of CryptoUsersService.service

```shell
[Unit]
Description=uWSGI instance to serve CryptoUsersService
After=network.target

[Service]
User=nikos
Group=nikos
WorkingDirectory=/opt/cryptoUsersService/CryptoUsersService
Environment="PATH=/opt/cryptoUsersService/CryptoUsersServiceEnv/bin"
ExecStart=/opt/cryptoUsersService/CryptoUsersServiceEnv/bin/gunicorn  --bind unix:CryptoUsersService.sock   "wsgi:app()"

[Install]
WantedBy=multi-user.target
```


enable, start check status
```shell
sudo systemctl enable CryptoUsersService.service
sudo systemctl start  CryptoUsersService.service
sudo systemctl status CryptoUsersService.service
```



