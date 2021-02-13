

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
sudo useradd admin       
sudo passwd admin  
cd /home    
sudo mkhomedir_helper admin    
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
gunicorn --bind 0.0.0.0:5000 "wsgi:create_app()"    
sudo chown admin:admin /home/admin/CryptoUsersService
test unicorn runs with  
gunicorn --bind 0.0.0.0:5000 wsgi:create_app

user running system service needs to be the one used for the commands above else permission denied 

todo nginx 




### usefull links while trubleshooting deploying 
https://askubuntu.com/questions/760896/how-can-i-fix-apt-error-w-target-packages-is-configured-multiple-times
https://github.com/microsoft/vscode-python/issues/14327






