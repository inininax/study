# 06. 스케줄링과 스케일링

## 리소스 요청과 제한

Kubernetes 스케줄러는 `requests`를 기준으로 노드 배치를 결정합니다. `limits`는 컨테이너가 사용할 수 있는 상한입니다.

```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 256Mi
```

운영에서는 requests 없이 워크로드를 배포하지 않는 것이 좋습니다. requests가 없으면 스케줄링과 용량 계획이 불안정해집니다.

단위 읽기:

- `100m` CPU는 0.1 core입니다.
- `500m` CPU는 0.5 core입니다.
- `128Mi`는 메비바이트 단위 메모리입니다.
- 스케줄러는 `limits`가 아니라 `requests`를 보고 자리를 잡습니다.

## QoS Class

Pod의 리소스 설정에 따라 QoS가 달라집니다.

- Guaranteed: 모든 컨테이너에 CPU/Memory requests와 limits가 같음
- Burstable: 일부 requests/limits가 있음
- BestEffort: requests/limits가 없음

노드 압박 상황에서는 BestEffort가 가장 먼저 축출될 수 있습니다.

## Node 선택

간단한 선택은 `nodeSelector`를 사용합니다.

```yaml
nodeSelector:
  disktype: ssd
```

더 복잡한 조건은 node affinity를 사용합니다.

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
            - key: nodepool
              operator: In
              values:
                - app
```

스케줄링 실패는 대부분 Pod 이벤트에 남습니다.

```bash
kubectl describe pod <pod-name> -n k8s-study
kubectl get events -n k8s-study --sort-by='.lastTimestamp'
```

## Taint와 Toleration

Taint는 노드가 특정 Pod를 거부하도록 만드는 표시입니다. Toleration은 Pod가 그 taint를 견딜 수 있음을 나타냅니다.

적합한 사용:

- 전용 노드풀
- GPU 노드
- 인프라 컴포넌트 전용 노드

## Topology Spread

Topology spread constraints는 Pod를 zone, node 같은 토폴로지에 고르게 분산합니다.

장애 도메인을 고려해야 하는 운영 워크로드에 중요합니다.

## HPA

HorizontalPodAutoscaler는 CPU, 메모리, 커스텀 메트릭을 기준으로 replica 수를 조절합니다.

전제:

- metrics-server 또는 커스텀 메트릭 어댑터가 필요합니다.
- Deployment에 requests가 있어야 CPU 기반 계산이 의미 있습니다.

로컬 클러스터에 metrics-server가 없으면 HPA의 `TARGETS`에 `<unknown>`이 보일 수 있습니다. 이 경우 HPA 리소스 생성은 성공했지만 실제 스케일링 판단에 필요한 메트릭이 부족한 상태입니다.

## VPA와 Cluster Autoscaler

- VPA: Pod의 requests/limits 추천 또는 조정
- Cluster Autoscaler: Pending Pod를 수용하기 위해 노드 수 조정

HPA와 VPA를 같은 리소스에 함께 사용할 때는 정책 충돌을 주의해야 합니다.

## PDB

PodDisruptionBudget은 자발적 중단 중 유지해야 하는 최소 가용성을 선언합니다.

```yaml
spec:
  minAvailable: 1
```

PDB는 노드 장애 같은 비자발적 장애를 막지는 못합니다. 드레인, 업그레이드 같은 자발적 중단에서 가용성을 보호합니다.

## 체크리스트

- [ ] requests와 limits의 차이를 설명할 수 있다.
- [ ] Pending Pod에서 스케줄링 실패 원인을 이벤트로 확인할 수 있다.
- [ ] HPA가 metrics-server와 requests에 의존한다는 점을 이해했다.
- [ ] PDB가 보호하는 중단과 보호하지 못하는 중단을 구분할 수 있다.
