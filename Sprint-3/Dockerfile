FROM node:19.7-alpine
WORKDIR /usr/src/app
COPY package*.json ./
COPY . .
RUN mkdir -p /usr/src/app
RUN npm install
RUN npm install express-handlebars
EXPOSE 9000
CMD ["node", "index.js"]