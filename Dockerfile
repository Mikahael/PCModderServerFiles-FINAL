FROM ubuntu:22.04

LABEL author="Aloe" maintainer="aloegovera@gmail.com"

# Install dependencies
RUN apt update && apt install -y python2.7-dev \
    software-properties-common \
    git \
    libopenal-dev \
    libvorbis-dev \
    cmake \
    clang-format \
    rsync \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Ensure user exists
RUN id -u container >/dev/null 2>&1 || useradd -m -d /home/container container

# Clone repository into /home/container instead of moving it
RUN git clone https://github.com/Mikahael/PCModderServerFiles-FINAL.git /home/container \
    && chown -R container:container /home/container \
    && chmod +x /home/container/bombsquad_server  # Ensure executable permissions

# Copy and set permissions for entrypoint
USER root
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chown container:container /entrypoint.sh
USER container

# Expose necessary ports
EXPOSE 43210/udp

# Run the startup script
CMD [ "/bin/bash", "/entrypoint.sh" ]
