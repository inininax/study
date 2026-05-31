# 10. 생태계와 캡스톤 준비

## Kustomize

Kustomize는 Kubernetes YAML을 템플릿 언어 없이 조합하고 패치하는 도구입니다. `kubectl`에 내장되어 있어 바로 사용할 수 있습니다.

적합한 사용:

- dev/staging/prod 환경 차이 관리
- 공통 base와 환경별 overlay 분리
- ConfigMap/Secret generator
- 이미지 태그 변경

```bash
kubectl kustomize examples/08-kustomize/overlays/dev
kubectl apply -k examples/08-kustomize/overlays/dev
```

초심자는 Kustomize를 "공통 YAML은 base에 두고, 환경 차이는 overlay에서 바꾸는 도구"로 이해하면 됩니다. 적용 전에 `kubectl kustomize`로 최종 YAML을 눈으로 확인하는 습관이 중요합니다.

## Helm

Helm은 Kubernetes 패키지 매니저입니다.

적합한 사용:

- 복잡한 애플리케이션 패키징
- 외부 오픈소스 설치
- values 파일 기반 환경 설정
- 릴리스 단위 관리

주의점:

- 템플릿이 복잡해지면 렌더링 결과를 항상 확인해야 합니다.
- CRD 설치와 업그레이드는 chart마다 정책이 다릅니다.
- values 파일에 Secret을 평문으로 두지 않습니다.

## 도구 선택 기준

| 상황 | 먼저 고려할 도구 |
| --- | --- |
| 이 저장소처럼 작은 예제와 환경 차이 관리 | Kustomize |
| 외부 오픈소스 애플리케이션 설치 | Helm |
| Git 변경을 기준으로 클러스터를 계속 동기화 | GitOps |
| Kubernetes API 자체를 확장 | CRD와 Operator |

## GitOps

GitOps는 Git 저장소의 선언 상태를 클러스터에 지속적으로 동기화하는 운영 방식입니다.

대표 도구:

- Argo CD
- Flux

핵심 원칙:

- 클러스터 변경은 Git 변경으로 추적한다.
- 사람이 직접 `kubectl edit`한 변경은 drift로 본다.
- 자동 동기화 범위와 승인 절차를 분리한다.

## CRD와 Operator

CRD는 Kubernetes API를 확장해 새로운 리소스 타입을 정의합니다. Operator는 특정 도메인 운영 지식을 컨트롤러로 구현한 것입니다.

예:

- cert-manager의 Certificate
- Prometheus Operator의 ServiceMonitor
- External Secrets Operator의 ExternalSecret

숙련자는 CRD를 사용할 때 다음을 확인합니다.

- CRD 버전과 변환 전략
- 컨트롤러 장애 시 영향
- 백업 대상에 Custom Resource 포함 여부
- 업그레이드 절차

## 캡스톤 목표

캡스톤에서는 다음 리소스를 한 namespace에 구성합니다.

- Namespace
- ConfigMap
- Secret
- Deployment
- Service
- Ingress
- HPA
- PDB
- NetworkPolicy
- ServiceAccount, Role, RoleBinding

진행 순서:

1. Namespace와 설정 리소스를 먼저 확인합니다.
2. Deployment rollout과 Pod Ready 상태를 확인합니다.
3. Service endpoint와 port-forward 접근을 확인합니다.
4. RBAC 권한이 허용/거부되는 범위를 확인합니다.
5. 일부러 selector, image, probe를 깨뜨린 뒤 원인을 설명합니다.

완료 기준:

- 애플리케이션 Pod가 Ready 상태입니다.
- Service endpoint가 생성됩니다.
- rollout status가 성공합니다.
- RBAC 권한이 최소 범위로 확인됩니다.
- 의도적으로 잘못된 selector나 이미지 태그를 넣었을 때 원인을 찾을 수 있습니다.

## 다음 학습 주제

- CKA/CKAD/CKS 시험 범위와 실전 문제
- Prometheus 기반 SLO 운영
- Service Mesh와 Gateway API
- Multi-cluster 운영
- Kubernetes API와 controller-runtime
- 비용 최적화와 capacity planning
