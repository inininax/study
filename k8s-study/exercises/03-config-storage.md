# 실습 03. 설정과 스토리지

## 목표

- ConfigMap과 Secret을 Pod에 주입합니다.
- PVC를 사용하는 워크로드를 배포합니다.
- 설정과 데이터가 애플리케이션 이미지 밖에 있다는 점을 확인합니다.

먼저 [설정과 스토리지 문서](../docs/05-configuration-and-storage.md)의 ConfigMap, Secret, PVC 차이를 읽습니다.

## ConfigMap과 Secret

```bash
kubectl apply -f examples/00-namespace/namespace.yaml
kubectl apply -f examples/02-config-secret/
kubectl rollout status deploy/config-demo -n k8s-study
kubectl logs deploy/config-demo -n k8s-study
```

정상 신호:

- 로그에 `mode=study`, `feature=true`, `log=info`, `user=study_user`가 보입니다.
- `mounted config:` 아래에 `greeting=hello-kubernetes`가 보입니다.

환경 변수를 확인합니다.

```bash
kubectl exec deploy/config-demo -n k8s-study -- env | sort
```

## 스토리지

기본 StorageClass가 있는 클러스터에서 실행합니다.

```bash
kubectl get storageclass
kubectl apply -f examples/04-storage/
kubectl get pvc,pod -n k8s-study
kubectl exec deploy/storage-demo -n k8s-study -- sh -c 'date >> /data/visits.txt && cat /data/visits.txt'
```

정상 신호:

- PVC `storage-demo-data`가 `Bound` 상태입니다.
- Pod가 재시작되어도 `/data/visits.txt` 내용이 남아 있습니다.

PVC가 `Pending`이면 `kubectl describe pvc storage-demo-data -n k8s-study`로 이벤트를 확인합니다.

Pod를 재시작해도 PVC 데이터가 유지되는지 확인합니다.

```bash
kubectl rollout restart deploy/storage-demo -n k8s-study
kubectl rollout status deploy/storage-demo -n k8s-study
kubectl exec deploy/storage-demo -n k8s-study -- cat /data/visits.txt
```

## 정리

```bash
kubectl delete -f examples/02-config-secret/
kubectl delete -f examples/04-storage/
```
