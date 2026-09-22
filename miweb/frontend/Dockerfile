FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

# Ajusta "dev" o "start" según el script de tu package.json
CMD ["npm", "run", "dev", "--", "--host"]