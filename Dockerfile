#Build container with frontend and backend together, running with gunicorn server

#Build the React frontent
FROM node:16-alpine as build
WORKDIR /controle_aplicacoes_financeiras/react_frontend
ENV PATH /controle_aplicacoes_financeiras/react_frontend/node_modules/.bin:$PATH
COPY ./react_frontend/package.json  ./
COPY ./react_frontend/src ./src
COPY ./react_frontend/public ./public
RUN npm install
RUN npm run build

#Build the Python backend and copy frontend build static files to run togherer in gunicorn
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

#Run gunicorn
EXPOSE 3000
ENV PORT 3000
WORKDIR /controle_aplicacoes_financeiras/python_backend
ARG DB_BASE_NAME
ARG DB_CLUSTER_NAME
ARG DB_PASSWORD
ARG DB_USERNAME
ENV DB_BASE_NAME=$DB_BASE_NAME
ENV DB_CLUSTER_NAME=$DB_CLUSTER_NAME
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_USERNAME=$DB_USERNAME
CMD gunicorn --bind=0.0.0.0:$PORT -t 600 --graceful-timeout 600 webapp.app:app

