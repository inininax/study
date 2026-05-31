# 08. 관측과 장애 대응

## 기본 원칙

장애 대응은 명령어를 많이 아는 것보다 원인을 좁히는 순서가 중요합니다.

권장 순서:

1. 리소스가 존재하는가?
2. 원하는 namespace를 보고 있는가?
3. 상태와 이벤트는 무엇을 말하는가?
4. 컨트롤러가 원하는 개수를 만들었는가?
5. Pod가 스케줄되었는가?
6. 이미지 pull과 컨테이너 시작이 성공했는가?
7. probe가 실패하고 있지 않은가?
8. Service selector와 endpoint가 맞는가?
9. DNS와 네트워크 정책 문제가 아닌가?
10. 애플리케이션 로그는 무엇을 말하는가?

초심자에게 가장 중요한 습관은 "증상 이름만 보고 결론 내리지 않기"입니다. 같은 `CrashLoopBackOff`라도 설정 누락, 잘못된 명령, 너무 공격적인 livenessProbe처럼 원인이 다를 수 있습니다.

## 필수 명령

```bash
kubectl get all -n k8s-study
kubectl get events -n k8s-study --sort-by='.lastTimestamp'
kubectl describe pod <pod-name> -n k8s-study
kubectl logs <pod-name> -n k8s-study
kubectl logs <pod-name> -c <container-name> -n k8s-study
kubectl logs <pod-name> --previous -n k8s-study
```

## 증상별 첫 명령

| 증상 | 먼저 볼 것 |
| --- | --- |
| 리소스가 안 보임 | `kubectl get all -n k8s-study` |
| Pod가 `Pending` | `kubectl describe pod <pod-name> -n k8s-study` |
| 이미지 오류 | `kubectl describe pod <pod-name> -n k8s-study` |
| 재시작 반복 | `kubectl logs <pod-name> --previous -n k8s-study` |
| Service 접근 실패 | `kubectl get endpoints <svc-name> -n k8s-study` |
| 최근 실패 이유 확인 | `kubectl get events -n k8s-study --sort-by='.lastTimestamp'` |

## 흔한 상태

### Pending

가능한 원인:

- 리소스 부족
- nodeSelector/affinity 조건 불일치
- taint를 견디는 toleration 없음
- PVC 바인딩 실패

확인:

```bash
kubectl describe pod <pod-name> -n k8s-study
```

### ImagePullBackOff

가능한 원인:

- 이미지 이름 또는 태그 오타
- private registry 인증 실패
- 레지스트리 네트워크 문제

확인:

```bash
kubectl describe pod <pod-name> -n k8s-study
```

### CrashLoopBackOff

가능한 원인:

- 애플리케이션 즉시 종료
- 필수 환경 변수 누락
- 설정 파일 오류
- livenessProbe가 너무 공격적임

확인:

```bash
kubectl logs <pod-name> --previous -n k8s-study
kubectl describe pod <pod-name> -n k8s-study
```

### Ready가 되지 않음

가능한 원인:

- readinessProbe 실패
- 애플리케이션 포트 불일치
- 의존 서비스 연결 실패

## 디버깅 Pod

간단한 네트워크 확인:

```bash
kubectl run netshoot -n k8s-study --rm -it \
  --image=nicolaka/netshoot -- bash
```

가벼운 HTTP 확인:

```bash
kubectl run curl -n k8s-study --rm -it \
  --image=curlimages/curl:8.10.1 -- sh
```

## 메트릭과 로그

로컬 학습에서는 다음부터 시작합니다.

- metrics-server: `kubectl top`과 HPA에 필요
- 애플리케이션 stdout/stderr 로그
- 이벤트 기반 상태 확인

운영 환경에서는 다음을 검토합니다.

- Prometheus와 Alertmanager
- Grafana 대시보드
- Loki, Elasticsearch/OpenSearch 같은 로그 저장소
- OpenTelemetry 기반 tracing
- SLO와 알림 기준

## 장애 대응 기록

장애를 해결한 뒤 다음을 남기면 실력이 빠르게 늘어납니다.

- 증상
- 영향 범위
- 최초 감지 시각
- 사용한 명령과 관측 결과
- 원인
- 임시 조치
- 영구 조치
- 재발 방지 체크

학습 중에는 짧게 써도 됩니다. 예를 들어 "Service endpoint가 비어 있었고 selector `app` 값이 Pod label과 달랐다" 정도만 남겨도 다음 장애에서 큰 힌트가 됩니다.

## 체크리스트

- [ ] Pending, ImagePullBackOff, CrashLoopBackOff의 확인 순서를 알고 있다.
- [ ] 이벤트와 로그를 함께 확인할 수 있다.
- [ ] Service endpoint 문제를 진단할 수 있다.
- [ ] 장애 대응 기록을 남길 수 있다.
