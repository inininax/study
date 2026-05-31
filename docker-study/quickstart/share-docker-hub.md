# Share images on Docker Hub Example

## Set up your Docker Hub account
```
docker login
```

## Create a Docker Hub repository and push your image
```
<Docker ID>/<Repository Name>:<tag>
```
```
docker tag bulletinboard:1.0 gordon/bulletinboard:1.0
docker push gordon/bulletinboard:1.0
```