# 실습 04. 스케줄링과 스케일링

## 목표

- requests, limits, probe가 있는 Deployment를 배포합니다.
- HPA와 PDB의 전제를 이해합니다.
- 스케줄링 관련 상태를 관찰합니다.

먼저 [스케줄링과 스케일링 문서](../docs/06-scheduling-and-scaling.md)의 requests, limits, HPA, PDB 차이를 읽습니다.

## 적용

```bash
kubectl apply -f examples/00-namespace/namespace.yaml
kubectl apply -f examples/05-scheduling-scaling/deployment-resources-probes.yaml
kubectl rollout status deploy/healthy-web -n k8s-study
kubectl describe pod -l app=healthy-web -n k8s-study
```

정상 신호:

- Deployment `healthy-web`의 rollout이 성공합니다.
- Pod 이벤트에 스케줄링, 이미지 pull, 컨테이너 시작 기록이 보입니다.
- `Readiness`와 `Liveness` probe 설정을 `describe`에서 확인할 수 있습니다.

## HPA

HPA는 metrics-server가 필요합니다.

```bash
kubectl apply -f examples/05-scheduling-scaling/hpa.yaml
kubectl get hpa -n k8s-study
```

metrics-server가 없으면 메트릭을 가져오지 못하는 상태가 보일 수 있습니다. 이 경우 HPA 리소스 자체는 생성되지만 스케일링은 동작하지 않습니다.

`TARGETS`가 `<unknown>/70%`처럼 보이면 먼저 metrics-server 유무를 의심합니다. 이것은 예제 YAML 오류라기보다 클러스터 애드온 전제의 문제입니다.

## PDB

```bash
kubectl apply -f examples/05-scheduling-scaling/pdb.yaml
kubectl get pdb -n k8s-study
```

PDB는 자발적 중단에서 최소 가용성을 보호합니다.

PDB는 Pod가 절대 죽지 않게 만드는 기능이 아닙니다. 노드 장애 같은 비자발적 장애는 막지 못하고, drain이나 업그레이드 같은 자발적 중단에서 기준을 제공합니다.

## 정리

```bash
kubectl delete -f examples/05-scheduling-scaling/
```
