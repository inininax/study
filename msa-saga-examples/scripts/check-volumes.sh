#!/bin/bash

# Docker Volumes 확인 스크립트
# 사용법: ./scripts/check-volumes.sh

echo "=== Docker Volumes 확인 ==="
echo ""

echo "1️⃣ 모든 볼륨 목록:"
docker volume ls
echo ""

echo "2️⃣ 프로젝트 관련 볼륨:"
docker volume ls | grep msa-saga
echo ""

echo "3️⃣ 각 볼륨 상세 정보:"
for volume in order-db-data payment-db-data inventory-db-data delivery-db-data temporal-db-data redis-data kafka-data zookeeper-data; do
    echo ""
    echo "📦 ${volume}:"
    docker volume inspect "msa-saga-examples_${volume}" 2>/dev/null | grep -E '"Mountpoint"|"CreatedAt"|"Driver"' || echo "   볼륨이 존재하지 않습니다."
done

echo ""
echo "4️⃣ 볼륨 사용량:"
docker system df -v | grep -A 20 "VOLUME NAME"

