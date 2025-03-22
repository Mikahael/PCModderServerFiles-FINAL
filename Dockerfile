FROM ubuntu:18.04

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    vim \
    python2.7-dev \
    libsdl2-2.0-0 \
    libpython2.7 \
    ca-certificates \
    libgl1 \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

# Download and extract BombSquad Server (Version 1.4.155)
RUN curl -L https://files.ballistica.net/bombsquad/builds/old/BombSquad_Server_Linux_64bit_1.4.155.tar.gz -o /tmp/bombsquad_server.tar.gz && \
    mkdir -p /BombSquad_Server && \
    tar -zxvf /tmp/bombsquad_server.tar.gz -C /BombSquad_Server --strip 1 && \
    rm /tmp/bombsquad_server.tar.gz

# Set working directory
WORKDIR /BombSquad_Server

# Ensure permissions
RUN chmod +x bombsquad_server

# Use an entrypoint script to run multiple commands
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
