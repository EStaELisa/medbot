FROM node:18
WORKDIR /app
COPY ../../frontend/package*.json ./
RUN npm install
COPY ../../../frontend .
ENV TZ="Europe/Berlin"
EXPOSE 3000
CMD ["npm", "run", "dev"]