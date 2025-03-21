FROM        ubuntu:22.04

LABEL       author="Aloe" maintainer="aloegovera@gmail.com"

RUN         apt update \
    && apt-get install -y python2.7-pip python2.7-dev python2.7-venv libopenal-dev libsdl2-dev libvorbis-dev cmake clang-format rsync \
    && useradd -m -d /home/container container

USER        container
ENV         USER=container HOME=/home/container
WORKDIR     /home/container

COPY        ./entrypoint.sh /entrypoint.sh
CMD         [ "/bin/bash", "/entrypoint.sh" ]
