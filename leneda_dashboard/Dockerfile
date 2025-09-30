FROM python:3.11-alpine

# Install minimal dependencies
RUN pip install --no-cache-dir flask requests

# Copy application files
COPY rootfs/app /app

# Copy and set up the run script
COPY run.sh /run.sh
RUN chmod a+x /run.sh

# Expose port
EXPOSE 8099

# Start the application
CMD ["/run.sh"]
