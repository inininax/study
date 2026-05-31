# 11. 용어와 명령어 치트시트

이 문서는 실습 중 낯선 용어나 명령을 빠르게 다시 확인하기 위한 참조입니다. 처음부터 외우기보다 실습하다 막힐 때 돌아와서 확인합니다.

## 핵심 리소스 한 줄 설명

| 리소스 | 의미 | 먼저 확인할 것 |
| --- | --- | --- |
| Pod | 컨테이너가 실행되는 가장 작은 단위 | `READY`, `STATUS`, 이벤트, 로그 |
| Deployment | Pod 복제와 롤아웃을 관리하는 리소스 | `READY`, rollout 상태, ReplicaSet |
| ReplicaSet | 지정한 Pod 개수를 유지하는 컨트롤러 | Deployment가 만든 결과인지 확인 |
| Service | 바뀌는 Pod IP 앞의 안정적인 접근 지점 | selector, endpoint, port/targetPort |
| Ingress | HTTP/HTTPS 라우팅 규칙 | Ingress Controller 설치 여부 |
| ConfigMap | 민감하지 않은 설정 | env 또는 volume 주입 방식 |
| Secret | 민감한 설정값 | RBAC, Git 커밋 여부, 외부 Secret 관리 |
| PVC | 지속 스토리지 요청 | `Bound` 상태와 StorageClass |
| Job | 완료되어야 하는 일회성 작업 | completion, 실패 횟수, 로그 |
| CronJob | 일정에 따라 Job을 만드는 리소스 | schedule, 생성된 Job |
| HPA | 메트릭 기반 replica 자동 조정 | metrics-server, requests |
| PDB | 자발적 중단 중 최소 가용성 선언 | drain/업그레이드 상황 |
| ServiceAccount | Pod가 API에 접근할 때 쓰는 신원 | 연결된 RoleBinding |
| Role/RoleBinding | namespace 범위 권한과 연결 | subject, resource, verb |
| NetworkPolicy | Pod 간 네트워크 접근 제어 | CNI 지원 여부, 허용 규칙 |

## 자주 보는 상태

| 상태 | 뜻 | 첫 확인 명령 |
| --- | --- | --- |
| `Running` | 컨테이너가 실행 중 | `kubectl logs <pod>` |
| `Pending` | 아직 노드에 배치되거나 준비되지 않음 | `kubectl describe pod <pod>` |
| `ImagePullBackOff` | 이미지 pull 실패 후 재시도 대기 | `kubectl describe pod <pod>` |
| `CrashLoopBackOff` | 컨테이너가 반복 종료됨 | `kubectl logs <pod> --previous` |
| `CreateContainerConfigError` | ConfigMap/Secret 등 실행 전 설정 문제 | `kubectl describe pod <pod>` |
| `Completed` | Job Pod가 정상 완료됨 | `kubectl logs <pod>` |
| `Terminating` | 삭제 중 | finalizer, volume detach, grace period 확인 |

## 기본 명령 흐름

```bash
kubectl config current-context
kubectl get namespace
kubectl get all -n k8s-study
kubectl get events -n k8s-study --sort-by='.lastTimestamp'
```

Pod 확인:

```bash
kubectl get pods -n k8s-study -o wide
kubectl describe pod <pod-name> -n k8s-study
kubectl logs <pod-name> -n k8s-study
kubectl logs <pod-name> --previous -n k8s-study
```

Deployment 확인:

```bash
kubectl rollout status deploy/<name> -n k8s-study
kubectl rollout history deploy/<name> -n k8s-study
kubectl describe deploy/<name> -n k8s-study
kubectl get rs,pod -n k8s-study -l app=<app>
```

Service 확인:

```bash
kubectl get svc,endpoints,endpointslice -n k8s-study
kubectl describe svc <service-name> -n k8s-study
kubectl get pods -n k8s-study --show-labels
```

RBAC 확인:

```bash
kubectl auth can-i get pods \
  --as=system:serviceaccount:k8s-study:pod-reader \
  -n k8s-study
```

## YAML 읽는 순서

1. `apiVersion`: 어떤 API 그룹과 버전인가?
2. `kind`: 어떤 리소스인가?
3. `metadata.name`: 어떤 이름으로 만들어지는가?
4. `metadata.namespace`: 어느 namespace에 만들어지는가?
5. `metadata.labels`: 다른 리소스가 찾을 수 있는 표식은 무엇인가?
6. `spec`: 사용자가 원하는 상태는 무엇인가?
7. `status`: 클러스터가 관측한 현재 상태는 무엇인가?

`status`는 보통 YAML에 직접 작성하지 않습니다. `kubectl get -o yaml`로 조회했을 때 API Server가 채운 현재 상태로 이해합니다.

## 연결 관계 빠른 점검

Service가 Pod를 못 찾을 때:

```bash
kubectl describe svc <service-name> -n k8s-study
kubectl get pods -n k8s-study --show-labels
kubectl get endpoints <service-name> -n k8s-study
```

비교할 값:

- Service의 `spec.selector`
- Pod의 `metadata.labels`
- Pod의 Ready 상태
- Service `targetPort`와 컨테이너 `containerPort`

ConfigMap 또는 Secret이 적용되지 않을 때:

```bash
kubectl get configmap,secret -n k8s-study
kubectl describe pod <pod-name> -n k8s-study
kubectl rollout restart deploy/<name> -n k8s-study
```

PVC가 붙지 않을 때:

```bash
kubectl get storageclass
kubectl get pvc -n k8s-study
kubectl describe pvc <pvc-name> -n k8s-study
```

## 초심자 판단 기준

- `apply` 성공은 리소스 저장 성공입니다. 애플리케이션 준비 완료는 `rollout status`, Pod Ready, endpoint로 다시 확인합니다.
- Pod를 삭제해도 Deployment가 관리하면 다시 만들어집니다. 원인을 고치려면 Pod보다 Deployment YAML을 봅니다.
- Service 접속 실패는 DNS보다 endpoint를 먼저 확인합니다.
- HPA가 만들어져도 metrics-server가 없으면 스케일링 판단을 못 할 수 있습니다.
- NetworkPolicy는 CNI가 지원해야 실제 차단이 동작합니다.
- Secret은 base64 인코딩일 뿐입니다. 운영에서는 암호화와 접근 권한을 별도로 설계합니다.

## 다음으로 돌아갈 문서

- 개념이 헷갈릴 때: [Kubernetes 핵심 개념](01-core-concepts.md)
- 명령 흐름이 헷갈릴 때: [kubectl과 YAML](02-kubectl-and-yaml.md)
- 연결이 안 될 때: [네트워킹](04-networking.md)
- 장애 상태를 만났을 때: [관측과 장애 대응](08-observability-troubleshooting.md)
- 전체 복습을 할 때: [캡스톤 준비](10-ecosystem-and-capstone.md)
