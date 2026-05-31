# Hellophp example (nginx + php + mysql)

```
docker run -i -t --name hellophp ubuntu /bin/bash
```

```
docker attach hellophp
(ctrl + p + q)

apt-get update && apt-get install -y vim curl nginx
```

```
docker-compose up -d
```

```
docker-compose start
docker-compose ps
docker-compose stop
docker-compose down # 삭제
docker-compose down --volume # volume까지 삭제
docker-compose up -d # 수정 시 container 재생성
```