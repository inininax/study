# 05. 설정과 스토리지

## 설정 외부화

컨테이너 이미지는 실행 파일과 기본 설정만 담고, 환경별 값은 Kubernetes 리소스로 주입하는 것이 좋습니다.

사용 도구:

- ConfigMap: 민감하지 않은 설정
- Secret: 비밀번호, 토큰, 인증서 같은 민감 값
- Volume: 파일 형태 설정
- Environment Variable: 간단한 값 주입

선택 기준:

| 필요 | 리소스 또는 방식 |
| --- | --- |
| 민감하지 않은 작은 설정값 | ConfigMap |
| 비밀번호, 토큰, 인증서 | Secret |
| 설정 파일을 그대로 주입 | ConfigMap/Secret volume |
| Pod 재시작 후에도 데이터 유지 | PVC |
| 컨테이너 간 임시 파일 공유 | `emptyDir` |

## ConfigMap

ConfigMap은 key-value 또는 파일 형태 데이터를 저장합니다.

```bash
kubectl create configmap app-config \
  --from-literal=APP_MODE=dev \
  --dry-run=client -o yaml
```

ConfigMap을 환경 변수로 주입할 수 있습니다.

```yaml
envFrom:
  - configMapRef:
      name: app-config
```

파일로 마운트할 수도 있습니다.

```yaml
volumes:
  - name: config
    configMap:
      name: app-config
```

## Secret

Secret은 기본적으로 base64로 인코딩된 값입니다. 암호화와 접근 제어는 별도로 신경 써야 합니다.

학습용으로는 `stringData`가 읽기 쉽습니다.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  PASSWORD: change-me
```

운영에서는 다음을 검토합니다.

- etcd 암호화
- Secret 접근 RBAC 제한
- 외부 Secret Manager 연동
- Secret 값의 Git 커밋 방지
- 주기적 회전

base64는 암호화가 아닙니다. 초심자는 `Secret`이라는 이름 때문에 안전하다고 오해하기 쉽지만, 운영 보안은 RBAC, etcd 암호화, 외부 Secret 관리까지 함께 봐야 합니다.

## Volume, PV, PVC

Kubernetes 스토리지는 다음 계층으로 이해합니다.

- Volume: Pod에 붙는 스토리지 선언
- PersistentVolume: 클러스터가 제공하는 실제 스토리지
- PersistentVolumeClaim: 사용자가 요청하는 스토리지
- StorageClass: 동적 프로비저닝 방식

Pod가 재시작되어도 데이터를 유지하려면 PVC를 사용합니다.

PVC 실습 전에 기본 StorageClass가 있는지 확인합니다.

```bash
kubectl get storageclass
```

기본 StorageClass가 없으면 PVC가 `Pending` 상태로 남을 수 있습니다. 이때는 `kubectl describe pvc <name> -n k8s-study`의 이벤트를 봅니다.

## StatefulSet과 스토리지

StatefulSet은 각 Pod에 안정적인 PVC를 연결할 수 있습니다.

주의점:

- StatefulSet 삭제가 PVC 삭제를 항상 의미하지는 않습니다.
- 데이터 백업과 복구 절차가 먼저 있어야 합니다.
- ReadWriteOnce, ReadWriteMany 같은 접근 모드를 스토리지 제공자가 지원하는지 확인해야 합니다.

## 설정 변경 반영

ConfigMap 또는 Secret을 변경해도 애플리케이션이 자동으로 재시작되지 않을 수 있습니다.

일반적인 전략:

- 애플리케이션이 파일 변경을 감지하도록 구현
- Deployment template annotation을 변경해 rollout 유도
- Kustomize `configMapGenerator` 사용
- Helm checksum annotation 사용

학습 중에는 `kubectl rollout restart deploy/<name> -n k8s-study`로 재시작을 유도하면 변경 반영 과정을 쉽게 관찰할 수 있습니다.

## 체크리스트

- [ ] ConfigMap과 Secret의 용도를 구분할 수 있다.
- [ ] 환경 변수와 볼륨 마운트 방식의 차이를 이해했다.
- [ ] PVC가 필요한 경우와 필요 없는 경우를 구분할 수 있다.
- [ ] 설정 변경 시 Pod 재시작 필요 여부를 판단할 수 있다.
