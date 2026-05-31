# 00. 학습 로드맵

## 목표

Kubernetes를 "명령어를 따라 치는 수준"에서 "운영 이슈를 해석하고 안정적인 배포를 설계하는 수준"으로 끌어올리는 것이 목표입니다.

## 먼저 익힐 3단계

12주 계획이 길게 느껴진다면 다음 3단계로 압축해서 시작합니다.

| 단계 | 익힐 것 | 성공 기준 |
| --- | --- | --- |
| 1 | Pod, Deployment, Service | 앱을 띄우고 `port-forward`로 접근한다 |
| 2 | ConfigMap, Secret, PVC, Probe | 설정과 데이터를 이미지 밖으로 빼고 Ready 상태를 설명한다 |
| 3 | RBAC, NetworkPolicy, 이벤트, 로그 | 권한과 연결 문제를 `describe`, `logs`, `events`로 좁힌다 |

이후 12주 계획은 같은 주제를 더 넓고 운영적인 관점으로 반복하는 과정입니다.

## 12주 학습 계획

| 주차 | 주제 | 산출물 |
| --- | --- | --- |
| 1 | 컨테이너와 Kubernetes 기본 모델 | Pod와 Deployment 차이 설명 |
| 2 | `kubectl`, YAML, 선언형 관리 | `kubectl diff/apply` 사용 |
| 3 | Workload 리소스 | Deployment 롤아웃/롤백 실습 |
| 4 | Service와 클러스터 네트워킹 | ClusterIP, NodePort, Ingress 비교 |
| 5 | 설정과 Secret | 환경 변수와 볼륨 주입 구성 |
| 6 | 스토리지 | PVC를 사용하는 워크로드 작성 |
| 7 | 리소스와 스케줄링 | requests/limits, affinity, toleration 구성 |
| 8 | 오토스케일링과 가용성 | HPA, PDB 개념과 제약 이해 |
| 9 | 보안과 RBAC | 최소 권한 Role/RoleBinding 작성 |
| 10 | 관측과 장애 대응 | CrashLoopBackOff, ImagePullBackOff 디버깅 |
| 11 | 운영 패턴 | Kustomize, GitOps, 업그레이드 전략 이해 |
| 12 | 캡스톤 | 네임스페이스 단위 서비스 배포와 운영 점검 |

## 단계별 역량 기준

### 입문

- Pod, Deployment, Service의 관계를 그림 없이 말로 설명할 수 있다.
- `kubectl get`, `describe`, `logs`, `exec`, `apply`, `delete`를 사용할 수 있다.
- YAML의 `apiVersion`, `kind`, `metadata`, `spec`, `status`를 구분한다.

### 중급

- Deployment의 ReplicaSet 생성, 롤아웃, 롤백 동작을 설명한다.
- Service 셀렉터 문제, DNS 문제, 포트 매핑 문제를 추적한다.
- ConfigMap, Secret, PVC를 사용해 애플리케이션을 외부화한다.
- 리소스 요청/제한과 probe를 모든 주요 워크로드에 적용한다.

### 숙련

- 장애 증상에서 원인을 좁히는 순서를 갖고 있다.
- RBAC와 NetworkPolicy를 최소 권한 관점에서 설계한다.
- Kustomize 또는 Helm으로 환경 차이를 관리한다.
- 업그레이드, 백업, 배포 전략, 관측, 비용, 보안 기준을 함께 고려한다.

## 학습 규칙

- 문서를 읽은 뒤 바로 예제를 적용합니다.
- YAML은 복사에서 끝내지 말고 최소 한 가지 필드를 직접 바꿔봅니다.
- 실패를 의도적으로 만들어봅니다. `examples/09-troubleshooting/`은 일부러 깨진 예제입니다.
- 정상 상태를 먼저 본 뒤 실패를 만듭니다. 그래야 정상과 비정상의 차이가 보입니다.
- 모든 실습은 `kubectl delete -f <path>` 또는 네임스페이스 삭제로 정리합니다.

## 실습 전제

로컬 클러스터는 다음 중 하나를 사용하면 됩니다.

```bash
kind create cluster --name k8s-study
kubectl cluster-info
```

또는:

```bash
minikube start
kubectl cluster-info
```

기본 확인:

```bash
kubectl get nodes
kubectl get namespace
```

Ingress, HPA, NetworkPolicy는 클러스터 애드온과 CNI 지원 여부에 따라 동작이 달라질 수 있습니다. 해당 실습 문서의 전제를 먼저 확인하세요. 예를 들어 metrics-server가 없으면 HPA는 만들어져도 CPU 메트릭을 읽지 못할 수 있고, NetworkPolicy를 지원하지 않는 CNI에서는 정책 리소스가 있어도 트래픽이 차단되지 않을 수 있습니다.

## 막혔을 때 보는 순서

1. `kubectl config current-context`로 엉뚱한 클러스터를 보고 있지 않은지 확인합니다.
2. `kubectl get all -n k8s-study`로 리소스가 만들어졌는지 확인합니다.
3. `kubectl get events -n k8s-study --sort-by='.lastTimestamp'`로 최근 실패 이유를 봅니다.
4. Pod 문제는 `kubectl describe pod <pod-name> -n k8s-study`와 `kubectl logs <pod-name> -n k8s-study`를 함께 봅니다.
5. 네트워크 문제는 Service selector, endpoint, `port`와 `targetPort`를 차례로 확인합니다.

용어나 명령이 헷갈리면 [용어와 명령어 치트시트](11-glossary-and-cheatsheet.md)를 옆에 열어두고 실습합니다.
