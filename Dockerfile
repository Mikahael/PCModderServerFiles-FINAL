FROM ubuntu:22.04

LABEL author="Aloe" maintainer="aloegovera@gmail.com"

# Update and install dependencies
RUN apt update \
    && apt-get install -y python2.7 python2.7-pip python2.7-dev python2.7-venv \
       libopenal-dev libsdl2-dev libvorbis-dev cmake clang-format rsync git \
    && useradd -m -d /home/container container

# Switch to non-root user
USER container
ENV USER=container HOME=/home/container
WORKDIR /home/container

# Clone the GitHub repository directly into /home/container/
RUN git clone https://github.com/Mikahael/PCModderServerFiles-FINAL.git /home/container \
    && rm -rf /home/container/.git  # Optional: Remove .git folder if you don't need version control inside the container

# Copy entrypoint script and set permissions
USER root
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chown -R container:container /home/container
USER container

# Expose necessary ports
EXPOSE 43210/udp

# Set default command
CMD [ "/bin/bash", "/entrypoint.sh" ]
