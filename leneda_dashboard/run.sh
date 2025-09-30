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

# Start the Python HTTP server
cd /app
exec python3 server.py
