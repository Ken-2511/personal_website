#!/bin/bash

# Copy the nginx_temp file to the default site configuration
sudo cp nginx_temp /etc/nginx/sites-available/default

# Restart the nginx service to apply the new configuration
sudo systemctl restart nginx

# Output the status of the nginx service
# sudo systemctl status nginx