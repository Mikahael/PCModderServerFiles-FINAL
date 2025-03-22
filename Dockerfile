FROM        ubuntu:22.04

LABEL       author="Aloe" maintainer="aloegovera@gmail.com"

# Install necessary packages
RUN apt update \
    && apt-get install -y python2.7 python2.7-dev python-pip libopenal-dev libsdl2-dev libvorbis-dev cmake clang-format rsync \
    && useradd -m -d /home/container container

# Switch to root to set up permissions
USER root
WORKDIR /home/container

# Copy entrypoint script
COPY ./entrypoint.sh /entrypoint.sh

# Ensure entrypoint script is executable and has correct ownership
RUN chmod +x /entrypoint.sh && chown -R container:container /home/container

# Switch to non-root user
USER container

# Set environment variables
ENV USER=container HOME=/home/container

# Set working directory
WORKDIR /home/container

# Start the container with the entrypoint script
CMD ["/bin/bash", "/entrypoint.sh"]
