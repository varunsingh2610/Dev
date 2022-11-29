# Specify a base image
FROM node:alpine

# Install some depenendencies
WORKDIR /usr/app
COPY ./package.json ./
RUN npm install
COPY ./ ./

# Default command
CMD ["npm", "start"]