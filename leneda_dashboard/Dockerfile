FROM python:3.11-alpine

# No additional packages needed - Python 3 has http.server and urllib built-in

# Copy application files
COPY rootfs/app /app

# Copy and set up the run script
COPY run.sh /run.sh
RUN chmod a+x /run.sh

# Expose port
EXPOSE 8099

# Start the application
CMD ["/run.sh"]
