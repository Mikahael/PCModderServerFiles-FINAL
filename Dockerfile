FROM ubuntu:18.04

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    vim \
    python \
    libsdl2-2.0-0 \
    libpython2.7 \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Set working directory to Pterodactyl's expected path
WORKDIR /home/container

# Download and extract BombSquad server files
RUN curl -L https://files.ballistica.net/bombsquad/builds/old/BombSquad_Server_Linux_64bit_1.4.155.tar.gz -o /tmp/bombsquad_server.tar.gz && \
    mkdir -p /home/container && \
    tar -zxvf /tmp/bombsquad_server.tar.gz -C /home/container --strip 1 && \
    rm /tmp/bombsquad_server.tar.gz

# Ensure the server script has executable permissions
RUN chmod +x /home/container/bombsquad_server

# Copy custom entrypoint script to ensure correct startup
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
