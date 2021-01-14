#!/bin/bash
docker run -it --name swingout -v $PWD/swingout:/app -p 8080:80 baxeico/django-uwsgi-nginx
