FROM node:18-alpine
WORKDIR /app
COPY package.json ./
RUN npm install --silent
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npx","serve","-s","build","-l","3000"]
