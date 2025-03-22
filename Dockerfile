# syntax=docker/dockerfile:1

# Base image
ARG base_image=ubuntu:22.04

#-------------------------------DOWNLOADER--------------------------------
FROM ${base_image} AS downloader

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies for downloading
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
        wget \
        tar \
        rsync && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /tmp/downloads

# Download BombSquad server and extract it
RUN wget --no-check-certificate -O bombsquad_server.tar.gz "https://files.ballistica.net/bombsquad/builds/old/BombSquad_Linux_64bit_1.4.155.tar.gz" && \
    mkdir extracted && \
    tar -xvzf bombsquad_server.tar.gz -C extracted

#-------------------------------RUNNER--------------------------------
FROM ${base_image} AS runner

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Install Python 2.7 (required for BombSquad)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y \
        python2.7-dev && \
    rm -rf /var/lib/apt/lists/*

# Add a container user
RUN useradd -m -s /bin/bash container

# Copy BombSquad server files from the downloader stage
COPY --from=downloader /tmp/downloads/extracted /home/container/

# Set working directory
WORKDIR /home/container

# Copy entrypoint script
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chown -R container:container /home/container

# Set user
USER container
ENV USER=container HOME=/home/container

# Expose required port for BombSquad
EXPOSE 43210/udp

# Run BombSquad server
CMD [ "/entrypoint.sh" ]
