# Use the official Node.js 18 image as the base image
FROM node:18

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json into the container
COPY ./package*.json ./

# Install the project dependencies
RUN npm install

# Copy the entire application source code into the container
COPY . .

# Set the timezone to Europe / Berlin
ENV TZ="Europe/Berlin"

# Expose port 3000 for incoming connectionos
EXPOSE 3000

# Define the command to start the development server
CMD ["npm", "run", "dev"]