# Jenkins Examples for Beginners

Jenkins Declarative Pipeline을 처음 배우는 사람을 위한 예제 모음입니다. 각 디렉터리는 하나의 독립적인 `Jenkinsfile` 예제이며, 기초 출력부터 빌드/테스트, 파라미터, 병렬 실행, 후처리, Docker, 실행 정책까지 순서대로 학습할 수 있습니다.

## 프로젝트 목적

- Jenkins Pipeline의 기본 구조와 자주 쓰는 지시어를 작은 예제로 익힙니다.
- 실제 프로젝트에 적용하기 전에 안전한 명령(`echo`, `mkdir`, 간단한 파일 생성`)으로 흐름을 확인합니다.
- 예제별 주석을 통해 "어떤 상황에서 이 문법을 쓰는지"를 이해할 수 있게 합니다.

## 학습 순서

| 순서 | 예제 | 학습 포인트 |
|------|------|-------------|
| 1 | **01-hello-world** | 가장 기본적인 파이프라인, `stage`, `steps`, 환경 정보 출력 |
| 2 | **02-build-and-test** | 빌드 및 테스트 실행, 산출물 보관 |
| 3 | **03-multi-stage** | 여러 단계로 구성된 배포 흐름, `when` 조건 |
| 4 | **04-parameters** | 빌드 파라미터와 조건부 stage |
| 5 | **05-parallel-stages** | 독립 작업 병렬 실행 |
| 6 | **06-environment-variables** | 전역/stage 환경 변수와 동적 변수 |
| 7 | **07-post-actions** | 빌드 결과에 따른 후처리 |
| 8 | **08-docker-pipeline** | Docker 명령과 Docker Pipeline 패턴 |
| 9 | **09-pipeline-options** | 타임아웃, 재시도, 동시 실행 방지, 빌드 기록 보관 |

## 용어 설명

| 용어 | 설명 |
|------|------|
| Pipeline | Jenkins에서 작업 흐름을 정의하는 스크립트 |
| Stage | 파이프라인의 논리적 단계 (예: Build, Test, Deploy) |
| Step | Stage 내에서 실행되는 단일 작업 |
| Agent | 파이프라인이 실행될 환경 |
| Declarative Pipeline | 선언형 방식의 파이프라인 (권장) |
| Scripted Pipeline | 스크립트 방식의 파이프라인 |

## 파이프라인 구조

```
pipeline {
    agent any          // 어디서 실행할지
    stages {           // 단계들
        stage('단계이름') {
            steps {    // 실행할 작업들
                // 작업 내용
            }
        }
    }
    post {             // 빌드 후 처리
        // 결과에 따른 작업
    }
}
```

## 사용 방법

### Jenkins UI에 붙여넣기

1. Jenkins 대시보드에서 "New Item" 클릭
2. 프로젝트 이름 입력 후 "Pipeline" 선택
3. "Pipeline" 섹션으로 스크롤
4. Definition에서 "Pipeline script" 선택
5. 예제 `Jenkinsfile` 내용 붙여넣기
6. "Save" 후 "Build Now" 클릭

### Git 저장소에서 불러오기

1. Jenkins 대시보드에서 "New Item" 클릭 후 "Pipeline" 선택
2. Definition에서 "Pipeline script from SCM" 선택
3. SCM을 Git으로 선택하고 저장소 URL 입력
4. Script Path에 실행할 예제 경로 입력 (예: `01-hello-world/Jenkinsfile`)
5. "Save" 후 "Build Now" 클릭

## 실행 전 확인

- 예제는 `sh` 스텝을 사용하므로 Linux/Unix 계열 Jenkins 에이전트에서 실행하는 것을 권장합니다.
- Docker 예제는 Docker가 설치된 에이전트에서만 실제 Docker 명령을 실행하세요.
- 로컬에서는 `scripts/validate-jenkinsfiles.sh`로 공백 오류를 확인할 수 있습니다.
- Jenkins Declarative Linter를 사용하려면 `JENKINS_URL`과 `JENKINS_CLI_JAR`를 설정한 뒤 같은 스크립트를 실행하세요.

```bash
scripts/validate-jenkinsfiles.sh

JENKINS_URL=http://localhost:8080 \
JENKINS_CLI_JAR=./jenkins-cli.jar \
scripts/validate-jenkinsfiles.sh
```

## 참고

- 모든 예제는 Declarative Pipeline 방식을 사용합니다.
- 실제 프로젝트에 적용하기 전에 테스트 환경에서 먼저 확인하세요
- Jenkins 공식 Pipeline 문서: https://www.jenkins.io/doc/book/pipeline/
