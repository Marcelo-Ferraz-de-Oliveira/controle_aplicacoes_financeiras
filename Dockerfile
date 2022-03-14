#Build the React frontent
FROM node:16-alpine as build
WORKDIR /controle_aplicacoes_financeiras/react_frontend
ENV PATH /controle_aplicacoes_financeiras/react_frontend/node_modules/.bin:$PATH
COPY ./react_frontend/package.json  ./
# COPY ./react_frontend/package-lock.json ./
COPY ./react_frontend/src ./src
COPY ./react_frontend/public ./public
RUN npm install
RUN npm run build

#Build the Python backend and copy frontend build to run togherer in gunicorn
FROM python:3.9
WORKDIR /controle_aplicacoes_financeiras/python_backend
COPY --from=build /controle_aplicacoes_financeiras/react_frontend/build ../react_frontend/build

RUN apt update
RUN apt install default-jre chromium-driver -y
RUN mkdir ./webapp
COPY ./python_backend/webapp ./webapp
COPY ./python_backend/requirements.txt ./
RUN pip3 install -r requirements.txt
ENV FLASK_ENV production

EXPOSE 3000
WORKDIR /controle_aplicacoes_financeiras/python_backend
CMD ["gunicorn", "-b",":3000", "-t", "600", "--graceful-timeout", "600", "webapp.app:app"]

# #Build an nginx container
# FROM nginx:stable-alpine
# COPY --from=build /controle_aplicacoes_financeiras/react_frontend/build /usr/share/nginx/html
# RUN rm /etc/nginx/conf.d/default.conf
# COPY nginx.conf /etc/nginx/conf.d
# EXPOSE 80
# CMD ["nginx","-g","daemon off;"]
# COPY deployment/nginx.default.conf /etc/nginx/conf.d/default.conf
#Build the Python backend
# FROM python:3.9
# WORKDIR /controle_aplicacoes_financeiras/python_backend/webapp
# COPY --from=build-step /