# 실습 07. 배치 작업과 Kustomize

## 목표

- Job과 CronJob을 생성하고 완료 상태를 확인합니다.
- Kustomize base/overlay 구조를 렌더링하고 적용합니다.
- 환경별 replica와 ConfigMap 차이를 확인합니다.

먼저 [Workload 문서](../docs/03-workloads.md)의 Job/CronJob과 [생태계 문서](../docs/10-ecosystem-and-capstone.md)의 Kustomize 설명을 읽습니다.

## Job

```bash
kubectl apply -f examples/00-namespace/namespace.yaml
kubectl apply -f examples/07-jobs/job.yaml
kubectl wait --for=condition=complete job/pi-sample -n k8s-study --timeout=120s
kubectl logs job/pi-sample -n k8s-study
```

정상 신호:

- Job `pi-sample`의 `COMPLETIONS`가 `3/3`이 됩니다.
- 로그에 원주율 숫자가 출력됩니다.

Job Pod를 확인합니다.

```bash
kubectl get pods -n k8s-study -l job-name=pi-sample
```

## CronJob

```bash
kubectl apply -f examples/07-jobs/cronjob.yaml
kubectl get cronjob,job -n k8s-study
```

수동으로 한 번 실행해볼 수 있습니다.

```bash
kubectl create job manual-hello \
  --from=cronjob/hello-every-five-minutes \
  -n k8s-study
kubectl logs job/manual-hello -n k8s-study
```

CronJob은 즉시 실행되지 않을 수 있으므로 학습 중에는 `kubectl create job --from=cronjob/...`로 수동 실행해 결과를 빠르게 확인합니다.

## Kustomize 렌더링

적용 전에 렌더링 결과를 봅니다.

```bash
kubectl kustomize examples/08-kustomize/overlays/dev
kubectl kustomize examples/08-kustomize/overlays/prod
```

렌더링 결과에서 `dev-`와 `prod-` name prefix, replica 수, ConfigMap 값 차이를 찾습니다.

dev overlay 적용:

```bash
kubectl apply -k examples/08-kustomize/overlays/dev
kubectl get deploy,svc,configmap -n k8s-kustomize
```

prod overlay 적용:

```bash
kubectl apply -k examples/08-kustomize/overlays/prod
kubectl get deploy,svc,configmap -n k8s-kustomize
```

두 overlay는 같은 base를 사용하지만 이름 prefix, replica 수, ConfigMap 값이 다릅니다.

적용 후에는 `kubectl get deploy -n k8s-kustomize`로 dev/prod 리소스가 같은 namespace 안에서 서로 다른 이름으로 만들어졌는지 확인합니다.

## 정리

```bash
kubectl delete job manual-hello -n k8s-study --ignore-not-found
kubectl delete -f examples/07-jobs/
kubectl delete -k examples/08-kustomize/overlays/dev
kubectl delete -k examples/08-kustomize/overlays/prod
kubectl delete namespace k8s-kustomize --ignore-not-found
```
