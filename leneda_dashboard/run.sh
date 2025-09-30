#!/bin/sh
set -e

echo "=================================================="
echo "  Leneda Energy Dashboard Starting..."
echo "=================================================="
echo "Version: 1.0.0"
echo "License: GPL-3.0"
echo "Starting web server on port 8099..."
echo "No external dependencies - Pure Python stdlib!"
echo "=================================================="

# Wait for DNS to be ready (prevent startup race condition)
echo "Waiting for DNS to be ready..."
sleep 3

# Verify basic network connectivity
echo "Checking network connectivity..."
if ! ping -c 1 -W 2 8.8.8.8 > /dev/null 2>&1; then
    echo "Warning: Network may not be ready, but continuing..."
fi

# Start the Python HTTP server
cd /app
echo "Starting server..."
exec python3 server.py
