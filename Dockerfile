FROM python:3.11.4

# Install Node.js and Puppeteer dependencies
RUN apt-get update && apt-get install -y wget gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    libxss1 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libcups2 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the Python requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && apt-get install -y npm

# Install Puppeteer
RUN npm i puppeteer

# Add your application code
COPY . /app

CMD ["python", "main.py"]












# # Use marvelapp/node-puppeteer as the base image
# FROM marvelapp/node-puppeteer
#
# # Set the working directory in the container to /app
# WORKDIR /app
#
# # Copy your application code to the container
# COPY . .
#
# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt
#
# # Set the command to run your application
# CMD ["python", "main.py"]
#






# # Stage 1: Build Python environment
# FROM python:3.11.4 AS python-env
#
# WORKDIR /app
#
# # Copy Python requirements file and install Python dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
#
# # Stage 2: Build Node.js environment and install Puppeteer
# FROM node:20.10.0 AS node-env
#
# # Install necessary libraries for Puppeteer (Google Chrome)
# RUN apt-get update \
#     && apt-get install -y wget gnupg \
#     && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
#     && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
#     && apt-get update \
#     && apt-get install -y \
#         google-chrome-stable \
#         libxss1 \
#         libx11-xcb1 \
#         libxcomposite1 \
#         libxcursor1 \
#         libxdamage1 \
#         libxi6 \
#         libxtst6 \
#         libcups2 \
#         libxrandr2 \
#         libasound2 \
#         libpangocairo-1.0-0 \
#         libatk1.0-0 \
#         libatk-bridge2.0-0 \
#         libgtk-3-0 \
#         libnss3 \
#         libxshmfence1 \
#         libgbm1 \
#         libdrm2 \
#         libcairo2 \
#         libatspi2.0-0 \
#         libdbus-1-3 \
#         libc6 \
#         libcomerr2 \
#         libexpat1 \
#         libgcc1 \
#         libgdk-pixbuf2.0-0 \
#         libglib2.0-0 \
#         libgomp1 \
#         libnspr4 \
#         libnss3 \
#         libpango-1.0-0 \
#         libpangocairo-1.0-0 \
#         libstdc++6 \
#         libx11-6 \
#         libx11-xcb1 \
#         libxau6 \
#         libxcb1 \
#         libxdmcp6 \
#         libxext6 \
#         libxfixes3 \
#         libxi6 \
#         libxrender1 \
#         libxss1 \
#         libxtst6 \
#         zlib1g \
#     && rm -rf /var/lib/apt/lists/*
#
# WORKDIR /node_app
#
# # Copy package.json and package-lock.json for Node.js project
# COPY package.json package-lock.json ./
#
# # Install npm dependencies, including Puppeteer
# RUN npm install
#
# # Stage 3: Final image with Python and Node.js
# FROM python:3.11.4 AS final
#
# # Copy Python environment
# COPY --from=python-env /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
#
# # Copy Node.js environment, including Puppeteer
# COPY --from=node-env /node_app/node_modules /app/node_modules
# COPY --from=node-env /usr/local/bin/node /usr/local/bin/node
# COPY --from=node-env /usr/local/lib/node_modules /usr/local/lib/node_modules
#
# # Copy the rest of your application code
# COPY . /app
#
# WORKDIR /app
#
# CMD ["python", "main.py"]
#
#
#





# # Stage 1: Build Python environment
# FROM python:3.11.4 AS python
#
# WORKDIR /app
#
# COPY requirements.txt .
#
# RUN pip install --no-cache-dir -r requirements.txt
#
# # Stage 2: Build Node.js environment and install puppeteer
# FROM node:20.10.0 AS node
#
# WORKDIR /node_app
#
# COPY package.json package-lock.json ./
#
# # Install npm dependencies, including puppeteer
# RUN npm install
#
# # Stage 3: Final image with Python and Node.js
# FROM python:3.11.4 AS final
#
# # Copy Python environment
# COPY --from=python /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
#
# # Copy Node.js environment, including puppeteer
# COPY --from=node /node_app/node_modules /app/node_modules
#
# # Copy the rest of your application code
# COPY . /app
#
# WORKDIR /app
#
# CMD ["python", "main.py"]
