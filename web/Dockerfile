FROM node:18.0.0-alpine

RUN mkdir -p /usr/src/proteger-web
WORKDIR /usr/src/proteger-web

COPY . .

RUN npm install

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
