# Set the base image with the desired Python version
ARG PYTHON_VERSION=3.10

FROM public.ecr.aws/lambda/python:${PYTHON_VERSION} AS build

# Install Chromium and Chromedriver
RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/98.0.4758.48/chromedriver_linux64.zip" && \
    curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F950363%2Fchrome-linux.zip?alt=media" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/chrome-linux.zip -d /opt/

FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}

RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y

# Set the working directory
WORKDIR /var/task

# Copy the Chromium and Chromedriver binaries from the build stage
COPY --from=build /opt/chrome-linux /opt/chrome
COPY --from=build /opt/chromedriver /opt/

# Setup environment variables
ENV PATH="/opt/chrome/stable:/opt/chromedriver/stable:$PATH"

# Copy entrypoint: https://docs.aws.amazon.com/fr_fr/lambda/latest/dg/images-test.html
# Install locally the AWS Lambda Runtime Interface Emulator
# curl -Lo aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie \
# && chmod +x aws-lambda-rie
# Install AWS Lambda RIE for local emulation and awslambdaric for runtime interface
COPY aws-lambda-rie /usr/local/bin/aws-lambda-rie
RUN chmod +x /usr/local/bin/aws-lambda-rie \
    && pip install awslambdaric

# Copy the entry script into the container and make it executable
COPY entry_script.sh /entry_script.sh
RUN chmod +x /entry_script.sh

# Copy the necessary files into the container
COPY dom_scrapping_tutorial /var/task/dom_scrapping_tutorial
COPY pyproject.toml uv.lock README.md .env /var/task/

# Install uv at a fixed version
RUN pip install uv==0.5.4

# Install the package
RUN uv pip install . --system

# Configure the container to run as an executable
ENTRYPOINT ["/entry_script.sh"]
CMD ["dom_scrapping_tutorial.handler.handler"]