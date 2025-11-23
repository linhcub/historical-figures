FROM nginx:alpine

# Copy custom nginx configuration if you have one
# COPY nginx.conf /etc/nginx/nginx.conf

# Copy static site content (HTML files) to nginx html directory
COPY ../../src/app/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]