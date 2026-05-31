# Kubernetes 학습 자료

이 저장소는 Kubernetes 초심자가 운영 가능한 수준의 숙련자로 성장하기 위한 한국어 학습 자료입니다. 개념 문서, 단계별 실습, 적용 가능한 YAML 예제를 함께 제공합니다.

## 기준

- 작성 기준일: 2026-05-25
- Kubernetes 기준: 공식 릴리스의 최신 안정 브랜치인 v1.36, 최신 패치 v1.36.1 기준
- 실습 환경: `kubectl`, `kind` 또는 `minikube`가 있는 로컬 클러스터
- 공식 참고 자료:
  - Kubernetes Documentation: https://kubernetes.io/docs/
  - Kubernetes Releases: https://kubernetes.io/releases/
  - kubectl Quick Reference: https://kubernetes.io/docs/reference/kubectl/quick-reference/

## 처음 시작하는 방법

Kubernetes가 처음이라면 모든 개념을 한 번에 외우려 하지 말고 "적용한다, 본다, 고친다, 지운다" 흐름을 먼저 몸에 익힙니다.

1. 로컬 클러스터를 만들고 `kubectl cluster-info`가 성공하는지 확인합니다.
2. [로드맵](docs/00-roadmap.md)에서 이번 주에 볼 범위만 고릅니다.
3. 개념 문서를 읽을 때는 `kind`, `metadata.name`, `metadata.namespace`, `spec`, `status`를 먼저 찾습니다.
4. 실습에서는 명령을 실행한 뒤 정상 신호를 확인합니다. 예를 들어 Pod는 `Running`, Deployment는 `Available`, Service는 endpoint가 있어야 합니다.
5. 막히면 바로 삭제하지 말고 `kubectl get events`, `kubectl describe`, `kubectl logs`로 원인을 좁힙니다.

처음 1시간 목표는 "Deployment 하나를 띄우고 Service로 접근한 뒤 삭제한다"입니다. 이 목표는 [첫 워크로드 실습](exercises/01-first-workload.md)에서 바로 확인할 수 있습니다.

## 학습 순서

1. [로드맵](docs/00-roadmap.md)으로 전체 흐름과 목표를 파악합니다.
2. [핵심 개념](docs/01-core-concepts.md)부터 [생태계와 캡스톤 준비](docs/10-ecosystem-and-capstone.md)까지 순서대로 읽습니다.
3. 낯선 용어가 나오면 [용어와 명령어 치트시트](docs/11-glossary-and-cheatsheet.md)에서 다시 확인합니다.
4. 각 장을 읽은 뒤 [실습](exercises/README.md)을 실행합니다.
5. `examples/`의 YAML을 직접 수정하고 `kubectl diff`, `kubectl apply`, `kubectl describe`로 결과를 검증합니다.
6. 마지막으로 [캡스톤](exercises/06-capstone.md)을 수행해 배포, 네트워킹, 설정, 보안, 관측, 장애 대응을 한 번에 연습합니다.
7. 추가로 [배치 작업과 Kustomize](exercises/07-jobs-kustomize.md)를 수행해 운영 도구 사용 범위를 넓힙니다.

## 자료 구성

```text
docs/
  00-roadmap.md
  01-core-concepts.md
  02-kubectl-and-yaml.md
  03-workloads.md
  04-networking.md
  05-configuration-and-storage.md
  06-scheduling-and-scaling.md
  07-security-rbac.md
  08-observability-troubleshooting.md
  09-operations-production.md
  10-ecosystem-and-capstone.md
  11-glossary-and-cheatsheet.md
exercises/
  README.md
  01-first-workload.md
  02-networking.md
  03-config-storage.md
  04-scheduling-scaling.md
  05-security-observability.md
  06-capstone.md
  07-jobs-kustomize.md
examples/
  00-namespace/
  01-first-workload/
  02-config-secret/
  03-networking/
  04-storage/
  05-scheduling-scaling/
  06-security-rbac/
  07-jobs/
  08-kustomize/
  09-troubleshooting/
  10-capstone/
```

## 추천 학습 방식

- 처음에는 모든 리소스를 `kubectl apply -f`로 적용하고, 삭제는 `kubectl delete -f`로 합니다.
- YAML을 적용하기 전에 `kubectl diff -f <path>`로 변경점을 확인합니다.
- 문제가 생기면 먼저 `kubectl get`, `kubectl describe`, `kubectl logs`, `kubectl events` 순서로 확인합니다.
- 명령을 실행할 때마다 "내가 기대한 상태"와 "클러스터가 보여주는 상태"를 한 문장으로 적어봅니다.
- 문서의 체크리스트는 암기 시험이 아니라 다음 실습으로 넘어가도 되는지 확인하는 기준입니다.
- 예제는 학습용입니다. 운영 환경에서는 이미지 태그 고정, 리소스 요청/제한, 보안 컨텍스트, 네트워크 정책, 배포 전략, 백업 전략을 반드시 검토해야 합니다.

## 완료 목표

이 자료를 끝까지 수행하면 다음을 할 수 있어야 합니다.

- Pod, Deployment, Service, Ingress, ConfigMap, Secret, PVC, Job, CronJob을 설명하고 작성한다.
- 선언형 YAML과 `kubectl`을 사용해 변경을 예측하고 적용한다.
- 리소스 요청/제한, probe, HPA, PDB, affinity, taint/toleration을 활용한다.
- RBAC, ServiceAccount, Pod Security, NetworkPolicy의 역할을 이해하고 최소 권한을 구성한다.
- 장애 상황에서 이벤트, 로그, 상태, 셀렉터, DNS, 이미지, probe 문제를 추적한다.
- Kustomize 기반 환경 분리와 캡스톤 배포 구성을 이해한다.
