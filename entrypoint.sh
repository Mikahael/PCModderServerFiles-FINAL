#!/bin/bash
mv /home/me/* /home/container
cd /home/container
MODIFIED_STARTUP=`eval echo $(echo ${STARTUP} | sed -e 's/{{/${/g' -e 's/}}/}/g')`
echo ":/home/container$ ${MODIFIED_STARTUP}"
${MODIFIED_STARTUP}
echo "Ensuring BombSquad files are in /home/container..."

# Move files to the correct location if necessary
if [ ! -f "/home/container/bombsquad_server" ]; then
    echo "Files not found in /home/container. Moving..."
    mv /BombSquad_Server/* /home/container/ || true
fi

# Set proper permissions
chmod +x /home/container/bombsquad_server

# Verify file existence
ls -lah /home/container

# Start the server
exec /home/container/bombsquad_server "$@"
