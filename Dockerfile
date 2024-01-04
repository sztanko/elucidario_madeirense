# Use the official Python 3.11 image.
FROM python:3.11

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_current.x | bash -
RUN apt-get install -y nodejs

# Install the required packages
RUN apt-get update && apt-get install -y \
    unzip \
    build-essential \
    wget \
    virtualenv \
    libspatialindex-dev \
    git \
    htop \
    jq \
    curl \
    lsb-release \
    apt-transport-https \
    software-properties-common
RUN echo '%gitpod ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/gitpod \
    && addgroup -g 33333 gitpod && adduser -u 33333 -G gitpod -h /home/gitpod -s /bin/bash -D gitpod