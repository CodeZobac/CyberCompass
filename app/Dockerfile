FROM node:18-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app
COPY . .

# Expose Next.js development port
EXPOSE 3000

# Start the app in development mode
CMD ["npm", "run", "dev"]