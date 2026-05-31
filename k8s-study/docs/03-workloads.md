# 03. Workload

## Pod

Pod는 하나 이상의 컨테이너가 함께 실행되는 단위입니다. 같은 Pod 안의 컨테이너는 네트워크 네임스페이스와 볼륨을 공유합니다.

Pod를 직접 운영 배포 단위로 쓰는 경우는 드뭅니다. 장애 시 재생성, 롤아웃, 복제 관리가 약하기 때문에 보통 Deployment, StatefulSet, Job 같은 상위 리소스를 사용합니다.

초심자 선택 기준:

| 상황 | 먼저 볼 리소스 |
| --- | --- |
| 계속 떠 있어야 하는 웹/API | Deployment |
| 한 번 실행하고 끝나는 작업 | Job |
| 정해진 시간마다 실행되는 작업 | CronJob |
| 노드마다 하나씩 필요한 에이전트 | DaemonSet |
| 안정적인 이름과 저장소가 필요한 앱 | StatefulSet |

## Deployment

Deployment는 stateless 애플리케이션의 기본 배포 리소스입니다.

주요 기능:

- ReplicaSet을 통해 원하는 Pod 수 유지
- RollingUpdate 전략
- rollout history와 rollback
- 이미지 변경과 설정 변경 반영

```bash
kubectl rollout status deploy/web -n k8s-study
kubectl rollout history deploy/web -n k8s-study
kubectl set image deploy/web nginx=nginx:1.28 -n k8s-study
kubectl rollout undo deploy/web -n k8s-study
```

## ReplicaSet

ReplicaSet은 지정한 개수의 Pod를 유지합니다. 직접 작성하기보다 Deployment가 생성한 결과로 이해하는 경우가 많습니다.

```bash
kubectl get rs -n k8s-study
```

## StatefulSet

StatefulSet은 안정적인 네트워크 이름과 스토리지 정체성이 필요한 워크로드에 사용합니다.

적합한 예:

- 데이터베이스
- 브로커
- 클러스터 멤버십이 필요한 애플리케이션

StatefulSet을 쓸 때는 headless Service, PVC, 업데이트 전략, 백업 전략을 함께 봐야 합니다.

## DaemonSet

DaemonSet은 모든 노드 또는 특정 노드 집합에 Pod를 하나씩 배치합니다.

적합한 예:

- 로그 수집 에이전트
- 노드 모니터링 에이전트
- CNI, CSI 노드 컴포넌트

## Job과 CronJob

Job은 완료되어야 하는 일회성 작업에 사용합니다. CronJob은 스케줄에 따라 Job을 생성합니다.

적합한 예:

- 데이터 마이그레이션
- 정기 리포트 생성
- 주기적 정리 작업

## Probe

Probe는 애플리케이션 생명주기와 트래픽 연결을 제어합니다.

- `startupProbe`: 애플리케이션 시작 시간이 긴 경우 사용합니다.
- `readinessProbe`: 트래픽을 받아도 되는지 판단합니다.
- `livenessProbe`: 재시작이 필요한 비정상 상태인지 판단합니다.

운영에서 readiness와 liveness를 혼동하면 장애를 키울 수 있습니다. readiness 실패는 트래픽 제외이고, liveness 실패는 컨테이너 재시작입니다.

처음에는 `readinessProbe`를 먼저 이해합니다. Service가 준비되지 않은 Pod로 트래픽을 보내지 않도록 막아주기 때문입니다. `livenessProbe`는 앱이 정말 재시작되어야 하는 상태인지 확신할 때 추가합니다.

## 배포 전략

Deployment 기본 전략은 RollingUpdate입니다.

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 1
    maxSurge: 1
```

- `maxUnavailable`: 업데이트 중 사용할 수 없어도 되는 Pod 수입니다.
- `maxSurge`: 원하는 replica 수보다 추가로 만들 수 있는 Pod 수입니다.

## 숙련 포인트

- Deployment YAML에서 selector는 변경이 어렵기 때문에 처음부터 신중히 정합니다.
- 이미지 태그 `latest`는 재현성이 낮습니다. 운영에서는 고정 태그 또는 digest를 사용합니다.
- 모든 장기 실행 워크로드에는 requests, limits, readinessProbe를 기본으로 둡니다.
- 무중단 배포는 Deployment만으로 완성되지 않습니다. 애플리케이션 graceful shutdown, readiness, PDB, 로드밸런서 동작이 함께 맞아야 합니다.

## 실습 연결

[첫 워크로드 실습](../exercises/01-first-workload.md)에서는 Deployment와 Service를 다룹니다. [배치 작업과 Kustomize 실습](../exercises/07-jobs-kustomize.md)에서는 Job과 CronJob을 따로 확인합니다.

## 체크리스트

- [ ] Deployment, StatefulSet, DaemonSet, Job의 사용 사례를 구분할 수 있다.
- [ ] rollout과 rollback을 수행할 수 있다.
- [ ] readinessProbe와 livenessProbe의 차이를 설명할 수 있다.
- [ ] RollingUpdate의 `maxUnavailable`, `maxSurge` 의미를 이해했다.
