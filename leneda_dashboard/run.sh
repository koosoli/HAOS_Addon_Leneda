#!/bin/sh
set -e

echo "=================================================="
echo "  Leneda Energy Dashboard Starting..."
echo "=================================================="
echo "Version: 0.1.0"
echo "Starting web server on port 8099..."
echo "=================================================="

# Start the Flask application
cd /app
exec python3 server.py
