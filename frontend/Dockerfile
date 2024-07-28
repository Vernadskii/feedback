FROM node:22

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

# port for the development purpose
EXPOSE 5173

# start the development server
CMD ["npm", "run", "dev"]