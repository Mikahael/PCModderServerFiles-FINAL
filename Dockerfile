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

# Ensure the user exists and owns the directory
RUN useradd -m -d /home/container container \
    && chown -R container:container /home/container

# Switch to non-root user
USER container

# Clone the repository (fixes permission issue)
RUN git clone https://github.com/Mikahael/PCModderServerFiles-FINAL.git /home/container/repo \
    && cp -r /home/container/repo/* /home/container/ \
    && rm -rf /home/container/repo

# Set executable permissions
RUN chmod +x /home/container/bombsquad_server

# Copy and set permissions for entrypoint script
COPY --chown=container:container entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
