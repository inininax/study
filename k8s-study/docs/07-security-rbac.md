# 07. 보안과 RBAC

## 보안 기본 관점

Kubernetes 보안은 한 번의 설정으로 끝나지 않습니다. 다음 계층을 함께 봐야 합니다.

- 클러스터 API 접근
- 인증과 인가
- Namespace 격리
- ServiceAccount와 RBAC
- Pod Security Standards
- 이미지 공급망
- Secret 관리
- NetworkPolicy
- Admission Control
- 감사 로그

## ServiceAccount

Pod는 ServiceAccount를 통해 Kubernetes API에 접근합니다. 지정하지 않으면 namespace의 `default` ServiceAccount를 사용합니다.

운영에서는 워크로드마다 전용 ServiceAccount를 만들고 필요한 권한만 부여합니다.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: pod-reader
  namespace: k8s-study
```

## RBAC

RBAC은 Role/ClusterRole과 RoleBinding/ClusterRoleBinding으로 구성됩니다.

- Role: namespace 범위 권한
- ClusterRole: 클러스터 범위 권한 또는 여러 namespace에 재사용 가능한 권한
- RoleBinding: 사용자, 그룹, ServiceAccount에 Role을 연결
- ClusterRoleBinding: 클러스터 범위로 연결

RBAC은 다음 문장으로 읽습니다.

```text
누가(subject) 어떤 범위에서(namespace/cluster) 어떤 리소스(resource)에 어떤 행동(verb)을 할 수 있는가?
```

최소 권한 원칙:

- 필요한 리소스만 지정합니다.
- 필요한 verb만 허용합니다.
- 가능하면 namespace 범위 Role을 사용합니다.
- `*` 사용을 피합니다.

권한 확인:

```bash
kubectl auth can-i get pods --as=system:serviceaccount:k8s-study:pod-reader -n k8s-study
```

## Pod Security Standards

Pod Security Standards는 Pod가 과도한 권한으로 실행되는 것을 막기 위한 기준입니다.

운영에서 우선 검토할 설정:

- `runAsNonRoot: true`
- `allowPrivilegeEscalation: false`
- `readOnlyRootFilesystem: true`
- Linux capabilities drop
- host namespace 사용 금지
- privileged 컨테이너 금지

초심자는 먼저 "root로 실행하지 않기", "권한 상승 막기", "필요 없는 Linux capability 제거하기" 세 가지를 확인합니다.

## NetworkPolicy

NetworkPolicy는 네트워크 최소 권한입니다. namespace 내부의 모든 트래픽을 허용하는 기본 상태에서 필요한 통신만 허용하는 구조로 바꿀 수 있습니다.

단, CNI가 NetworkPolicy를 지원해야 실제로 적용됩니다.

## 이미지 보안

운영 체크:

- 신뢰할 수 있는 레지스트리 사용
- 이미지 태그 고정 또는 digest 사용
- 취약점 스캔
- 불필요한 패키지 제거
- non-root 사용자
- SBOM과 서명 정책 검토

## Secret 보안

Secret은 base64 인코딩일 뿐입니다. 다음을 함께 구성해야 합니다.

- etcd 암호화
- RBAC 최소 권한
- Git에 Secret 평문 저장 금지
- 외부 Secret Manager 또는 Sealed Secrets 같은 도구 검토
- 주기적 회전

## 체크리스트

- [ ] ServiceAccount와 RBAC의 연결 구조를 설명할 수 있다.
- [ ] `kubectl auth can-i`로 권한을 검증할 수 있다.
- [ ] Pod Security Standards의 핵심 제한을 이해했다.
- [ ] NetworkPolicy와 RBAC의 보호 범위가 다르다는 점을 안다.
