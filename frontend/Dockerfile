# Use official Node.js image
FROM node:20

# Set working directory inside container
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose the React development server port
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]
