# Git 일일 워크플로우 예제

> 실무에서 매일 사용하는 Git 명령어 패턴들

## 🌅 출근 후 첫 작업

```bash
# 1. 프로젝트 디렉토리로 이동
cd ~/workspace/my-project

# 2. 현재 상태 확인
git status

# 3. 최신 변경사항 가져오기
git checkout main
git pull origin main

# 4. 오늘 작업할 브랜치 확인/생성
git branch -a  # 모든 브랜치 확인
```

## 💻 새 기능 개발 시작

```bash
# Feature 브랜치 생성 및 전환
git checkout -b feature/user-notification

# 또는 기존 브랜치가 있다면
git checkout feature/user-notification
git rebase main  # main의 최신 변경사항 반영
```

## 🔨 개발 중 작업 패턴

### 작업 중간 저장

```bash
# 변경사항 확인
git status
git diff

# 의미 있는 단위로 커밋
git add src/services/notification.go
git commit -m "feat: 알림 서비스 기본 구조 구현"

# 다음 작업
git add tests/notification_test.go
git commit -m "test: 알림 서비스 단위 테스트 추가"

# 전체 추가 (신중하게)
git add .
git commit -m "docs: 알림 API 문서 업데이트"
```

### 작업 임시 저장 (급한 업무 발생 시)

```bash
# 현재 작업 임시 저장
git stash save "WIP: 알림 기능 작업 중"

# 급한 hotfix 작업
git checkout main
git checkout -b hotfix/critical-bug
# ... 급한 작업 ...
git add .
git commit -m "hotfix: 크리티컬 버그 수정"
git push origin hotfix/critical-bug

# 원래 작업으로 복귀
git checkout feature/user-notification
git stash pop
```

## 🔄 정기적인 동기화 (점심/오후)

```bash
# main 브랜치 최신화
git checkout main
git pull origin main

# 작업 브랜치로 돌아가서 최신 변경사항 반영
git checkout feature/user-notification
git rebase main

# 충돌 발생 시
git status  # 충돌 파일 확인
# 파일 편집하여 충돌 해결
git add resolved-file.go
git rebase --continue
```

## 📤 작업 완료 후 푸시 및 PR 생성

```bash
# 최종 확인
git log --oneline -5  # 최근 커밋들 확인
git diff origin/main..HEAD  # main과의 차이점 확인

# 원격에 푸시
git push origin feature/user-notification

# 첫 푸시인 경우
git push --set-upstream origin feature/user-notification

# GitHub CLI로 PR 생성 (권장)
gh pr create \
    --title "feat: 사용자 알림 시스템 구현" \
    --body "
## 📋 변경사항
- 실시간 알림 기능 추가
- 이메일 알림 설정 구현
- 알림 히스토리 저장

## 🧪 테스트
- [x] 단위 테스트 통과
- [x] 통합 테스트 완료
- [x] 브라우저 테스트 완료

Closes #789
" \
    --reviewer "team-lead" \
    --label "feature,backend" \
    --draft

echo "✅ Draft PR 생성 완료! 리뷰 준비되면 gh pr ready로 변경하세요"

# 또는 스크립트 사용
./scripts/github-api.sh pr "feat: 사용자 알림 시스템 구현" "상세 설명..." main false
```

## 🎯 하루 마무리

```bash
# 현재 상태 확인
git status

# 작업하지 않은 변경사항이 있다면
git stash save "EOD: $(date '+%Y-%m-%d') 작업 종료"

# 또는 커밋
git add .
git commit -m "WIP: $(date '+%Y-%m-%d') 진행 상황 저장"

# 백업 (중요한 작업인 경우)
git bundle create ../backup-$(date +%Y%m%d).bundle HEAD
```

## 🔥 긴급 상황 대응

### 실수한 커밋 되돌리기

```bash
# 최근 커밋 취소 (파일은 유지)
git reset --soft HEAD~1

# 파일까지 완전히 되돌리기
git reset --hard HEAD~1

# 안전한 되돌리기 (히스토리 보존)
git revert HEAD
```

### 잘못된 브랜치에 커밋한 경우

```bash
# 현재 브랜치: feature/wrong-branch
# 이동하려는 브랜치: feature/correct-branch

# 1. 올바른 브랜치 생성/전환
git checkout -b feature/correct-branch

# 2. 잘못된 브랜치로 이동
git checkout feature/wrong-branch

# 3. 최근 커밋 취소
git reset --hard HEAD~1

# 4. 올바른 브랜치로 이동
git checkout feature/correct-branch
# 커밋이 이미 여기에 있음
```

### 충돌 해결이 어려울 때

```bash
# 현재 merge/rebase 중단
git merge --abort
# 또는
git rebase --abort

# 다른 방법 시도 (예: merge 대신 rebase)
git checkout feature/my-branch
git merge main  # rebase 대신 merge 사용
```

## 📊 팀 협업 시나리오

### Pull Request 생성 전 체크리스트

```bash
# 1. 최신 main과 동기화
git checkout main && git pull origin main
git checkout feature/my-feature && git rebase main

# 2. 테스트 실행
go test ./...  # Go 프로젝트 예시
npm test       # Node.js 프로젝트 예시

# 3. 코드 스타일 검사
gofmt -s -w .  # Go
npm run lint   # JavaScript/TypeScript

# 4. 커밋 메시지 검토
git log --oneline origin/main..HEAD

# 5. 변경사항 요약 확인
git diff --stat origin/main..HEAD

# 6. GitHub CLI로 PR 생성 및 체크
gh pr create --title "feat: 새 기능 구현" --draft
gh pr checks  # CI/CD 상태 확인
```

### GitHub PR 기반 코드 리뷰 과정

```bash
# PR 상태 확인
./scripts/github-api.sh pr-status 123

# Draft PR을 Ready 상태로 변경
gh pr ready 123
# 또는
./scripts/github-api.sh pr-ready 123

# 리뷰 요청 후 피드백 받기
# 리뷰어가 변경 요청을 한 경우 피드백 반영

# 리뷰 피드백 반영 후
git add .
git commit -m "refactor: 리뷰 피드백 반영 - 변수명 개선"

# Force push (주의: 혼자 작업하는 브랜치에서만)
git push --force-with-lease origin feature/my-feature

# PR에 코멘트로 알림
gh pr comment 123 --body "@team-lead 피드백 반영 완료했습니다. 다시 확인 부탁드립니다!"

# 승인받은 후 머지
./scripts/github-api.sh pr-merge 123 squash true
```

### PR 리뷰어 역할 (동료 작업 검토)

```bash
# 리뷰할 PR 목록 확인
gh pr list --author "colleague-name"

# 특정 PR 로컬에서 테스트
gh pr checkout 123
# 또는
./scripts/github-api.sh pr-checkout 123

# 변경사항 확인 및 테스트
git diff main..HEAD
go test ./...

# 리뷰 제출
gh pr review 123 --approve --body "LGTM! 훌륭한 구현입니다."

# 또는 변경 요청
gh pr review 123 --request-changes --body "몇 가지 수정이 필요합니다."

# 스크립트 사용
./scripts/github-api.sh pr-review 123 approve "LGTM!"
```

## 🎯 Pro Tips

### 자주 사용하는 명령어 조합

```bash
# 매일 아침 루틴
alias morning="git checkout main && git pull origin main && git status"

# 커밋 전 확인
alias precommit="git status && git diff --cached"

# 브랜치 정리 (머지된 브랜치 삭제)
alias cleanup="git branch --merged main | grep -v main | xargs -n 1 git branch -d"

# 로그 예쁘게 보기
alias glog="git log --graph --oneline --decorate --all"

# PR 관련 유용한 alias
alias pr-create="gh pr create --draft"
alias pr-list="gh pr list --author @me"
alias pr-status="gh pr status"
alias pr-merge="gh pr merge --squash --delete-branch"

# GitHub CLI와 스크립트 조합
alias pr-quick="./scripts/github-api.sh pr"
alias pr-check="./scripts/github-api.sh pr-status"
```

### GitHub PR 워크플로우 자동화

```bash
# 완전한 PR 생성 및 관리 워크플로우
create_and_manage_pr() {
    local title="$1"
    local body="$2"
    
    # 1. 현재 브랜치 확인
    local branch=$(git branch --show-current)
    if [ "$branch" = "main" ]; then
        echo "❌ main 브랜치에서는 PR을 생성할 수 없습니다"
        return 1
    fi
    
    # 2. 최신 상태로 업데이트
    echo "🔄 최신 상태로 업데이트 중..."
    git fetch origin
    git rebase origin/main
    
    # 3. 테스트 실행
    echo "🧪 테스트 실행 중..."
    npm test || go test ./... || echo "⚠️ 테스트 실패"
    
    # 4. 푸시
    echo "📤 브랜치 푸시 중..."
    git push -u origin "$branch"
    
    # 5. Draft PR 생성
    echo "📝 Draft PR 생성 중..."
    local pr_url=$(gh pr create --title "$title" --body "$body" --draft)
    echo "✅ Draft PR 생성: $pr_url"
    
    # 6. 상태 확인
    echo "📊 PR 상태:"
    gh pr status
    
    echo ""
    echo "💡 다음 단계:"
    echo "  - 코드 리뷰 준비되면: gh pr ready"
    echo "  - CI/CD 확인: gh pr checks"
    echo "  - 머지: gh pr merge --squash"
}

# 사용법
# create_and_manage_pr "feat: 새 기능" "상세 설명..."
```

### PR 기반 일일 워크플로우 요약

```bash
# 📅 아침 루틴
morning_routine() {
    echo "🌅 개발 하루 시작!"
    
    # 1. main 브랜치 최신화
    git checkout main && git pull origin main
    
    # 2. 나의 PR 상태 확인
    echo "📋 나의 PR 현황:"
    gh pr list --author "@me" --state open
    
    # 3. 리뷰 요청된 PR 확인
    echo "👀 리뷰 요청 받은 PR:"
    gh pr list --review-requested "@me"
    
    # 4. 작업할 브랜치로 이동
    echo "🌿 작업 브랜치 목록:"
    git branch | grep -v main
}

# 🌆 저녁 마무리
evening_routine() {
    echo "🌙 하루 마무리!"
    
    # 1. 현재 작업 상태 확인
    git status
    
    # 2. 작업 중인 내용이 있다면 임시 저장
    if ! git diff-index --quiet HEAD --; then
        git stash save "EOD: $(date '+%Y-%m-%d') 작업 종료"
        echo "💾 작업 내용을 임시 저장했습니다"
    fi
    
    # 3. PR 상태 최종 확인
    echo "📊 오늘의 PR 활동:"
    gh pr list --author "@me" --state open
    
    # 4. 내일 할 일 메모 (선택사항)
    echo "📝 내일 할 일을 메모해두세요..."
}
```

### 설정 최적화

```bash
# 자동 rebase 설정
git config --global pull.rebase true

# 기본 에디터 설정
git config --global core.editor "code --wait"

# 유용한 alias들
git config --global alias.undo 'reset --soft HEAD~1'
git config --global alias.recommit 'commit --amend --no-edit'
git config --global alias.last 'log -1 HEAD --stat'
```

이 워크플로우를 참고하여 본인의 업무 패턴에 맞게 조정해서 사용하세요!