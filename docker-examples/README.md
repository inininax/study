# Docker Database Examples

Docker Compose로 로컬 데이터베이스 실습 환경을 빠르게 띄우기 위한 예제 모음입니다.

이 저장소는 MySQL, PostgreSQL, MongoDB, Redis의 단일 인스턴스 예제와 운영 보조 구성(초기화 스크립트, 백업, 모니터링, 관리 UI)을 포함한 확장 예제를 제공합니다. 모든 예제는 로컬 개발/학습용이며, 프로덕션 배포 전에는 비밀번호, 네트워크 노출, 백업 보관, 접근 제어를 환경에 맞게 다시 검토해야 합니다.

## Prerequisites

- Docker
- Docker Compose v2 (`docker compose`)
- 선택: `openssl` (MongoDB keyfile 재생성 시 사용)

## Directory Structure

```text
docker-examples/
├── mysql/
│   ├── mysql_setup_01.sh
│   ├── mysql_setup_02.sh
│   ├── mysql_01/
│   └── mysql_02/
├── postgres/
│   ├── postgres_setup_01.sh
│   ├── postgres_setup_02.sh
│   ├── postgres_01/
│   └── postgres_02/
├── mongodb/
│   ├── mongodb_setup_01.sh
│   ├── mongodb_setup_02.sh
│   ├── mongodb_01/
│   └── mongodb_02/
└── redis/
    ├── redis_setup_01.sh
    ├── redis_setup_02.sh
    ├── redis_01/
    └── redis_02/
```

`*_01` 디렉터리는 기본 단일 서비스 구성을, `*_02` 디렉터리는 초기 데이터, 백업, Prometheus/Grafana 또는 관리 UI가 포함된 확장 구성을 담습니다. 같은 이름의 `*_setup_*.sh` 스크립트는 해당 예제 구조를 새 경로에 다시 생성할 때 사용합니다.

## Quick Start

예제 디렉터리로 이동한 뒤 Compose 설정을 확인하고 실행합니다.

```bash
cd mysql/mysql_01
cp .env.example .env
docker compose config
docker compose up -d
```

종료와 리소스 정리는 다음처럼 합니다.

```bash
docker compose down
```

데이터 볼륨까지 삭제하려면 `docker compose down -v`를 사용하세요.

## Generate an Example

각 데이터베이스 폴더의 setup 스크립트는 같은 구성을 다른 경로에 생성할 수 있습니다.

```bash
cd postgres
bash postgres_setup_02.sh -p ./my-postgres-lab
cd my-postgres-lab
docker compose up -d
```

기존 경로가 비어 있지 않으면 스크립트가 덮어쓰기 여부를 묻습니다.

## Included Stacks

| Path | Purpose |
| --- | --- |
| `mysql/mysql_01` | MySQL 8 단일 컨테이너, 커스텀 설정, named volume |
| `mysql/mysql_02` | MySQL 8, 초기 SQL, 백업 스크립트, Prometheus/Grafana, mysqld exporter |
| `postgres/postgres_01` | PostgreSQL 15 단일 컨테이너, 커스텀 설정, named volume |
| `postgres/postgres_02` | PostgreSQL 15, 초기 SQL, 백업 스크립트, Prometheus/Grafana, postgres exporter |
| `mongodb/mongodb_01` | MongoDB 6 단일 컨테이너, 커스텀 설정, healthcheck |
| `mongodb/mongodb_02` | MongoDB 6, 초기 사용자 생성, keyfile, 백업 스크립트, mongo-express, Prometheus/Grafana |
| `redis/redis_01` | Redis 7 단일 컨테이너, 비밀번호, 커스텀 설정 |
| `redis/redis_02` | Redis 7 master/replica/sentinel, 백업 스크립트, redis-commander, Prometheus/Grafana |

## Backups

`*_02/backup/backup.sh`는 스크립트 위치를 기준으로 백업 디렉터리를 찾고, 상위 디렉터리의 `.env`가 있으면 자동으로 읽습니다.

```bash
cd redis/redis_02
./backup/backup.sh
```

기본적으로 30일이 지난 백업 파일은 삭제됩니다. 다른 위치에 저장하려면 실행 시 `BACKUP_DIR`를 지정하세요.

```bash
BACKUP_DIR=/tmp/db-backups ./backup/backup.sh
```

## Runtime Files

각 예제에는 필요한 환경변수를 담은 `.env.example`이 있습니다. 실행 전 `.env`로 복사한 뒤 로컬 값에 맞게 수정하세요. Compose 실행 과정에서 `.env`, `data/`, 백업 결과물 등이 생성될 수 있습니다. 이런 파일은 로컬 상태와 비밀값을 포함할 수 있으므로 커밋하지 않습니다.

## Troubleshooting

- 포트 충돌이 나면 각 예제의 `.env`에서 호스트 포트를 변경합니다.
- 설정 파일 변경 후에는 `docker compose config`로 Compose 구문을 먼저 확인합니다.
- 로그는 `docker compose logs -f <service>`로 확인합니다.
- MongoDB keyfile을 새로 만들 때는 `openssl rand -base64 756 > keyfile/mongo-keyfile && chmod 400 keyfile/mongo-keyfile`를 사용합니다.
- `mongodb/mongodb_02`는 `./mongodb_setup_02.sh`를 먼저 실행해야 합니다(keyfile 생성 및 소유권 uid 999 설정 포함).
