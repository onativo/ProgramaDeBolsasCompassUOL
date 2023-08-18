FROM node:19.7-alpine
COPY package*.json ./
COPY . .
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN npm install
RUN npm install express-handlebars
EXPOSE 80
CMD ["node", "app.js"]