# 실습 02. 네트워킹

## 목표

- Deployment와 Service를 연결합니다.
- Service selector와 endpoint를 확인합니다.
- Ingress와 NetworkPolicy 예제를 살펴봅니다.

먼저 [네트워킹 문서](../docs/04-networking.md)의 Service selector, endpoint, Ingress Controller 전제를 읽습니다.

## 적용

```bash
kubectl apply -f examples/00-namespace/namespace.yaml
kubectl apply -f examples/03-networking/deployment-service.yaml
kubectl get svc,endpoints,endpointslice -n k8s-study
```

정상 신호:

- Service `echo`가 보입니다.
- `endpoints` 또는 `endpointslice`에 Pod IP와 `8080` 포트가 보입니다.
- endpoint가 비어 있지 않으면 Service selector가 Ready Pod를 찾은 것입니다.

## 클러스터 내부 접근

```bash
kubectl run curl -n k8s-study --rm -it \
  --image=curlimages/curl:8.10.1 -- sh
```

컨테이너 안에서:

```bash
curl http://echo
```

같은 namespace 안에서는 Service 이름 `echo`만으로 접근할 수 있습니다. 다른 namespace에서는 `echo.k8s-study.svc.cluster.local`처럼 전체 DNS 이름을 사용합니다.

## selector 확인

```bash
kubectl get pods -n k8s-study --show-labels
kubectl describe svc echo -n k8s-study
```

Service의 selector가 Pod label과 일치해야 endpoint가 생깁니다.

초심자는 여기서 `kubectl get pods --show-labels`의 `app=echo`와 `kubectl describe svc echo`의 `Selector: app=echo`가 같은지 비교합니다.

## Ingress

Ingress Controller가 있는 클러스터에서만 실제 외부 접근이 됩니다.

```bash
kubectl apply -f examples/03-networking/ingress.yaml
kubectl describe ingress echo -n k8s-study
```

## NetworkPolicy

NetworkPolicy는 지원 CNI가 있어야 적용됩니다.

```bash
kubectl apply -f examples/03-networking/network-policy.yaml
kubectl get networkpolicy -n k8s-study
```

정책 리소스가 생성되는 것과 실제 트래픽 차단이 동작하는 것은 다릅니다. 로컬 클러스터의 CNI가 NetworkPolicy를 지원하는지 확인해야 합니다.

## 정리

```bash
kubectl delete -f examples/03-networking/
```
