# Use an official Node.js runtime as a parent image
FROM node:20-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the Nuxt.js application
RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

# Copy the built application from the build stage
COPY --from=build /app/.output ./.output

# Copy node_modules from the build stage
# This is a simple approach. For a more optimized image, 
# you could install only production dependencies.
COPY --from=build /app/node_modules ./node_modules
COPY package.json .

# Expose the port the app runs on
EXPOSE 3000

# The command to run the app
# Nuxt 3 server is located in .output/server/index.mjs
CMD ["node", ".output/server/index.mjs"]
