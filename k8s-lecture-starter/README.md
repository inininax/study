# Kubernetes study

## 원문 출처
- 강의 자료: [인프런 쉽게 시작하는 쿠버네티스(Kubernetes) 강의](https://www.inflearn.com/course/%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4-%EC%89%BD%EA%B2%8C%EC%8B%9C%EC%9E%91/dashboard)
- 개념 원문: [조대협님의 블로그](https://bcho.tistory.com/category/%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C%20%EC%BB%B4%ED%93%A8%ED%8C%85%20%26%20NoSQL/%EB%8F%84%EC%BB%A4%20%26%20%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4)

---

## 쉽게 시작하는 쿠버네티스(Kubernetes) 강의 Study
### 예제 실습
- [1.2. 코드로 쉽게 구성하는 쿠버네티스 랩 환경](./0102.md)
- [1.3. 쿠버네티스 랩을 쉽게 접근하기 위한 터미널 구성](./0103.md)
- [2.1. 배포를 통해 확인하는 파드(Pod)](./0201.md)
- [2.2. 파드를 외부에서도 접속하게 하는 서비스(Service)](./0202.md)
- [2.3. 파드와 디플로이먼트(Deployment) 차이](./0203.md)
- [2.4. 외부로 노출하는 더 좋은 방법인 로드 밸런서(LoadBalancer)](./0204.md)

---

## Kubernetes 기초 개념
- 구글 내부 Borg, Go로 구현, 클라우드 네이티브 컴퓨팅 재단(Cloud Native Computing Foundation, CNCF)에 제공

### 마스터와 노드 (쿠버네티스 클러스터)
- 마스터: 클러스터 전체를 관리하는 컨트롤러
- 노드: 컨테이너가 배포되는 머신 (가상 또는 물리 서버머신)

### 오브젝트
- 오브젝트 스펙(Object Spec)
    - 오브젝트 설정 정보를 기술한 스펙
    - 커맨드 라인의 인자 또는 파일(yaml, json)로 정의
- 기본 오브젝트(Basic Object): Pod, Volume, Service, Name space

#### Pod
- 가장 기본적인 배포 단위
- 컨테이너들을 포함하는 단위 (단일 구성 또는, App+Logger+Reverse proxy 등...)
- Pod 내의 컨테이너들은 IP와 Port를 공유한다.
- Pod 내의 컨테이너들은 Volume을 공유한다.
- 예시
    ```
    apiVersion: v1
    kind: Pod
    metadata:
    name: myapp
    spec:
    containers:
    - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 8090

    출처: https://bcho.tistory.com/1256?category=731548 [조대협의 블로그]
    ```

#### Volume
- Pod의 Local storage는 영구적이지 않다.<br>
  때문에 영구적으로 파일을 저장해야할 경우 Volume을 마운트해서 사용한다.

#### Service
- 여러개의 Pod들을 로드밸러서를 사용해 하나로 묶어 Service로 사용한다.
- Pod는 동적 생성되고 지속적으로 변경될 수 있기 때문에 (IP도 변경될 수 있다.)
- Pod 생성 시 Label을 부여하고
- Service는 Label selector를 통해 Label을 골라내어 Pod를 묶고 Service로 제공할 수 있다.
- 예시 
    ```
    kind: Service
    apiVersion: v1
    metadata:
    name: my-service
    spec:
    selector:
        app: myapp
    ports:
    - protocol: TCP
        port: 80
        targetPort: 9376

    출처: https://bcho.tistory.com/1256?category=731548 [조대협의 블로그]
    ```

#### Name space
- 쿠버네티스 클러스터 내의 논리적인 분리 단위
- 네임스페이스별 접근 권한을 다르게 운영 가능
- 리소스 할당량 지정 가능
- 단, 논리적인 개념에서의 분리, 다른 네임스페이스간의 Pod라도 통신은 가능

### Label
- kubernetes의 resource를 선택하는데 사용
- 하나의 리소스에 여러개의 Label을 부여할 수 있다.
- Label은 Key, Value 형태로 부여할 수 있다.

### 컨트롤러
- 위 4가지 기본 오브젝트로 application을 설정하고 배포하는 것이 가능하다.
- 이를 편리하게 하는 것이 컨트롤러이다.
- 컨트롤러는 Replication Controller, ReplicaSet, Deployment, DaemonSet, Job, StatefulSet 등이 있다.

#### Replication Controller (RC)
- Selector: Pod들을 Label 기반으로 가져온다.
- Pod Replica 수: RC에 의해 관리될 Pod의 수이다. 예시 3일 경우 3개의 Pod을 유지한다.
- Pod Template: Pod을 추가로 생성할 때의 정보 (Docker image, Port, Label 등등)
- 주의점! Pod을 변경할 경우 기존에 생성된 Pod들이 replica 수에 따라 유지되기 때문에 과거의 Pod이 그대로 유지된다. 자동으로 삭제 후 생성하지 않는다.

#### ReplicaSet (RS)
- Replication Controller의 새버전 정도
- RC는 Equality 기반 Selector를 이용 하는데, Replica Set은 Set 기반의 Selector를 사용한다.

#### Deployment
- RC와 Replica Set의 추상화 개념
- 실제 운영에서는 추상화 개념의 Deployment를 사용
- 배포
    - 블루, 그린
    - 롤링 업그레이드

#### DaemonSet (DS)
- Pod가 각각의 노드에서 하나씩만 돌게 하는 형태로 Pod를 관리하는 컨트롤러
- 특정 노드들에게만 Pod가 하나씩 배포되도록 설정 가능 (모니터링, 로그 수집 등)

#### Job
- 워크로드 모델 중 배치나 한번 실행되고 끝나는 형태의 작업
- Job 종료 시 Pod도 함께 종료
    ```
    apiVersion: batch/v1
    kind: Job
    metadata:
    name: pi
    spec:
    template:
        spec:
        containers:
        - name: pi
            image: perl
            command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
        restartPolicy: Never
    backoffLimit: 4
    ```

#### Cron Job
- 주기적으로 정헤진 스케쥴에 따라 Job 컨트롤러 실행
    ```
    apiVersion: batch/v1beta1
    kind: CronJob
    metadata:
    name: hello
    spec:
    schedule: "*/1 * * * *"
    jobTemplate:
        spec:
        template:
            spec:
            containers:
            - name: hello
                image: busybox
                args:
                - /bin/sh
                - -c
                - date; echo Hello from the Kubernetes cluster
            restartPolicy: OnFailure
    ```

#### StatefulSet
- RC, RS 등은 데이터베이스와 같이 상태를 가진 애플리케이션을 관리하기 어렵다.
- 데이터베이스와 같이 상태를 가지는 Pod를 지원하기 위해 사용한다.
