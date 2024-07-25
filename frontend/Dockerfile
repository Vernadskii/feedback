FROM node:latest

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# port for the development purpose
EXPOSE 5173

# start the development server
CMD ["npm", "run", "dev"]