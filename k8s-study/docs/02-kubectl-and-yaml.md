# 02. kubectl과 YAML

## 목표

Kubernetes를 안정적으로 다루려면 `kubectl` 명령을 많이 외우는 것보다 리소스를 조회하고, 차이를 확인하고, 선언형으로 적용하는 흐름을 익혀야 합니다.

초심자용 기본 루틴은 다음 한 줄입니다.

```text
get으로 목록 확인 -> describe로 이벤트 확인 -> logs로 앱 출력 확인 -> diff/apply로 선언 상태 반영
```

## 기본 조회

```bash
kubectl get nodes
kubectl get pods -A
kubectl get deployment,service -n k8s-study
kubectl get pod -o wide -n k8s-study
```

처음에는 `-A`로 전체를 보기보다 실습 namespace를 명시하는 습관을 들입니다. 리소스가 없다고 보일 때 실제로는 다른 namespace를 보고 있는 경우가 많습니다.

자세한 상태는 `describe`로 확인합니다.

```bash
kubectl describe pod <pod-name> -n k8s-study
```

로그는 다음 순서로 확인합니다.

```bash
kubectl logs <pod-name> -n k8s-study
kubectl logs deploy/web -n k8s-study
kubectl logs deploy/web --previous -n k8s-study
```

## 선언형 적용 흐름

운영에서는 다음 흐름을 습관화합니다.

```bash
kubectl diff -f examples/01-first-workload/
kubectl apply -f examples/01-first-workload/
kubectl rollout status deploy/web -n k8s-study
kubectl get all -n k8s-study
```

삭제도 같은 파일 기준으로 합니다.

```bash
kubectl delete -f examples/01-first-workload/
```

## YAML 읽는 법

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  labels:
    app: web
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
```

중요한 포인트:

- Deployment의 `spec.selector.matchLabels`와 Pod template의 `metadata.labels`가 맞아야 합니다.
- Deployment 이름과 컨테이너 이름은 같을 필요가 없습니다.
- `replicas`는 Pod 개수를 직접 만드는 것이 아니라 컨트롤러의 원하는 상태입니다.

읽는 순서:

1. `apiVersion`과 `kind`로 API 종류를 확인합니다.
2. `metadata.name`과 `namespace`로 리소스 위치를 확인합니다.
3. `selector.matchLabels`와 `template.metadata.labels`가 같은지 봅니다.
4. `containers[].image`, `ports`, `resources`, `probes`를 확인합니다.

## dry-run과 explain

리소스를 만들기 전 구조를 확인할 수 있습니다.

```bash
kubectl create deployment web --image=nginx:1.27 \
  --dry-run=client -o yaml
```

필드 설명은 `explain`으로 확인합니다.

```bash
kubectl explain deployment.spec.strategy
kubectl explain pod.spec.containers.resources
```

## JSONPath와 커스텀 출력

운영 중에는 원하는 필드만 빠르게 확인해야 합니다.

```bash
kubectl get pods -n k8s-study \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'
```

```bash
kubectl get pods -n k8s-study \
  -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName,PHASE:.status.phase
```

## 자주 쓰는 명령

```bash
kubectl config get-contexts
kubectl config current-context
kubectl config set-context --current --namespace=k8s-study
kubectl api-resources
kubectl get events -n k8s-study --sort-by='.lastTimestamp'
kubectl rollout history deploy/web -n k8s-study
kubectl rollout undo deploy/web -n k8s-study
```

## 실수하기 쉬운 부분

- `kubectl create`로 만든 리소스를 나중에 YAML로 관리하지 않으면 재현성이 낮아집니다.
- `kubectl edit`은 긴급 수정에는 유용하지만 Git에 남지 않으면 운영 추적이 어렵습니다.
- Secret을 YAML에 평문으로 커밋하면 안 됩니다. 학습용 Secret과 운영 Secret 관리는 구분해야 합니다.
- `kubectl delete pod`는 임시 조치입니다. Deployment가 관리하는 Pod라면 다시 생성됩니다.
- `kubectl apply`가 성공해도 애플리케이션이 준비된 것은 아닙니다. Deployment는 `rollout status`, Pod는 `Ready` 상태를 따로 확인합니다.

## 체크리스트

- [ ] `kubectl diff` 후 `apply`하는 습관을 들였다.
- [ ] `kubectl explain`으로 낯선 필드를 확인할 수 있다.
- [ ] rollout 상태와 이벤트를 확인할 수 있다.
- [ ] namespace를 명시하거나 context 기본 namespace를 설정할 수 있다.
