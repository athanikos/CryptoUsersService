

[![CircleCI](https://circleci.com/gh/athanikos/CryptoUsersService.svg?style=shield&circle-token=9b6d27782cfdf91400ada3189a15ef83a22ef2d7)](https://app.circleci.com/pipelines/github/athanikos/CryptoUsersService)


### Crypto Users Service
A service for managing crypto user data 
Transactions /notifications / Settings 


#### Environment Setup 
Refer to CryptoStore repository for mongo installation & configuration     
Use keyring to set  username and password for mongo db  

#### capabilities 
get prices  
insert, update, get  transaction  
get balance  (compute)  
get user-notification   
get user-settings 
insert user-channel   
insert user-settings  

#### resources 
WSGI server -  https://www.fullstackpython.com/wsgi-servers.html    
deploy - https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04   

#### deployment instructions (in venv)
sudo useradd crypto        
sudo passwd crypto 
cd /opt     
mkdir /opt/cryptoUsersService/
sudo apt update     
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install python3-venv   
sudo python3.8 -m venv CryptoUsersServiceEnv     
source CryptoUsersServiceEnv/bin/activate     
sudo chown -R admin:admin /home/admin/CryptoUsersServiceEnv
pip install wheel   
pip install gunicorn flask      
git clone https://github.com/athanikos/CryptoUsersService       
cd CryptoUsersService/      
pip install --upgrade pip       
pip install -r requirements.txt     


#notice the parethesis in app since it is a method 
gunicorn --bind 0.0.0.0:4999 "wsgi:app()"


sudo ufw allow 4999

need to su with the user specified in CryptoSuersService.service 
and set the USERNAME and password for the mongo db
 python3   
 import keyring    
 from keyrings.alt.file import PlaintextKeyring    
 keyring.set_keyring(PlaintextKeyring())   
 keyring.set_password('CryptoUsersService', 'USERNAME', 'someusername') 
 keyring.set_password('CryptoUsersService', 'someusername', 'somapass')    

in case errors not allowed when seting keyring create a /.local  folder and give access to user 
sudo mkdir /.local
sudo chown -R "$USER":"$USER" /.local  



user running system service needs to be the one used for the commands above else permission denied 
install  nginx 
https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04
sudo apt update
sudo apt install nginx
sudo ufw app list
sudo ufw allow 4999 
sudo ufw status

cd /etc/nginx/sites-available
sudo nano CryptoUsersService
paste the contents of CryptoUsersService.nginx file 
sudo ln -s /etc/nginx/sites-available/CryptoUsersService /etc/nginx/sites-enabled/

nginx sets :

server {
    listen 4999;
    location / {
        include proxy_params;
        proxy_pass http://unix:/opt/cryptoUsersService/CryptoUsersService/CryptoUsersService.sock;
    }
}




Edit ~/.local/share/python_keyring/keyringrc.cfg:
[backend]
default-keyring=keyrings.alt.file.PlaintextKeyring



sudo nano /etc/systemd/system/CryptoUsersService.service
paste in that file the contents of CryptoUsersService.service

apt-get install build-essential python-dev
apt-get uwsgi
which uwsgi 
paste the path into the CryptoUsersService.service section of uwsgi 


sudo chown -R crypto:crypto /opt/cryptoUsersService/


####make sure mongo is running and start if not 
sudo service mongod status
sudo service mongod start  




### useful links while troubleshooting deployment  
https://github.com/microsoft/vscode-python/issues/14327
https://www.digitalocean.com/community/questions/conflicting-server-name-mydomain-com-on-0-0-0-0-80-ignored-nginx-error-log-ubuntu-20-04
https://www.digitalocean.com/community/questions/wsgi-nginx-error-permission-denied-while-connecting-to-upstream
https://stackoverflow.com/questions/36488688/nginx-upstream-prematurely-closed-connection-while-reading-response-header-from
https://www.datadoghq.com/blog/nginx-502-bad-gateway-errors-gunicorn/
https://stackoverflow.com/questions/39188136/running-flask-with-gunicorn-raises-typeerror-index-takes-0-positional-argumen
https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-apps-using-gunicorn-http-server-behind-nginx
https://lnx.azurewebsites.net/please-enter-password-for-encrypted-keyring-when-running-python-script-on-ubuntu/





#### health checks 
sudo systemctl restart nginx
sudo systemctl restart mongod 
sudo systemctl restart CryptoUsersService 







