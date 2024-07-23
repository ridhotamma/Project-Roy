# Use the official Node.js image as a parent image
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install frontend dependencies
RUN npm install

# Copy the rest of the frontend files
COPY . .

# Expose port 3000 for the frontend
EXPOSE 3000

# Start the frontend application
CMD ["npm", "run", "dev"]
