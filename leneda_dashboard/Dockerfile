ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python and pip
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-flask \
    py3-requests

# Copy application files
COPY rootfs/app /app

# Copy and set up the run script
COPY run.sh /run.sh
RUN chmod a+x /run.sh

# Expose port
EXPOSE 8099

# Start the application
CMD ["/run.sh"]
