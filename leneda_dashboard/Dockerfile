FROM python:3.11-alpine

# Install Flask and Requests
RUN pip3 install --no-cache-dir --index-url https://pypi.org/simple flask requests

# Copy application files
COPY rootfs/app /app

# Copy and set up the run script
COPY run.sh /run.sh
RUN chmod a+x /run.sh

# Expose port
EXPOSE 8099

# Start the application
CMD ["/run.sh"]
