# Use Ubuntu 18.04 as base image
FROM ubuntu:18.04

# Install required dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    vim \
    python \
    libsdl2-2.0-0 \
    libpython2.7 \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/container

# Download and extract BombSquad Server into /home/container/bombsquad_server
RUN mkdir -p /home/container/bombsquad_server && \
    curl -L https://files.ballistica.net/bombsquad/builds/old/BombSquad_Server_Linux_64bit_1.4.155.tar.gz -o /tmp/bombsquad_server.tar.gz && \
    tar -zxvf /tmp/bombsquad_server.tar.gz -C /home/container/bombsquad_server --strip-components=1 && \
    rm /tmp/bombsquad_server.tar.gz

# Ensure the server file is executable
RUN chmod +x /home/container/bombsquad_server/bombsquad_server

# Set entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
