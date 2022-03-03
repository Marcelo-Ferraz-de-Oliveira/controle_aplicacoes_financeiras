VENV_DIR=venv

install:
	@if [ -d $(VENV_DIR) ]; then \
		echo "Dependecies already installed in $(VENV_DIR)."; \
	 else \
	 	echo "Installing in $(VENV_DIR)"; \
	 	sudo apt install default-jre python3.9 python3-pip chromium-chromedriver -y && python3 -m venv $(VENV_DIR); \
	 	. $(VENV_DIR)/bin/activate && cd python_backend && pip3 install -r requirements.txt && cd webapp && cp .flaskenv.example .flaskenv; \
		cd ../../react_frontend && sudo apt install nodejs npm -y && npm install; \
	fi

start:
	@if [ -d $(VENV_DIR) ]; then \
		export PYTHONPATH="$${PWD}/python_backend"; \
		. $(VENV_DIR)/bin/activate && cd python_backend/webapp && flask run & \
		cd react_frontend && npm start & \
	else \
		echo "Execute make install first"; \
	fi

stop:
	@lsof -i :5000 | grep "5000" | awk '{print $$2}' | xargs -r kill -9
	@lsof -i :3000 | grep "3000" | awk '{print $$2}' | xargs -r kill -9
	@clear
