# Use an official Node.js runtime as a parent image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to leverage Docker caching
COPY package.json package-lock.json /app/

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . /app/

# Expose port 3000 for the React app
EXPOSE 3000

# Start the development server
CMD ["npm", "start"] 