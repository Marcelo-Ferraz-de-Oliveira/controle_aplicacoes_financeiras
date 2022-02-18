#/bin/bash
cd flask-server
sudo apt install default-jre python3.9 python3-pip chromium-chromedriver -y
pip3 install -r requirements.txt
cp .flaskenv.example .flaskenv
flask run &
cd ../react-frontend
sudo apt install nodejs npm -y
npm install
npm start &
