FROM node:24-alpine
WORKDIR /app

# Copy the entire application
COPY . /app

# Install dependencies
RUN npm install

# Expose port
EXPOSE 3000

CMD ["npm", "run", "dev", "--", "-H", "0.0.0.0"]