# 실습 01. 첫 워크로드

## 목표

- Namespace, Pod, Deployment, Service를 생성합니다.
- Deployment rollout 상태를 확인합니다.
- Service를 통해 Pod에 접근합니다.

먼저 [Kubernetes 핵심 개념](../docs/01-core-concepts.md)의 Deployment, Pod, Service 관계를 읽고 오면 좋습니다.

## 적용

```bash
kubectl apply -f examples/00-namespace/namespace.yaml
kubectl apply -f examples/01-first-workload/
kubectl rollout status deploy/web -n k8s-study
kubectl get pod,deploy,svc -n k8s-study -o wide
```

정상 신호:

- Deployment `web`의 `READY`가 `2/2`에 가까워집니다.
- Pod 2개가 `Running`이고 `READY`가 `1/1`입니다.
- Service `web`이 `ClusterIP`를 가집니다.

## 접근

포트 포워딩:

```bash
kubectl port-forward svc/web 8080:80 -n k8s-study
```

다른 터미널에서:

```bash
curl http://localhost:8080
```

Nginx 기본 페이지 HTML이 보이면 Service를 통해 Pod까지 연결된 것입니다. 포트 포워딩 터미널은 실습이 끝날 때 `Ctrl+C`로 종료합니다.

## 관찰

Pod 하나를 삭제해봅니다.

```bash
kubectl delete pod -l app=web -n k8s-study
kubectl get pods -n k8s-study -w
```

Deployment가 원하는 replica 수를 유지하기 위해 새 Pod를 만듭니다.

여기서 핵심은 Pod를 직접 살리는 것이 아니라 Deployment 컨트롤러가 `replicas: 2`라는 원하는 상태를 맞춘다는 점입니다.

## 변경

replica 수를 바꿔봅니다.

```bash
kubectl scale deploy/web --replicas=3 -n k8s-study
kubectl get pods -n k8s-study
```

YAML과 실제 상태가 달라졌으므로 다시 선언형 상태로 맞춥니다.

```bash
kubectl apply -f examples/01-first-workload/deployment.yaml
```

다시 적용하면 YAML에 적힌 `replicas: 2`로 돌아갑니다. 명령형 변경과 선언형 YAML이 다를 때 어떤 상태를 기준으로 삼을지 확인하는 연습입니다.

## 정리

```bash
kubectl delete -f examples/01-first-workload/
```
