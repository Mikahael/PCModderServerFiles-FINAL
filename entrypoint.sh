#!/bin/bash
cd /home/container/bombsquad_server
MODIFIED_STARTUP=`eval echo $(echo ${STARTUP} | sed -e 's/{{/${/g' -e 's/}}/}/g')`
echo ":/home/container$ ${MODIFIED_STARTUP}"
${MODIFIED_STARTUP}

# Ensure the server file is executable
chmod +x bombsquad_server

# Start the BombSquad server
./bombsquad_server
