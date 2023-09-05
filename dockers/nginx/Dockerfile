FROM nginx:latest
# COPY ./html /usr/share/nginx/html
RUN apt-get update && apt-get install -y procps

RUN mkdir -p /home/app/staticfiles
RUN mkdir -p /home/app/frontend_files
RUN chmod -R 755 /home/app/staticfiles/
RUN chmod -R 755 /home/app/frontend_files/