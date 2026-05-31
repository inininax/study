# Jenkins Pipeline 초보자 가이드

## Jenkins란?

Jenkins는 자동화 서버로, 소프트웨어 빌드, 테스트, 배포를 자동화합니다.

## Pipeline이란?

Pipeline은 Jenkins에서 작업 흐름을 코드로 정의하는 기능입니다.
`Jenkinsfile`이라는 파일에 파이프라인을 작성합니다.

## 기본 구조

```groovy
pipeline {
    agent any              // 실행 환경 지정
    environment { }        // 환경 변수
    stages {
        stage('단계명') {  // 논리적 단계
            steps {        // 실제 실행 명령
                sh '명령어'
            }
        }
    }
    post { }               // 빌드 후 처리
}
```

## 주요 키워드

| 키워드 | 설명 | 예시 |
|--------|------|------|
| `pipeline` | 전체 파이프라인 정의 | `pipeline { }` |
| `agent` | 실행 환경 | `agent any` |
| `stages` | 모든 단계 포함 | `stages { }` |
| `stage` | 개별 단계 | `stage('Build')` |
| `steps` | 실행 명령 | `steps { sh 'echo hello' }` |
| `environment` | 환경 변수 | `environment { NAME = 'value' }` |
| `options` | 실행 정책 | `options { timeout(time: 30, unit: 'MINUTES') }` |
| `post` | 빌드 후 처리 | `post { success { } }` |
| `sh` | 쉘 명령 실행 | `sh 'ls -la'` |
| `echo` | 메시지 출력 | `echo 'Hello'` |

## 조건문

### when (단계 조건)
```groovy
stage('Deploy') {
    when {
        branch 'main'        // main 브랜치에서만 실행
    }
    steps {
        echo 'Deploying...'
    }
}
```

### script (Groovy 조건)
```groovy
script {
    if (env.BRANCH_NAME == 'main') {
        echo 'main 브랜치'
    }
}
```

## 환경 변수

### Jenkins 기본 변수
- `env.JOB_NAME` - 잡 이름
- `env.BUILD_NUMBER` - 빌드 번호
- `env.BUILD_URL` - 빌드 URL
- `env.WORKSPACE` - 작업 디렉토리
- `env.BRANCH_NAME` - 브랜치 이름 (Multibranch Pipeline)

### 사용자 정의
```groovy
environment {
    MY_VAR = 'value'
}
```

## 실행 정책(options)

`options`는 파이프라인 전체 또는 특정 stage의 실행 방식을 제어합니다. 운영 환경에서는 빌드가 무한정 실행되거나, 같은 잡이 동시에 실행되거나, 빌드 기록이 지나치게 많이 쌓이는 상황을 막는 데 자주 사용합니다.

```groovy
pipeline {
    agent any
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
        skipDefaultCheckout()
    }
    stages {
        stage('Build') {
            options {
                retry(2)
                timeout(time: 5, unit: 'MINUTES')
            }
            steps {
                echo 'Building...'
            }
        }
    }
}
```

| 옵션 | 설명 |
|------|------|
| `buildDiscarder` | 오래된 빌드 기록과 산출물을 정리 |
| `disableConcurrentBuilds` | 같은 Pipeline 잡의 동시 실행 방지 |
| `timeout` | 지정한 시간을 넘기면 빌드 또는 stage 중단 |
| `retry` | 일시적인 실패가 났을 때 stage 재시도 |
| `skipDefaultCheckout` | 자동 SCM 체크아웃을 끄고 직접 `checkout scm` 실행 |

## 파이프라인 설정 방법

### 방법 1: Jenkinsfile 직접 입력
1. Jenkins 대시보드 > New Item
2. 프로젝트 이름 입력 > Pipeline 선택
3. Pipeline 섹션 > Definition: "Pipeline script"
4. 스크립트 입력 > Save

### 방법 2: SCM에서 가져오기
1. Jenkins 대시보드 > New Item
2. 프로젝트 이름 입력 > Pipeline 선택
3. Pipeline 섹션 > Definition: "Pipeline script from SCM"
4. SCM(Git 등) 선택 > 저장소 URL 입력
5. Script Path: `Jenkinsfile` > Save

## 검증 방법

예제를 수정한 뒤에는 먼저 저장소 스크립트로 기본 오류를 확인합니다.

```bash
scripts/validate-jenkinsfiles.sh
```

Jenkins 서버가 있다면 Declarative Linter도 함께 실행할 수 있습니다.

```bash
JENKINS_URL=http://localhost:8080 \
JENKINS_CLI_JAR=./jenkins-cli.jar \
scripts/validate-jenkinsfiles.sh
```

## 자주 사용하는 명령어

```groovy
// 메시지 출력
echo 'Hello World'

// 쉘 명령 실행
sh 'ls -la'
sh 'npm install'
sh 'npm test'
sh 'docker build -t myapp .'

// 결과 저장
sh(returnStdout: true, script: 'date').trim()

// 디렉토리 생성
sh 'mkdir -p output'

// 파일 읽기/쓰기
sh 'echo "content" > file.txt'
```

## 디버깅 팁

1. **콘솔 출력 확인**: 빌드 > Console Output에서 로그 확인
2. **echo 활용**: 각 단계에서 `echo`로 상태 확인
3. **simple pipeline**: 복잡한 파이프라인은 작은 단계부터 시작
4. **Blue Ocean 플러그인**: 시각적 파이프라인 확인

## 다음 단계

1. 예제 01부터 순서대로 실행해보기
2. 각 예제의 주석을 읽고 이해하기
3. 자신의 프로젝트에 맞춰 수정해보기
4. Jenkins 공식 문서 참고: https://www.jenkins.io/doc/book/pipeline/
