FROM node:18
WORKDIR /app
COPY ./package*.json ./
RUN npm install
COPY . .
ENV TZ="Europe/Berlin"
EXPOSE 3000
CMD ["npm", "run", "dev"]