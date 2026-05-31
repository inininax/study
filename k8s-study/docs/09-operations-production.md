# 09. 운영과 프로덕션 고려사항

## 운영 준비의 핵심

Kubernetes 운영은 YAML을 작성하는 일보다 시스템의 변경과 장애를 예측하는 일에 가깝습니다.

운영 체크 영역:

- 클러스터 버전과 업그레이드 정책
- 노드풀과 용량 계획
- 리소스 요청/제한 기본값
- 배포 전략과 롤백
- Secret과 인증서 관리
- 백업과 복구
- 관측과 알림
- 정책과 보안 기준
- 비용과 스케일링

초심자는 이 장을 "지금 당장 모두 구축할 목록"으로 읽기보다 "운영에서 추가로 확인해야 할 질문 목록"으로 읽는 것이 좋습니다.

| 학습 단계 | 우선 질문 |
| --- | --- |
| 로컬 실습 | 리소스가 Ready이고 삭제/복구가 되는가? |
| 팀 개발 환경 | 누가 배포하고, 변경이 어디에 기록되는가? |
| 운영 환경 | 장애, 업그레이드, 보안 사고 때 되돌릴 수 있는가? |

## 버전과 업그레이드

Kubernetes는 빠르게 발전합니다. 클러스터, 노드, kubectl, 애드온, CRD, 컨트롤러의 호환성을 함께 확인해야 합니다.

업그레이드 전 체크:

- 현재 클러스터 버전과 지원 종료 일정
- API deprecation과 removal
- CNI, CSI, Ingress Controller 호환성
- kubelet, kube-proxy, kubectl version skew
- 백업과 롤백 전략
- staging 클러스터 검증

## 배포 전략

기본 RollingUpdate 외에도 상황에 따라 전략을 선택합니다.

- RollingUpdate: 대부분의 stateless 서비스 기본값
- Blue/Green: 빠른 전환과 명확한 롤백이 필요할 때
- Canary: 일부 트래픽으로 점진 검증
- Recreate: 동시에 여러 버전 실행이 불가능할 때

Kubernetes 자체 Deployment는 트래픽 비율 기반 canary를 직접 제공하지 않습니다. Ingress Controller, service mesh, progressive delivery 도구를 함께 사용합니다.

## 리소스 정책

운영 namespace에는 다음을 검토합니다.

- ResourceQuota
- LimitRange
- PriorityClass
- PDB
- 기본 requests/limits

리소스 정책이 없으면 특정 워크로드가 클러스터 전체 안정성을 해칠 수 있습니다.

로컬 실습에서는 ResourceQuota와 LimitRange를 바로 적용하지 않아도 됩니다. 대신 모든 장기 실행 예제에 requests/limits가 있는지 먼저 확인합니다.

## 백업과 복구

백업 대상:

- etcd
- PV 데이터
- Git에 저장된 매니페스트
- Secret 원본 또는 외부 Secret Manager
- CRD와 Custom Resource

복구 훈련 없이 백업만 있는 것은 충분하지 않습니다. 정기적으로 복구 시간을 측정해야 합니다.

## 정책과 Admission

운영에서는 잘못된 리소스가 API Server에 저장되기 전에 막는 것이 중요합니다.

사용 가능한 접근:

- Pod Security Admission
- ValidatingAdmissionPolicy
- OPA Gatekeeper
- Kyverno
- 이미지 서명 검증 정책

## 멀티 테넌시

Namespace만으로 강한 격리가 완성되지는 않습니다. 다음을 함께 봐야 합니다.

- RBAC
- NetworkPolicy
- ResourceQuota
- Pod Security
- 노드 격리
- Secret 접근 범위
- 감사 로그

## 운영 런북 예시

런북은 장애가 난 뒤 생각을 시작하지 않기 위한 문서입니다. 명령 목록뿐 아니라 "이 명령 결과가 어떤 상태면 다음으로 무엇을 할지"까지 적어두면 좋습니다.

### 배포 실패

```bash
kubectl rollout status deploy/<name> -n <namespace>
kubectl describe deploy/<name> -n <namespace>
kubectl get rs,pod -n <namespace> -l app=<app>
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
kubectl rollout undo deploy/<name> -n <namespace>
```

### 노드 드레인

```bash
kubectl cordon <node>
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data
kubectl uncordon <node>
```

PDB가 있으면 drain이 지연될 수 있습니다. 이 지연은 가용성을 보호하기 위한 신호일 수 있습니다.

## 체크리스트

- [ ] 업그레이드 전에 API deprecation과 애드온 호환성을 확인한다.
- [ ] 모든 운영 워크로드에 requests, limits, readinessProbe가 있다.
- [ ] 백업뿐 아니라 복구 훈련 계획이 있다.
- [ ] 정책으로 위험한 Pod 설정을 사전에 차단한다.
