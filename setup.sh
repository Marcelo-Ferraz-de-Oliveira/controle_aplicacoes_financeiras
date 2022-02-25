#/bin/bash
VENV_DIR="venv/"
if [ -d "$VENV_DIR" ]; then
    echo "Dependecies already installed."
    echo "Starting servers..."
    source venv/bin/activate
else
    echo "Installing dependecies and creating virtual python env in $VENV_DIR folder..."
    sudo apt install default-jre python3.9 python3-pip chromium-chromedriver -y
    python3 -m venv venv
    source venv/bin/activate
    cd flask-server
    pip3 install -r requirements.txt
    cp .flaskenv.example .flaskenv
    cd ../react-frontend
    sudo apt install nodejs npm -y
    npm install
cd ..
fi
cd flask-server
flask run &
cd ../react-frontend
npm start &
