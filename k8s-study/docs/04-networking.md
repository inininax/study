# 04. 네트워킹

## Kubernetes 네트워크 기본 원칙

Kubernetes 네트워킹은 다음 전제를 기반으로 합니다.

- Pod는 고유한 IP를 가집니다.
- 같은 클러스터의 Pod끼리는 NAT 없이 통신할 수 있어야 합니다.
- Service는 바뀌는 Pod IP 앞에 안정적인 가상 IP와 DNS 이름을 제공합니다.

처음에는 다음 흐름으로 그려봅니다.

```text
Client -> Service DNS/ClusterIP -> Service selector -> Ready Pod IP
```

연결이 안 되면 Service 자체보다 selector와 endpoint를 먼저 봅니다.

## Service

Service는 selector로 Pod를 찾아 트래픽을 전달합니다.

주요 타입:

- `ClusterIP`: 클러스터 내부에서만 접근합니다. 기본값입니다.
- `NodePort`: 각 노드의 포트를 통해 접근합니다. 학습과 간단한 테스트에 유용합니다.
- `LoadBalancer`: 클라우드 로드밸런서를 생성합니다. 로컬 클러스터에서는 별도 애드온이 필요할 수 있습니다.
- `ExternalName`: 외부 DNS 이름을 Service처럼 참조합니다.

## Service 포트 구조

```yaml
ports:
  - name: http
    port: 80
    targetPort: 8080
```

- `port`: Service가 노출하는 포트입니다.
- `targetPort`: Pod 컨테이너가 실제로 듣는 포트입니다.
- `nodePort`: NodePort 타입에서 노드에 열리는 포트입니다.

## DNS

Service는 다음 형태의 DNS 이름을 가집니다.

```text
<service>.<namespace>.svc.cluster.local
```

같은 namespace 안에서는 Service 이름만으로 접근할 수 있습니다.

```bash
kubectl run curl -n k8s-study --rm -it --image=curlimages/curl:8.10.1 -- sh
curl http://web
```

## Ingress

Ingress는 HTTP/HTTPS 라우팅 규칙입니다. 실제 동작에는 Ingress Controller가 필요합니다.

예:

- nginx ingress controller
- Traefik
- cloud provider ingress controller

Ingress만 생성하고 controller가 없으면 외부 트래픽은 들어오지 않습니다.

로컬 클러스터에서는 Ingress Controller 설치 방식이 환경마다 다릅니다. Ingress 실습에서 `Address`가 비어 있어도 리소스 생성 자체는 정상일 수 있습니다.

## Gateway API

Gateway API는 Ingress보다 표현력이 좋은 차세대 Kubernetes 네트워킹 API입니다. 운영 환경에서는 Ingress와 Gateway API 중 클러스터 표준을 정하고 사용해야 합니다.

초심자는 Service와 Ingress를 먼저 익힌 뒤 Gateway API로 확장하는 순서가 좋습니다.

## NetworkPolicy

NetworkPolicy는 Pod 간 네트워크 접근을 제어합니다. NetworkPolicy를 적용하려면 CNI 플러그인이 이를 지원해야 합니다.

기본적으로 Kubernetes는 Pod 간 통신을 막지 않습니다. NetworkPolicy를 사용하면 namespace, label, port 기준으로 허용 규칙을 작성할 수 있습니다.

## 문제 해결 순서

Service 연결이 안 될 때는 다음 순서로 봅니다.

1. Pod가 Ready 상태인가?
2. Service selector가 Pod label과 일치하는가?
3. Service endpoint가 생성되었는가?
4. `port`와 `targetPort`가 맞는가?
5. DNS 이름이 맞는가?
6. NetworkPolicy가 차단하고 있지 않은가?
7. Ingress Controller가 설치되어 있고 라우팅 규칙이 맞는가?

명령:

```bash
kubectl get svc,endpoints,endpointslice -n k8s-study
kubectl describe svc web -n k8s-study
kubectl get pods -n k8s-study --show-labels
kubectl describe ingress web -n k8s-study
```

초심자 확인 루틴:

```bash
kubectl get svc echo -n k8s-study
kubectl get endpoints echo -n k8s-study
kubectl get pods -n k8s-study --show-labels
```

endpoint가 비어 있으면 대부분 Service selector와 Pod label이 맞지 않거나 Pod가 Ready가 아닌 상태입니다.

## 체크리스트

- [ ] ClusterIP, NodePort, LoadBalancer, Ingress의 역할을 구분할 수 있다.
- [ ] Service selector와 Pod label 문제를 찾을 수 있다.
- [ ] DNS 이름 규칙을 이해했다.
- [ ] NetworkPolicy가 CNI 지원에 의존한다는 점을 알고 있다.
