---
title: " Installation Notes for Flask App on Ubuntu 14.04 LTS using gUnicorn"
date: 2015-01-19T20:58:00.001Z
categories: ["Blogger Archive"]
series: ["Through the Haze"]
---

# Installation Notes for Flask App on Ubuntu 14.04 LTS using gUnicorn

Followed [these excellent directions from Real Python](https://realpython.com/blog/python/kickstarting-flask-on-ubuntu-setup-and-deployment/) and modified for python3 and Ubuntu 14.04.  
Start with updating ubuntu and loading additional packages  

```
> sudo apt-get updatesudo apt-get install -y python3 python3-pip nginx mongodb supervisorsudo pip3 install virtualenv

> sudo mkdir /var/wwwsudo chown ubuntu:ubuntu /var/wwwmkdir /var/www/flask-appmkdir /var/www/flask-app/logscd /var/www/flask-app
```

```

```

Setup virtualenv  

```
virtualenv flask_env
source flask_env/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

## Setup nginx

```
sudo /etc/init.d/nginx start
sudo rm /etc/nginx/sites-enabled/default
sudo touch /etc/nginx/sites-available/flask-app
sudo ln -s /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled/flask-app
sudo vim /etc/nginx/sites-enabled/flask-app
```

Add the following to the nginx flask-app conf file being edited  

```
server {
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
    location /static {
        alias  /var/www/flask-app/flAsk-app/static;
    }
}

sudo service nginx reload
```

## Setup gunicorn start file

Setup bash script to run gunicorn  

```
cd /var/www/flask-app
touch gunicorn_start
chmod a+x gunicorn_start
vim gunicorn_start
```

Insert the following into the gunicorn\_start bash script  

```
#!/bin/bash

NAME="flAsk-app"
FLASKDIR=/var/www/flask-app
VENVDIR=/var/www/flask-app/flask_env
SOCKFILE=/var/www/flask-app/sock
USER=ubuntu

> GROUP=ubuntu

NUM_WORKERS=3

echo "Starting $NAME"

# activate the virtualenv
cd $VENVDIR
source bin/activate

export PYTHONPATH=$FLASKDIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your unicorn
exec gunicorn runserver:app -b 127.0.0.1:8000 \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
```

## Setup Supervisor

This will run and restart the Flask application when the application files are changed.  

```
cd /etc/supervisor/conf.d
sudo vim flask-app.conf
```

Insert the following into the flask-app.conf file:  
> [program:flask-app]  
> command = /var/www/flask-app/gunicorn\_start  
> user = ubuntu  
> stdout\_logfile = /var/www/flask-app/logs/gunicorn\_supervisor.log  
> redirect\_stderr = true

  
Start flask-app gunicorn:  
> sudo supervisorctl update  
> sudo supervisorctl status

You can use the following commands as well:  
> sudo supervisorctl start flask-app  
> sudo supervisorctl start all  
> sudo supervisorctl help|avail|stop|restart

## Test that the application is running
