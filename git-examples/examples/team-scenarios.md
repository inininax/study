# 팀 협업 시나리오 예제

> 실무에서 자주 발생하는 팀 협업 상황과 Git 해결책

## 👥 시나리오 1: 새 팀원 온보딩

### 프로젝트 초기 설정

```bash
# 1. 저장소 클론
git clone https://github.com/company/backend-api.git
cd backend-api

# 2. 개발 환경 설정
git config user.name "김신입"
git config user.email "kim.newbie@company.com"

# 3. 브랜치 전략 이해
git branch -a  # 모든 브랜치 확인
git log --graph --oneline --all -10  # 브랜치 구조 파악

# 4. 첫 번째 작업 브랜치 생성
git checkout -b feature/setup-development-environment
```

### 첫 기여하기

```bash
# 1. 간단한 문서 수정
echo "## 개발 환경 설정 가이드" >> README.md
git add README.md
git commit -m "docs: 개발 환경 설정 가이드 추가"

# 2. 푸시 및 PR 생성
git push -u origin feature/setup-development-environment
# GitHub에서 Pull Request 생성

# 3. 리뷰 반영
# ... 코드 리뷰 후 수정 ...
git add .
git commit -m "docs: 리뷰 반영 - 설명 더 명확하게 수정"
git push origin feature/setup-development-environment
```

## 🔥 시나리오 2: 긴급 핫픽스

### 프로덕션 버그 발견

```bash
# 현재 feature 작업 중이었음
git status  # 작업 중인 파일 확인

# 1. 현재 작업 임시 저장
git stash save "WIP: 사용자 프로필 API 작업 중"

# 2. main 브랜치에서 hotfix 브랜치 생성
git checkout main
git pull origin main
git checkout -b hotfix/login-security-fix

# 3. 긴급 수정
# src/auth/jwt.go 파일 수정
git add src/auth/jwt.go
git commit -m "hotfix: JWT 토큰 검증 보안 취약점 수정

- 토큰 만료 시간 검증 추가
- 서명 알고리즘 제한 강화
- CVE-2023-XXXX 보안 이슈 해결"

# 4. 즉시 푸시 및 리뷰
git push -u origin hotfix/login-security-fix
```

### 핫픽스 배포 후 정리

```bash
# 1. main에 머지 후 태그 생성
git checkout main
git pull origin main
git tag -a v1.2.1 -m "Security hotfix v1.2.1"
git push origin v1.2.1

# 2. 다른 브랜치들에 반영
git checkout develop  # 개발 브랜치가 있다면
git merge main

# 3. 원래 작업 복귀
git checkout feature/user-profile-api
git stash pop
git rebase main  # 핫픽스 내용 포함
```

## 🚀 시나리오 3: 대규모 기능 개발 (팀 작업)

### Feature 브랜치 협업 전략

```bash
# 메인 개발자 (팀 리더)
git checkout -b feature/payment-system
git push -u origin feature/payment-system

# 기본 구조 구현
mkdir src/payment
touch src/payment/service.go src/payment/model.go
git add src/payment/
git commit -m "feat: 결제 시스템 기본 구조 생성"
git push origin feature/payment-system
```

### 팀원들의 세부 작업

```bash
# 팀원 A: 결제 서비스 구현
git checkout feature/payment-system
git pull origin feature/payment-system
git checkout -b feature/payment-service

# 개발 작업...
git add src/payment/service.go
git commit -m "feat: 결제 서비스 핵심 로직 구현"
git push -u origin feature/payment-service

# 팀원 B: 결제 모델 구현
git checkout feature/payment-system
git pull origin feature/payment-system
git checkout -b feature/payment-model

# 개발 작업...
git add src/payment/model.go tests/payment/model_test.go
git commit -m "feat: 결제 모델 및 테스트 구현"
git push -u origin feature/payment-model
```

### 하위 브랜치 통합

```bash
# 메인 개발자가 하위 브랜치들 머지
git checkout feature/payment-system

# 팀원 A 작업 머지
git merge feature/payment-service
git branch -d feature/payment-service
git push origin --delete feature/payment-service

# 팀원 B 작업 머지
git merge feature/payment-model
git branch -d feature/payment-model
git push origin --delete feature/payment-model

# 통합된 결과 푸시
git push origin feature/payment-system
```

## 🔄 시나리오 4: 충돌 해결 및 협업

### 동시 작업으로 인한 충돌

```bash
# 개발자 A의 상황
git checkout -b feature/user-auth-a
# src/auth/handler.go 파일 수정
git add src/auth/handler.go
git commit -m "feat: 로그인 핸들러 구현"
git push -u origin feature/user-auth-a

# 개발자 B의 상황 (같은 파일 수정)
git checkout -b feature/user-auth-b
# src/auth/handler.go 파일 수정 (다른 부분)
git add src/auth/handler.go
git commit -m "feat: 회원가입 핸들러 구현"
git push -u origin feature/user-auth-b
```

### A가 먼저 머지된 후 B의 충돌 해결

```bash
# 개발자 B: main 브랜치 최신화
git checkout main
git pull origin main

# 충돌 발생할 브랜치로 이동하여 rebase
git checkout feature/user-auth-b
git rebase main

# 충돌 발생!
# Auto-merging src/auth/handler.go
# CONFLICT (content): Merge conflict in src/auth/handler.go

# 충돌 파일 편집
code src/auth/handler.go
```

**충돌 해결 예시:**
```go
// src/auth/handler.go 충돌 해결 전
func LoginHandler(w http.ResponseWriter, r *http.Request) {
<<<<<<< HEAD
    // A의 로그인 로직
    username := r.FormValue("username")
    password := r.FormValue("password")
=======
    // B의 회원가입 로직 (잘못된 위치)
    email := r.FormValue("email")
    password := r.FormValue("password")
>>>>>>> feature/user-auth-b
}

// 충돌 해결 후
func LoginHandler(w http.ResponseWriter, r *http.Request) {
    username := r.FormValue("username")
    password := r.FormValue("password")
    // 로그인 로직...
}

func SignupHandler(w http.ResponseWriter, r *http.Request) {
    email := r.FormValue("email")
    password := r.FormValue("password")
    // 회원가입 로직...
}
```

```bash
# 충돌 해결 후
git add src/auth/handler.go
git rebase --continue
git push --force-with-lease origin feature/user-auth-b
```

## 📋 시나리오 5: GitHub PR 기반 코드 리뷰 프로세스

### GitHub CLI를 활용한 PR 생성

```bash
# 1. Self 리뷰
git diff origin/main..HEAD
git log --oneline origin/main..HEAD

# 2. 테스트 실행
go test ./...
go vet ./...

# 3. 코드 포맷팅
gofmt -s -w .
git add -A
git commit -m "style: 코드 포맷팅 적용"

# 4. 커밋 정리 (필요한 경우)
git rebase -i HEAD~3  # 최근 3개 커밋 정리

# 5. GitHub CLI로 PR 생성
gh pr create \
    --title "feat: 결제 시스템 구현" \
    --body "
## 📋 변경사항
- 신용카드 결제 API 구현
- 결제 검증 로직 추가
- 결제 히스토리 저장 기능

## 🧪 테스트
- [x] 단위 테스트 통과
- [x] 통합 테스트 통과
- [x] 보안 검사 완료

Closes #456
" \
    --reviewer "team-lead,senior-dev" \
    --label "feature,backend" \
    --assignee "@me"

echo "✅ PR 생성 완료! 리뷰 요청이 전송되었습니다."
```

### 리뷰어의 코드 리뷰 과정

```bash
# 1. PR 목록 확인
gh pr list --author "developer-name"

# 2. 특정 PR 체크아웃하여 로컬 테스트
gh pr checkout 123

# 3. 변경사항 분석
git diff main..feature/payment-system
git log main..feature/payment-system --oneline

# 4. 로컬에서 테스트 실행
go test ./...
go run main.go  # 실행 테스트

# 5. 코드 리뷰 작성 (승인)
gh pr review 123 --approve --body "
🎉 LGTM! 훌륭한 구현입니다.

### 좋은 점들:
- 에러 핸들링이 체계적으로 잘 되어 있음
- 테스트 커버리지가 높음
- 코드 구조가 명확하고 읽기 쉬움

### 마이너 제안:
- 주석을 조금 더 추가하면 좋을 것 같습니다
- 성능 최적화 여지가 있어 보입니다

머지 승인합니다! 🚀
"

# 6. 변경 요청이 필요한 경우
gh pr review 123 --request-changes --body "
몇 가지 수정이 필요합니다:

### 필수 수정사항:
1. 보안 취약점 수정 필요 (line 45)
2. 메모리 누수 가능성 (line 123)
3. 테스트 케이스 추가 필요

### 개선 제안:
- 함수명을 더 명확하게 변경
- 에러 메시지 개선

수정 후 다시 리뷰 요청해주세요.
"
```

### 작성자의 리뷰 피드백 반영

```bash
# 리뷰 피드백 확인
gh pr view 123

# 피드백 반영을 위한 수정 작업
# 1. 보안 취약점 수정
# 2. 메모리 누수 수정
# 3. 테스트 케이스 추가

# 수정사항 커밋
git add .
git commit -m "refactor: 코드 리뷰 피드백 반영

- 보안 취약점 수정: JWT 토큰 검증 강화
- 메모리 누수 수정: defer 패턴으로 리소스 정리
- ProcessPayment -> ProcessCreditCardPayment 함수명 변경
- 에러 핸들링 개선: 구체적인 에러 메시지 추가
- 테스트 케이스 추가: 엣지 케이스 검증

Addresses review comments from @team-lead"

# 푸시 및 리뷰 재요청
git push origin feature/payment-system

# 리뷰어에게 코멘트로 알림
gh pr comment 123 --body "
@team-lead @senior-dev 피드백 주신 모든 사항을 반영했습니다! 🙏

### 수정 내용:
✅ 보안 취약점 수정 완료
✅ 메모리 누수 해결
✅ 함수명 개선 
✅ 테스트 커버리지 95%로 향상

다시 리뷰 부탁드립니다.
"

# Fixup 커밋 활용 (기존 커밋에 합치기)
git commit --fixup=abc1234  # 특정 커밋 ID
git rebase -i --autosquash HEAD~5  # 자동으로 정리

git push --force-with-lease origin feature/payment-system
```

### PR 승인 후 머지 과정

```bash
# 모든 리뷰어가 승인한 후 작성자가 머지
gh pr checks 123  # CI/CD 상태 최종 확인

# Squash merge로 머지 (권장)
gh pr merge 123 --squash --delete-branch

# 또는 일반 merge
gh pr merge 123 --merge --delete-branch

# 머지 후 로컬 정리
git checkout main
git pull origin main
git branch -d feature/payment-system

echo "✅ PR 머지 완료! 로컬 브랜치도 정리되었습니다."
```

### 고급 PR 리뷰 시나리오

```bash
# 대규모 PR의 부분별 리뷰
# 파일별로 나누어 리뷰하는 경우
gh pr view 123 --json files | jq '.files[].filename'

# 특정 커밋만 리뷰하는 경우
git show abc1234  # 특정 커밋 확인
gh pr comment 123 --body "커밋 abc1234에서 훌륭한 리팩토링입니다!"

# Draft PR에서 WIP 피드백
gh pr comment 123 --body "
🚧 Work in Progress 피드백:

### 현재 진행상황 좋습니다:
- 기본 구조가 잘 잡혀있음
- 테스트 방향성이 좋음

### 완료 전 확인 사항:
- [ ] 에러 핸들링 추가
- [ ] 성능 테스트 실행
- [ ] 문서 업데이트

완료되면 ready for review로 변경해주세요!
"

# PR을 ready 상태로 변경
gh pr ready 123
```

### 팀 리뷰 정책 자동화

```bash
# .github/workflows/pr-review.yml
# 자동으로 팀 멤버 할당 및 라벨링

# PR 템플릿 체크 스크립트
check_pr_template() {
    local pr_number=$1
    local pr_body=$(gh pr view $pr_number --json body -q .body)
    
    if [[ "$pr_body" =~ "## 📋 변경사항" ]]; then
        echo "✅ PR 템플릿이 올바르게 사용되었습니다."
        gh pr edit $pr_number --add-label "template-ok"
    else
        echo "❌ PR 템플릿을 사용해주세요."
        gh pr comment $pr_number --body "
⚠️ PR 템플릿을 사용해주세요.

템플릿 가이드: [PR 가이드](docs/pr-template.md)
"
        gh pr edit $pr_number --add-label "template-missing"
    fi
}

# 사용법
check_pr_template 123
```

## 🎯 시나리오 6: 릴리스 관리

### 릴리스 브랜치 생성

```bash
# 릴리스 관리자
git checkout main
git pull origin main
git checkout -b release/v2.0.0

# 버전 정보 업데이트
echo "v2.0.0" > VERSION
git add VERSION
git commit -m "chore: 버전 v2.0.0으로 업데이트"

# 릴리스 브랜치 푸시
git push -u origin release/v2.0.0
```

### 릴리스 준비 중 버그 수정

```bash
# QA에서 버그 발견
git checkout release/v2.0.0
git checkout -b bugfix/login-validation

# 버그 수정
git add .
git commit -m "fix: 로그인 입력 값 검증 로직 수정"

# 릴리스 브랜치에 머지
git checkout release/v2.0.0
git merge bugfix/login-validation
git branch -d bugfix/login-validation

# main과 develop에도 반영 (필요한 경우)
git checkout main
git merge release/v2.0.0

git checkout develop
git merge main
```

### 릴리스 완료

```bash
# 릴리스 태그 생성
git checkout main
git tag -a v2.0.0 -m "Release v2.0.0

주요 변경사항:
- 새로운 결제 시스템 추가
- 사용자 인증 개선
- 성능 최적화"

git push origin v2.0.0

# 릴리스 브랜치 삭제
git branch -d release/v2.0.0
git push origin --delete release/v2.0.0
```

## 📊 팀 협업 Best Practices

### 일관성 있는 커밋 메시지

```bash
# Conventional Commits 스타일
git commit -m "feat(auth): JWT 토큰 기반 인증 시스템 구현"
git commit -m "fix(payment): 결제 금액 계산 오류 수정"
git commit -m "docs(api): 사용자 API 문서 업데이트"
git commit -m "test(user): 사용자 서비스 단위 테스트 추가"
git commit -m "refactor(db): 데이터베이스 연결 로직 개선"
```

### 브랜치 네이밍 규칙

```bash
# 기능 개발
feature/user-authentication
feature/payment-integration
feature/order-management

# 버그 수정
bugfix/login-error
bugfix/payment-calculation

# 핫픽스
hotfix/security-vulnerability
hotfix/critical-bug

# 릴리스
release/v1.2.0
release/2023-q4

# 실험/연구
experiment/new-database
spike/performance-optimization
```

### 팀 동기화 전략

```bash
# 매일 아침 팀 동기화
git checkout main
git pull origin main
git checkout feature/my-feature
git rebase main

# 주간 브랜치 정리
git branch --merged main | grep -v main | xargs -n 1 git branch -d
git remote prune origin

# 월간 저장소 정리
git gc --aggressive
git repack -ad
```

이러한 시나리오들을 통해 실제 팀 협업에서 발생할 수 있는 다양한 상황에 대비할 수 있습니다!