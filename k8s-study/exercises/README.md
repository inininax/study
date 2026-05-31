# 실습 안내

모든 실습은 저장소 루트에서 실행한다고 가정합니다.

실습의 목표는 명령을 그대로 따라 치는 것이 아니라 "내가 선언한 YAML이 클러스터에서 어떤 상태로 바뀌는지"를 관찰하는 것입니다.

## 준비

```bash
kubectl version --client
kubectl cluster-info
kubectl apply -f examples/00-namespace/namespace.yaml
kubectl config set-context --current --namespace=k8s-study
```

현재 context를 바꾸기 싫다면 모든 명령에 `-n k8s-study`를 붙이면 됩니다.

정상 신호:

- `kubectl cluster-info`가 API Server 정보를 출력합니다.
- `kubectl get namespace k8s-study`가 `Active` 상태를 보여줍니다.
- `kubectl config current-context`가 의도한 로컬 클러스터를 가리킵니다.

## 권장 순서

1. [첫 워크로드](01-first-workload.md)
2. [네트워킹](02-networking.md)
3. [설정과 스토리지](03-config-storage.md)
4. [스케줄링과 스케일링](04-scheduling-scaling.md)
5. [보안과 관측](05-security-observability.md)
6. [캡스톤](06-capstone.md)
7. [배치 작업과 Kustomize](07-jobs-kustomize.md)

## 공통 확인 명령

```bash
kubectl get all -n k8s-study
kubectl get events -n k8s-study --sort-by='.lastTimestamp'
kubectl describe pod <pod-name> -n k8s-study
kubectl logs <pod-name> -n k8s-study
```

## 진행 방식

각 실습은 다음 순서로 진행합니다.

1. `kubectl diff -f <path>` 또는 `kubectl kustomize <path>`로 적용 전 내용을 봅니다.
2. `kubectl apply`로 리소스를 만듭니다.
3. `kubectl get`으로 리소스가 생겼는지 확인합니다.
4. `kubectl describe`와 `logs`로 상태와 이벤트를 해석합니다.
5. 일부 값을 바꿔 정상 상태와 실패 상태의 차이를 관찰합니다.
6. 적용한 경로 그대로 `kubectl delete`를 실행합니다.

## 자주 막히는 지점

- `NotFound`: namespace나 리소스 이름이 맞는지 확인합니다.
- `Pending`: 리소스 부족, node 조건, PVC 바인딩 실패를 `describe` 이벤트에서 봅니다.
- `ImagePullBackOff`: 이미지 이름과 태그를 확인합니다.
- `CrashLoopBackOff`: `logs --previous`로 직전 컨테이너 출력을 봅니다.
- Service 접근 실패: endpoint가 비어 있는지 먼저 확인합니다.

## 정리

실습 전체를 정리하려면 namespace를 삭제합니다.

```bash
kubectl delete namespace k8s-study
```

개별 예제만 삭제하려면 적용한 경로를 그대로 사용합니다.

```bash
kubectl delete -f examples/01-first-workload/
```
