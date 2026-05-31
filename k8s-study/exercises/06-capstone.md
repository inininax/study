# 실습 06. 캡스톤

## 목표

하나의 namespace에 운영형 기본 구성을 배포합니다.

포함 리소스:

- Namespace
- ConfigMap
- Secret
- Deployment
- Service
- Ingress
- HPA
- PDB
- NetworkPolicy
- ServiceAccount, Role, RoleBinding

시작 전에는 [생태계와 캡스톤 준비](../docs/10-ecosystem-and-capstone.md)의 캡스톤 진행 순서를 읽습니다. 이 실습은 앞 실습의 개념을 한 번에 묶어 확인하는 마무리 과제입니다.

## 적용

```bash
kubectl apply -f examples/10-capstone/
kubectl rollout status deploy/capstone-web -n k8s-capstone
kubectl get all -n k8s-capstone
kubectl get configmap,secret,pdb,hpa,networkpolicy,role,rolebinding,serviceaccount -n k8s-capstone
```

정상 신호:

- Namespace `k8s-capstone`이 생성됩니다.
- Deployment `capstone-web` rollout이 성공합니다.
- Pod 2개가 `Running`이고 Ready 상태입니다.
- Service, HPA, PDB, NetworkPolicy, RBAC 리소스가 같은 namespace에 있습니다.

## 확인

Service endpoint:

```bash
kubectl get endpoints,endpointslice -n k8s-capstone
```

endpoint가 비어 있으면 Service selector와 Pod label, Pod Ready 상태를 먼저 확인합니다.

권한:

```bash
kubectl auth can-i get pods \
  --as=system:serviceaccount:k8s-capstone:capstone-reader \
  -n k8s-capstone
kubectl auth can-i create deployments \
  --as=system:serviceaccount:k8s-capstone:capstone-reader \
  -n k8s-capstone
```

첫 번째 권한 확인은 `yes`, 두 번째는 `no`가 나와야 합니다.

포트 포워딩:

```bash
kubectl port-forward svc/capstone-web 8080:80 -n k8s-capstone
curl http://localhost:8080
```

응답이 오면 Deployment, Service, Pod 포트 연결까지는 정상입니다. Ingress 외부 접근은 별도 Ingress Controller 전제에 따라 달라집니다.

## 도전 과제

1. Deployment replica를 3으로 늘립니다.
2. readinessProbe 포트를 틀리게 바꾸고 증상을 관찰합니다.
3. Service selector를 틀리게 바꾸고 endpoint 변화를 확인합니다.
4. 이미지 태그를 존재하지 않는 값으로 바꾸고 이벤트를 확인합니다.
5. 원래 YAML로 복구합니다.

## 완료 기준

- `capstone-web` Deployment rollout이 성공합니다.
- Service endpoint가 존재합니다.
- HPA는 metrics-server 유무에 따라 메트릭 상태가 다를 수 있지만 리소스가 생성됩니다.
- RBAC 확인에서 조회 권한은 허용되고 배포 생성 권한은 거부됩니다.
- 장애를 만들고 원인을 `describe`, `logs`, `events`로 설명할 수 있습니다.

## 정리

```bash
kubectl delete -f examples/10-capstone/
```
