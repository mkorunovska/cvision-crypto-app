FROM node:24-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci --silent

COPY . ./

EXPOSE 5173

CMD ["npm", "run", "dev"]