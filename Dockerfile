from nginx:latest
COPY dist /home/static/dist
COPY nginx.conf /etc/nginx/nginx.conf