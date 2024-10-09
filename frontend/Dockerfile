FROM node:18-alpine

WORKDIR /home/node/app

COPY package*.json /home/node/app/

RUN npm install

COPY . /home/node/app
