# Use a lightweight Ubuntu base image
FROM ubuntu:20.04

# Set the working directory
WORKDIR /home/container

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

# Create a non-root user if it doesn't exist
RUN id -u container >/dev/null 2>&1 || useradd -m -d /home/container container

# Clone the repository (overwrite existing files)
RUN rm -rf /home/container && git clone https://github.com/Mikahael/PCModderServerFiles-FINAL.git /home/container

# Ensure proper ownership and permissions
RUN chown -R container:container /home/container \
    && chmod +x /home/container/bombsquad_server

# Set the user to "container" (non-root)
USER container

# Set the default entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
