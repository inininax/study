# 실습 05. 보안과 관측

## 목표

- ServiceAccount, Role, RoleBinding을 생성합니다.
- 권한을 `kubectl auth can-i`로 검증합니다.
- 일부러 깨진 매니페스트를 배포하고 원인을 찾습니다.

먼저 [보안과 RBAC](../docs/07-security-rbac.md), [관측과 장애 대응](../docs/08-observability-troubleshooting.md)을 읽고 진행합니다.

## RBAC

```bash
kubectl apply -f examples/00-namespace/namespace.yaml
kubectl apply -f examples/06-security-rbac/serviceaccount-role-rolebinding.yaml
kubectl auth can-i get pods \
  --as=system:serviceaccount:k8s-study:pod-reader \
  -n k8s-study
kubectl auth can-i delete pods \
  --as=system:serviceaccount:k8s-study:pod-reader \
  -n k8s-study
```

첫 번째는 `yes`, 두 번째는 `no`가 나와야 합니다.

이 결과는 `pod-reader` ServiceAccount가 Pod 조회 권한만 갖고 삭제 권한은 갖지 않는다는 뜻입니다.

## 보안 컨텍스트

```bash
kubectl apply -f examples/06-security-rbac/restricted-pod.yaml
kubectl get pod restricted-nginx -n k8s-study
kubectl describe pod restricted-nginx -n k8s-study
```

정상 신호는 Pod가 과도한 권한 없이 실행되는 것입니다. `describe`에서 `runAsNonRoot`, capability drop, 권한 상승 차단 같은 설정을 YAML과 비교합니다.

## 장애 예제

```bash
kubectl apply -f examples/09-troubleshooting/
kubectl get pods,svc -n k8s-study
kubectl get events -n k8s-study --sort-by='.lastTimestamp'
```

확인할 문제:

- `broken-image`: 존재하지 않는 이미지 태그
- `crashloop`: 즉시 실패하는 명령
- `wrong-selector-service`: Service selector 불일치

추천 확인 순서:

```bash
kubectl describe pod -l app=broken-image -n k8s-study
kubectl logs deploy/crashloop --previous -n k8s-study
kubectl get endpoints wrong-selector -n k8s-study
kubectl get pods -n k8s-study --show-labels
```

## 정리

```bash
kubectl delete -f examples/09-troubleshooting/
kubectl delete -f examples/06-security-rbac/
```
