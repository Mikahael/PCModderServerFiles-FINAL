# Use a lightweight Ubuntu base image
FROM ubuntu:22.04

# Set the working directory
WORKDIR /home/container

# Install dependencies in one step (reduces layer size)
RUN apt update && apt install -y \
    python2.7-dev \
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

# Create a non-root user if it doesn't exist
RUN useradd -m -d /home/container container

# Switch to the container user before cloning
USER container

# Clone the repository (without unnecessary deletion)
RUN git clone https://github.com/Mikahael/PCModderServerFiles-FINAL.git /home/container

# Ensure executable permissions (only needed for files that require it)
RUN chmod +x /home/container/bombsquad_server

# Copy and set permissions for entrypoint script
COPY --chown=container:container entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
