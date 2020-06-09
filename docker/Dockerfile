# version 0.2

FROM ubuntu:18.04

# install essentials
RUN apt-get update -y
RUN apt-get install -y nginx
RUN apt-get install -y vim
RUN apt-get install -y apt-utils
RUN apt-get install -y wget
RUN apt-get install -y net-tools
RUN apt-get install -y ufw
RUN apt-get install -y iptables
RUN apt-get install -y curl

# Copy code to working directory
RUN mkdir /app
COPY ./app app

# Install Python 3.7
RUN apt-get install -y python3.7
RUN apt-get install -y build-essential python3-dev
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN apt-get install -y libpython3.7-dev
RUN apt-get install -y python3-distutils

# Install pip
RUN python3.7 get-pip.py
RUN python3.7 -m pip install flask

# install uwsgi
RUN apt-get install -y gcc
RUN python3.7 -m pip install uwsgi

# Create the conf file to run the site
RUN touch /etc/nginx/sites-available/app
RUN echo 'server {\n\tlisten 80;\n\tserver_name load_balancer_app;\n\tlocation / {\n\t\tinclude uwsgi_params;\n\t\tuwsgi_pass unix:/app/load_balancer.sock;\n\t}\n}' >> /etc/nginx/sites-available/app
RUN ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled
RUN mv /etc/nginx/sites-enabled/default ~/

# Reload nginx
RUN /usr/sbin/nginx

RUN mkdir /var/log/uwsgi/

RUN cd /app/ && chmod 777 .

CMD /usr/local/bin/uwsgi --ini /app/app.ini --logto /var/log/uwsgi/access.log --callable app --pidfile=/var/run/uwsgi.pid

EXPOSE 80
