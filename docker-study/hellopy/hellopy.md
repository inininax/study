# Hellopy

## Define a container with Dockerfile
### Dockerfile
```
# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
```

## The app itself
### requirements.txt
```
Flask
Redis
```

### app.py
```
from flask import Flask
from redis import Redis, RedisError
import os
import socket

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
```

## Build the app
```
$ ls
Dockerfile		app.py			requirements.txt
```

```
$ docker build -t hellopy .
```

```
$ docker images

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
hellopy             latest              dd747be0ec95        10 seconds ago      159MB
python              2.7-slim            eeb27ee6b893        9 days ago          148MB
```

## Run the app
```
$ docker run --name test-hellopy -p 4000:80  hellopy

 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)
172.17.0.1 - - [30/Apr/2020 11:01:32] "GET / HTTP/1.1" 200 -
```

Now let’s run the app in the background, in detached mode:
```
$ docker run --name test-hellopy -d -p 4000:80  hellopy
```

```
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                  NAMES
2135d126170b        hellopy             "python app.py"     43 seconds ago      Up 41 seconds       0.0.0.0:4000->80/tcp   test-hellopy
0a12ece84cd6        ubuntu              "/bin/bash"         3 hours ago         Up 3 hours                                 test-ubuntu
```

```
docker stop test-hellopy
```

## Share your image

### Log in with your Docker ID
```
docker login
```

### Tag the image
```
docker tag <image> <username>/<repository>:<tag>
```

```
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
hellopy             latest              dd747be0ec95        17 minutes ago      159MB
python              2.7-slim            eeb27ee6b893        9 days ago          148MB

$ docker tag hellopy take0415/hellopy:0.0.1

$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
hellopy             latest              dd747be0ec95        18 minutes ago      159MB
take0415/hellopy    0.0.1               dd747be0ec95        18 minutes ago      159MB
python              2.7-slim            eeb27ee6b893        9 days ago          148MB
```

### Publish the image
```
docker push <username>/<repository>:<tag>
```
```
docker push take0415/hellopy:0.0.1
```

### Pull and run the image from the remote repository
```
docker run -p 4000:80 <username>/<repository>:<tag>
```
```
docker run --name test-hellopy -p 4000:80 take0415/hellopy:0.0.1
```
