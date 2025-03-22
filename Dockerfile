FROM ubuntu:22.04

LABEL author="Aloe" maintainer="aloegovera@gmail.com"

# Update and install dependencies
RUN apt update \
    && apt-get install -y python2.7-dev \
       libopenal-dev libsdl2-dev libvorbis-dev cmake clang-format rsync git \
    && useradd -m -d /home/container container

# Create a non-root user if it doesn't already exist
RUN id -u container >/dev/null 2>&1 || useradd -m -d /home/container container

# Clone the repository into a temporary directory and move files
RUN git clone https://github.com/Mikahael/PCModderServerFiles-FINAL.git /home/temp_container \
    && mv /home/temp_container/* /home/container/ \
    && rm -rf /home/temp_container

# Copy entrypoint script and set permissions
USER root
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chown -R container:container /home/container
USER container

# Expose necessary ports
EXPOSE 43210/udp

# Set the default command
CMD [ "/bin/bash", "/entrypoint.sh" ]
