# 01. Kubernetes 핵심 개념

## Kubernetes가 해결하는 문제

Kubernetes는 컨테이너를 여러 노드에 배치하고, 원하는 개수로 유지하며, 장애가 나면 다시 만들고, 네트워크와 설정을 일관되게 연결해주는 오케스트레이션 시스템입니다.

핵심은 "현재 상태를 직접 조작"하는 것이 아니라 "원하는 상태를 선언"하는 것입니다.

```text
사용자 YAML -> API Server -> etcd 저장 -> Controller가 차이를 감지 -> Scheduler/Kubelet이 실행
```

초심자는 다음 연결만 먼저 잡아도 문서 읽기가 쉬워집니다.

```text
Deployment -> ReplicaSet -> Pod
Service -> label selector -> Pod
ConfigMap/Secret -> env 또는 volume -> Pod
```

Kubernetes를 볼 때는 "누가 누구를 만들고, 어떤 label로 연결되는가"를 계속 확인합니다.

## 클러스터 구성 요소

### Control Plane

- API Server: 모든 요청의 입구입니다. `kubectl`도 API Server와 통신합니다.
- etcd: 클러스터 상태를 저장하는 분산 키-값 저장소입니다.
- Scheduler: 아직 노드가 배정되지 않은 Pod를 적절한 노드에 배치합니다.
- Controller Manager: Deployment, ReplicaSet, Node 등 여러 컨트롤러를 실행합니다.
- Cloud Controller Manager: 클라우드 로드밸런서, 노드, 볼륨 같은 클라우드 리소스와 연결합니다.

### Worker Node

- kubelet: 노드의 에이전트입니다. PodSpec을 받아 컨테이너 런타임에 실행을 요청합니다.
- kube-proxy: Service 네트워킹 규칙을 구성합니다.
- Container Runtime: containerd, CRI-O 같은 런타임입니다.

## Kubernetes Object의 기본 구조

대부분의 리소스는 다음 구조를 갖습니다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: k8s-study
spec:
  replicas: 2
status:
  availableReplicas: 2
```

- `apiVersion`: API 그룹과 버전입니다.
- `kind`: 리소스 종류입니다.
- `metadata`: 이름, 네임스페이스, 라벨, 어노테이션입니다.
- `spec`: 사용자가 원하는 상태입니다.
- `status`: 시스템이 관측한 현재 상태입니다. 보통 직접 작성하지 않습니다.

처음 YAML을 읽을 때는 모든 필드를 이해하려 하지 말고 다음 순서로 봅니다.

1. `kind`: 어떤 종류의 리소스인가?
2. `metadata.name`과 `metadata.namespace`: 어디에 어떤 이름으로 만들어지는가?
3. `spec.selector`와 `metadata.labels`: 다른 리소스와 어떻게 연결되는가?
4. `spec.template`: 실제 Pod에는 어떤 설정이 들어가는가?
5. `status`: 클러스터가 현재 무엇을 관측했는가?

## Namespace, Label, Annotation

### Namespace

Namespace는 리소스를 논리적으로 분리합니다. 팀, 환경, 실습 범위를 나눌 때 사용합니다.

```bash
kubectl get all -n k8s-study
```

### Label

Label은 셀렉터로 검색하고 연결하기 위한 키-값입니다. Service가 Pod를 찾을 때도 label selector를 사용합니다.

```yaml
metadata:
  labels:
    app: web
    tier: frontend
```

### Annotation

Annotation은 사람이 읽거나 도구가 사용하는 부가 정보입니다. 셀렉터에는 사용하지 않습니다.

```yaml
metadata:
  annotations:
    owner: platform-team
```

## Controller와 Reconciliation

Kubernetes 컨트롤러는 반복적으로 현재 상태와 원하는 상태를 비교합니다. Deployment에 `replicas: 3`을 선언했는데 Pod가 2개뿐이면 컨트롤러가 Pod를 하나 더 만들도록 조정합니다.

이 모델 때문에 Kubernetes에서는 다음 질문을 자주 해야 합니다.

- 내가 선언한 원하는 상태는 무엇인가?
- 컨트롤러가 관측한 현재 상태는 무엇인가?
- 둘이 다르다면 어떤 이벤트가 남았는가?

## 꼭 기억할 모델

- Pod는 Kubernetes에서 배포 가능한 가장 작은 실행 단위입니다.
- Deployment는 Pod를 직접 대체하고 롤아웃을 관리하는 상위 리소스입니다.
- Service는 Pod IP가 바뀌어도 안정적인 접근 지점을 제공합니다.
- ConfigMap과 Secret은 설정을 이미지 밖으로 분리합니다.
- Namespace, Label, Selector가 연결 관계의 핵심입니다.

## 실습 연결

이 장을 읽은 뒤에는 [첫 워크로드 실습](../exercises/01-first-workload.md)에서 Deployment가 Pod를 만들고 Service가 label로 Pod를 찾는 흐름을 확인합니다. `kubectl get pods --show-labels -n k8s-study`와 `kubectl describe svc web -n k8s-study`를 나란히 보면 연결 구조가 보입니다.

## 체크리스트

- [ ] Pod와 컨테이너의 차이를 설명할 수 있다.
- [ ] Deployment가 ReplicaSet과 Pod를 만드는 흐름을 설명할 수 있다.
- [ ] Service가 label selector로 Pod를 찾는다는 점을 이해했다.
- [ ] `spec`과 `status`를 구분할 수 있다.
