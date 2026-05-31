# Hellopy services

## Your first docker-compose.yml file
docker-compose.yml
```
version: "3"
services:
  web:
    # replace username/repo:tag with your name and image details
    image: take0415/hellopy:0.0.1
    deploy:
      replicas: 5
      resources:
        limits:
          cpus: "0.1" # 10%
          memory: 50M
      restart_policy:
        condition: on-failure
    ports:
      - "4000:80" # local port : container port
    networks:
      - webnet
networks:
  webnet: # which is a load-balanced overlay network
```

## Run your new load-balanced app
- Before we can use the docker stack deploy command we first run:
```
$ docker swarm init
```

- Now let’s run it. You need to give your app a name. Here, it is set to getstartedlab:
```
$ docker stack deploy -c docker-compose.yml getstartedlab
```

- Our single service stack is running 5 container instances of our deployed image on one host. Let’s investigate.
- Get the service ID for the one service in our application:
```
$ docker ps
CONTAINER ID        IMAGE                    COMMAND             CREATED             STATUS              PORTS               NAMES
403ad5179947        take0415/hellopy:0.0.1   "python app.py"     25 seconds ago      Up 22 seconds       80/tcp              getstartedlab_web.4.wgdtga2fba2u5p6dy3bzozxec
0eb22b2526fc        take0415/hellopy:0.0.1   "python app.py"     25 seconds ago      Up 22 seconds       80/tcp              getstartedlab_web.2.fokmr4gk755ob2ppa9bf18c60
481eeff39d59        take0415/hellopy:0.0.1   "python app.py"     25 seconds ago      Up 23 seconds       80/tcp              getstartedlab_web.1.iprq1kifmyexnjpabc6m6qoeg
aa0360d78f92        take0415/hellopy:0.0.1   "python app.py"     25 seconds ago      Up 23 seconds       80/tcp              getstartedlab_web.5.yunav2wlfphrom4tk2wkusydq
fcb1cabc841b        take0415/hellopy:0.0.1   "python app.py"     25 seconds ago      Up 23 seconds       80/tcp              getstartedlab_web.3.n0atirwdhqgw6hnxdruzi1lz2
```

- Look for output for the web service, prepended with your app name. If you named it the same as shown in this example, the name is getstartedlab_web. The service ID is listed as well, along with the number of replicas, image name, and exposed ports.
- A single container running in a service is called a task. Tasks are given unique IDs that numerically increment, up to the number of replicas you defined in docker-compose.yml. List the tasks for your service:
```
$ docker service ps getstartedlab_web
ID                  NAME                  IMAGE                    NODE                DESIRED STATE       CURRENT STATE           ERROR               PORTS
iprq1kifmyex        getstartedlab_web.1   take0415/hellopy:0.0.1   docker-desktop      Running             Running 2 minutes ago
fokmr4gk755o        getstartedlab_web.2   take0415/hellopy:0.0.1   docker-desktop      Running             Running 2 minutes ago
n0atirwdhqgw        getstartedlab_web.3   take0415/hellopy:0.0.1   docker-desktop      Running             Running 2 minutes ago
wgdtga2fba2u        getstartedlab_web.4   take0415/hellopy:0.0.1   docker-desktop      Running             Running 2 minutes ago
yunav2wlfphr        getstartedlab_web.5   take0415/hellopy:0.0.1   docker-desktop      Running             Running 2 minutes ago
```

- Tasks also show up if you just list all the containers on your system, though that is not filtered by service:
```
$ docker container ls -q
403ad5179947
0eb22b2526fc
481eeff39d59
aa0360d78f92
fcb1cabc841b
0a12ece84cd6
```

```
$ curl -4 http://localhost:4000
<h3>Hello World!</h3><b>Hostname:</b> 403ad5179947<br/><b>Visits:</b> <i>cannot connect to Redis, counter disabled</i>
```

## Scale the app
- You can scale the app by changing the replicas value in docker-compose.yml, saving the change, and re-running the docker stack deploy command:
- deploy replicas 변경 후 실행 시 update
```
$ docker stack deploy -c docker-compose.yml getstartedlab
Updating service getstartedlab_web (id: nh4ezozt0cjz4bcpzcxmg2q7i)
```

## Take down the app and the swarm
- Take the app down with docker stack rm:
```
docker stack rm getstartedlab
```

- Take down the swarm.
```
docker swarm leave --force
```