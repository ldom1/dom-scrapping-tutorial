# Set the base image with the desired Python version
ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}-bookworm AS build

# Install necessary tools
RUN apt-get update && apt-get install -y \
    unzip curl libnss3 chromium-driver \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Download Chromium and Chromedriver
RUN curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/98.0.4758.48/chromedriver_linux64.zip" && \
    curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F950363%2Fchrome-linux.zip?alt=media" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/chrome-linux.zip -d /opt/

FROM python:${PYTHON_VERSION}-bookworm

# Install required libraries for Chromium
RUN apt-get update && apt-get install -y \
    libatk1.0-0 libgtk-3-0 libxcomposite1 libasound2 \
    libxcursor1 libxdamage1 libxext6 libxi6 libxrandr2 libxss1 \
    libxtst6 libpango1.0-0 at-spi2-core libxt6 xvfb x11-xserver-utils \
    dbus libdbus-glib-1-2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the Chromium and Chromedriver binaries from the build stage
COPY --from=build /opt/chrome-linux /opt/chrome
COPY --from=build /opt/chromedriver /opt/

# Setup environment variables
ENV PATH="/opt/chrome:/opt:$PATH"

# Copy the necessary files into the container
COPY dom_scrapping_tutorial /app/dom_scrapping_tutorial
COPY pyproject.toml uv.lock README.md .env /app/

# Install uv at a fixed version
RUN pip install uv==0.5.4

# Install the package
RUN uv pip install . --system

# Expose the port that the app runs on
EXPOSE 8501

# Configure the container to run as an executable
CMD ["uv", "run", "streamlit", "run", "dom_scrapping_tutorial/app.py"]
