# Git CLI 실무 가이드

> 백엔드 엔지니어를 위한 Git CLI 기본 사용법과 실무 워크플로우

## 📚 목차

1. [Git 기본 개념](#-git-기본-개념)
2. [필수 설정](#-필수-설정)
3. [기본 명령어](#-기본-명령어)
4. [브랜치 전략](#-브랜치-전략)
5. [실무 워크플로우](#-실무-워크플로우)
6. [협업 시나리오](#-협업-시나리오)
7. [문제 해결](#-문제-해결)
8. [고급 기법](#-고급-기법)
9. [성능 최적화](#-성능-최적화)

---

## 🎯 Git 기본 개념

### Git의 세 가지 영역

```bash
Working Directory → Staging Area → Repository
     (작업 공간)      (스테이징)     (저장소)
```

- **Working Directory**: 실제 파일들이 있는 작업 공간
- **Staging Area**: 커밋할 변경사항을 준비하는 공간
- **Repository**: 실제 커밋들이 저장되는 공간

### 파일 상태 이해

```bash
# 파일 상태 확인
git status

# 상태별 의미
# Untracked    : Git이 추적하지 않는 새 파일
# Modified     : 수정된 파일 (아직 staging 안됨)
# Staged       : 커밋 준비된 파일
# Committed    : 저장소에 저장된 파일
```

---

## ⚙️ 필수 설정

### 초기 설정

```bash
# 사용자 정보 설정 (필수)
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"

# 기본 브랜치명 설정
git config --global init.defaultBranch main

# 에디터 설정 (VS Code 사용 시)
git config --global core.editor "code --wait"

# 줄바꿈 설정 (OS별)
git config --global core.autocrlf true    # Windows
git config --global core.autocrlf input   # macOS/Linux

# 대소문자 구분 설정
git config --global core.ignorecase false
```

### 유용한 Alias 설정

```bash
# 자주 사용하는 명령어 단축키
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'

# 고급 alias
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
git config --global alias.unstage 'reset HEAD --'
git config --global alias.recommit 'commit --amend --no-edit'
```

---

## 🔨 기본 명령어

### 저장소 초기화

```bash
# 새 저장소 생성
git init
git init my-project    # 디렉토리 생성하며 초기화

# 기존 저장소 복제
git clone https://github.com/user/repo.git
git clone https://github.com/user/repo.git my-folder  # 다른 폴더명으로
```

### 변경사항 추적

```bash
# 현재 상태 확인
git status
git status -s          # 간결한 출력

# 변경사항 확인
git diff               # Working Directory vs Staging Area
git diff --staged      # Staging Area vs Last Commit
git diff HEAD          # Working Directory vs Last Commit
git diff HEAD~1        # 이전 커밋과 비교

# 파일별 변경사항
git diff filename.js
git diff --word-diff   # 단어 단위로 차이점 표시
```

### 파일 추가/제거

```bash
# 파일 추가
git add filename.js           # 특정 파일
git add .                     # 모든 변경사항
git add *.js                  # 패턴 매칭
git add -A                    # 모든 변경사항 (삭제 포함)
git add -p                    # 일부분만 선택적으로 추가

# 파일 제거
git rm filename.js            # 파일 삭제 및 staging
git rm --cached filename.js  # 추적만 중단 (파일은 유지)

# 파일 이동/이름 변경
git mv old-name.js new-name.js
```

### 커밋하기

```bash
# 기본 커밋
git commit -m "feat: 사용자 인증 기능 구현"

# Staging + 커밋 동시에
git commit -am "fix: 로그인 버그 수정"

# 빈 커밋 (CI 트리거용)
git commit --allow-empty -m "trigger: CI 빌드 재실행"

# 이전 커밋 수정
git commit --amend -m "새로운 커밋 메시지"
git commit --amend --no-edit    # 메시지 수정 없이
```

### 히스토리 조회

```bash
# 기본 로그
git log
git log --oneline              # 한 줄로 표시
git log --graph                # 그래프로 표시
git log -n 10                  # 최근 10개만

# 고급 로그 옵션
git log --since="2023-01-01"   # 특정 날짜 이후
git log --author="김개발"      # 특정 작성자
git log --grep="버그"          # 커밋 메시지 검색
git log --all --graph --oneline # 모든 브랜치 그래프

# 파일별 히스토리
git log filename.js
git log -p filename.js         # 변경내용과 함께
git blame filename.js          # 라인별 작성자 확인
```

---

## 🌿 브랜치 전략

### 브랜치 기본 조작

```bash
# 브랜치 확인
git branch                     # 로컬 브랜치 목록
git branch -r                  # 원격 브랜치 목록
git branch -a                  # 모든 브랜치 목록

# 브랜치 생성
git branch feature/user-auth   # 브랜치 생성만
git checkout -b feature/user-auth  # 생성 후 전환
git switch -c feature/user-auth    # Git 2.23+ 새 명령어

# 브랜치 전환
git checkout main
git switch main                # Git 2.23+ 권장

# 브랜치 삭제
git branch -d feature/user-auth     # 안전한 삭제
git branch -D feature/user-auth     # 강제 삭제
git push origin --delete feature/user-auth  # 원격 브랜치 삭제
```

### 실무 브랜치 네이밍 컨벤션

```bash
# Feature 개발
feature/user-authentication
feature/payment-integration
feature/order-management

# 버그 수정
bugfix/login-error
bugfix/memory-leak

# 핫픽스 (긴급 수정)
hotfix/security-patch
hotfix/critical-bug

# 릴리스 준비
release/v1.2.0
release/2023-q4

# 실험/연구
experiment/new-architecture
spike/performance-test
```

---

## 🔄 실무 워크플로우

### GitHub Flow (권장)

```bash
# 1. 최신 main 브랜치로 시작
git checkout main
git pull origin main

# 2. Feature 브랜치 생성
git checkout -b feature/user-profile

# 3. 개발 작업 수행
# ... 코딩 ...

# 4. 변경사항 커밋
git add .
git commit -m "feat: 사용자 프로필 조회 API 구현"

# 5. 정기적으로 main과 동기화
git checkout main
git pull origin main
git checkout feature/user-profile
git rebase main  # 또는 git merge main

# 6. 원격에 푸시
git push origin feature/user-profile

# 7. Pull Request 생성 (GitHub에서)

# 8. 코드 리뷰 후 머지

# 9. 브랜치 정리
git checkout main
git pull origin main
git branch -d feature/user-profile
```

### Conventional Commits

```bash
# 타입별 커밋 메시지 예시
git commit -m "feat: 사용자 인증 JWT 토큰 구현"
git commit -m "fix: 비밀번호 해싱 버그 수정"
git commit -m "docs: API 문서 업데이트"
git commit -m "style: 코드 포맷팅 적용"
git commit -m "refactor: 사용자 서비스 클래스 분리"
git commit -m "test: 로그인 단위 테스트 추가"
git commit -m "chore: 의존성 라이브러리 업데이트"
git commit -m "perf: 데이터베이스 쿼리 최적화"
git commit -m "ci: GitHub Actions 워크플로우 수정"

# Breaking Change
git commit -m "feat!: API 엔드포인트 변경

BREAKING CHANGE: /api/v1/users 엔드포인트가 /api/v2/users로 변경됨"
```

---

## 🤝 협업 시나리오

### 원격 저장소 관리

```bash
# 원격 저장소 확인
git remote -v

# 원격 저장소 추가
git remote add origin https://github.com/company/project.git
git remote add upstream https://github.com/original/project.git  # Fork된 경우

# 원격 브랜치 정보 업데이트
git fetch origin
git fetch --all

# 원격 브랜치 추적
git checkout -b feature/new-feature origin/feature/new-feature

# 푸시/풀
git push origin main
git pull origin main
git push --set-upstream origin feature/new-feature  # 첫 푸시 시
```

### 머지 vs 리베이스

```bash
# Merge (이력 보존)
git checkout main
git merge feature/user-auth
# 장점: 브랜치 히스토리 보존
# 단점: 복잡한 히스토리

# Rebase (선형 이력)
git checkout feature/user-auth
git rebase main
git checkout main
git merge feature/user-auth  # Fast-forward merge
# 장점: 깔끔한 선형 히스토리
# 단점: 원본 히스토리 변경

# Interactive Rebase (커밋 정리)
git rebase -i HEAD~3  # 최근 3개 커밋 정리
# pick, squash, edit, drop 등으로 커밋 조작
```

### 팀 협업 Best Practices

```bash
# 매일 아침 동기화
git checkout main
git pull origin main

# Feature 브랜치 정기 동기화 (충돌 최소화)
git checkout feature/my-feature
git rebase main  # 또는 git pull origin main --rebase

# 코드 리뷰를 위한 작은 커밋
git add -p  # 일부분만 staging
git commit -m "feat: 사용자 모델 구현"
git add .
git commit -m "test: 사용자 모델 테스트 추가"

# 푸시 전 최종 확인
git log --oneline origin/main..HEAD  # 푸시할 커밋들 확인
git diff origin/main..HEAD           # 전체 변경사항 확인
```

---

## 🚨 문제 해결

### 커밋 실수 복구

```bash
# 최근 커밋 취소 (변경사항 유지)
git reset --soft HEAD~1

# 최근 커밋 취소 (변경사항 제거)
git reset --hard HEAD~1

# 특정 파일만 이전 상태로
git checkout HEAD~1 -- filename.js

# 커밋 메시지 수정
git commit --amend -m "새로운 메시지"

# 커밋 되돌리기 (안전한 방법)
git revert HEAD         # 최근 커밋 되돌리기
git revert HEAD~2..HEAD # 여러 커밋 되돌리기
```

### 머지 충돌 해결

```bash
# 충돌 발생 시
git status  # 충돌 파일 확인

# 충돌 파일 편집 (<<<<<<< ======= >>>>>>> 마커 제거)

# 충돌 해결 후
git add conflicted-file.js
git commit  # 또는 git rebase --continue

# 머지 중단
git merge --abort
git rebase --abort

# 머지 도구 사용
git mergetool
```

### Stash 활용

```bash
# 작업 임시 저장
git stash
git stash save "WIP: 사용자 인증 작업 중"

# Stash 목록 확인
git stash list

# Stash 복원
git stash pop           # 적용 후 삭제
git stash apply         # 적용만 (보존)
git stash apply stash@{2}  # 특정 stash 적용

# Stash 삭제
git stash drop
git stash clear         # 모든 stash 삭제
```

### 실수한 파일 복구

```bash
# 작업 디렉토리 변경사항 취소
git checkout -- filename.js
git restore filename.js     # Git 2.23+

# Staging Area에서 제거
git reset HEAD filename.js
git restore --staged filename.js  # Git 2.23+

# 삭제된 파일 복구
git checkout HEAD~1 -- deleted-file.js

# 특정 커밋의 파일로 복구
git checkout abc1234 -- filename.js
```

---

## 🔀 GitHub Pull Request

### GitHub CLI 설치 및 설정

```bash
# GitHub CLI 설치
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# 인증
gh auth login

# 상태 확인
gh auth status
```

### Pull Request 기본 워크플로우

```bash
# 1. Feature 브랜치에서 작업 완료 후
git add .
git commit -m "feat: 새로운 기능 구현"
git push origin feature/new-feature

# 2. PR 생성
gh pr create --title "feat: 새로운 기능 구현" --body "상세 설명"

# 3. Draft PR로 생성 (아직 리뷰 준비 안됨)
gh pr create --draft --title "WIP: 새로운 기능 구현"

# 4. 리뷰어 지정하여 PR 생성
gh pr create --title "feat: 새로운 기능 구현" --reviewer "team-lead,colleague"

# 5. 라벨과 마일스톤 추가
gh pr create --title "feat: 새로운 기능 구현" --label "feature,backend" --milestone "v2.0.0"
```

### PR 관리 명령어

```bash
# PR 목록 확인
gh pr list                    # 열린 PR 목록
gh pr list --state all        # 모든 PR 목록
gh pr list --author "@me"     # 내가 작성한 PR

# PR 상세 정보 확인
gh pr view 123                # PR 번호로 확인
gh pr view feature/new-feature # 브랜치명으로 확인

# PR 상태 및 체크 확인
gh pr checks 123              # CI/CD 상태 확인
gh pr status                  # 현재 브랜치의 PR 상태

# PR 체크아웃 (다른 사람의 PR 로컬에서 테스트)
gh pr checkout 123

# PR 정보 수정
gh pr edit 123 --title "새로운 제목"
gh pr edit 123 --body "새로운 설명"
gh pr edit 123 --add-reviewer "new-reviewer"
```

### 코드 리뷰 및 승인

```bash
# PR에 코멘트 추가
gh pr comment 123 --body "훌륭한 구현입니다!"

# PR 리뷰 (승인)
gh pr review 123 --approve --body "LGTM! 코드 품질이 우수합니다."

# PR 리뷰 (변경 요청)
gh pr review 123 --request-changes --body "몇 가지 수정이 필요합니다."

# PR 리뷰 (일반 코멘트)
gh pr review 123 --comment --body "제안사항이 있습니다."

# 본인 PR을 ready 상태로 변경 (draft에서)
gh pr ready 123
```

### PR 머지 및 정리

```bash
# PR 머지 (squash merge 권장)
gh pr merge 123 --squash

# PR 머지 (merge commit)
gh pr merge 123 --merge

# PR 머지 (rebase)
gh pr merge 123 --rebase

# PR 머지 후 자동 삭제
gh pr merge 123 --squash --delete-branch

# PR 닫기 (머지하지 않고)
gh pr close 123
```

### PR과 Issue 연동

```bash
# 커밋 메시지에 Issue 번호 포함
git commit -m "feat: 사용자 인증 구현

Closes #123
Fixes #124
Related to #125"

# PR 설명에 Issue 연동
gh pr create --title "feat: 사용자 인증" --body "
이 PR은 사용자 인증 시스템을 구현합니다.

Closes #123
- JWT 토큰 기반 인증
- 로그인/로그아웃 API
- 권한 미들웨어
"
```

### PR 템플릿 활용

```bash
# .github/pull_request_template.md 파일 생성
mkdir -p .github
cat > .github/pull_request_template.md << 'EOF'
## 📋 변경사항 요약
<!-- 이 PR에서 변경한 내용을 간단히 설명해주세요 -->

## 🎯 변경 이유
<!-- 왜 이 변경이 필요한지 설명해주세요 -->

## 🧪 테스트 방법
<!-- 이 변경사항을 어떻게 테스트했는지 설명해주세요 -->
- [ ] 단위 테스트 통과
- [ ] 통합 테스트 통과
- [ ] 수동 테스트 완료

## 📋 체크리스트
- [ ] 코드 리뷰 준비 완료
- [ ] 테스트 추가/업데이트
- [ ] 문서 업데이트 (필요시)
EOF

# 템플릿 사용하여 PR 생성
gh pr create --title "feat: 새 기능" --body-file .github/pull_request_template.md
```

### 자동화 및 고급 활용

```bash
# GitHub Actions와 연동된 PR 상태 확인
gh pr checks --watch 123     # 실시간 상태 확인

# PR 병합 후 자동 정리 스크립트
cleanup_merged_prs() {
    # 머지된 브랜치 삭제
    git branch --merged main | grep -v main | xargs -n 1 git branch -d
    git remote prune origin
    
    # 로컬 브랜치 정리
    echo "머지된 브랜치들이 정리되었습니다."
}

# PR 생성과 동시에 팀에 슬랙 알림 (webhooks 설정 필요)
create_pr_with_notification() {
    local title="$1"
    local body="$2"
    
    local pr_url=$(gh pr create --title "$title" --body "$body")
    echo "PR이 생성되었습니다: $pr_url"
    
    # 슬랙 알림 (webhook URL 설정 필요)
    # curl -X POST -H 'Content-type: application/json' \
    #     --data "{\"text\":\"새 PR: $title - $pr_url\"}" \
    #     $SLACK_WEBHOOK_URL
}
```

---

## 🚀 고급 기법

### 태그 관리

```bash
# 태그 생성
git tag v1.0.0                    # Lightweight tag
git tag -a v1.0.0 -m "릴리스 v1.0.0"  # Annotated tag

# 태그 목록
git tag
git tag -l "v1.*"                 # 패턴 매칭

# 태그 푸시
git push origin v1.0.0            # 특정 태그
git push origin --tags            # 모든 태그

# 태그 삭제
git tag -d v1.0.0                 # 로컬 삭제
git push origin --delete v1.0.0   # 원격 삭제
```

### Cherry-pick

```bash
# 특정 커밋만 가져오기
git cherry-pick abc1234

# 여러 커밋 가져오기
git cherry-pick abc1234 def5678

# 충돌 발생 시
git cherry-pick --continue        # 해결 후 계속
git cherry-pick --abort           # 중단
```

### Bisect (버그 추적)

```bash
# 이진 탐색으로 버그 커밋 찾기
git bisect start
git bisect bad                    # 현재 커밋이 버그 있음
git bisect good v1.0.0           # 이 버전은 정상

# Git이 중간 커밋으로 이동, 테스트 후
git bisect good   # 또는 git bisect bad

# 버그 커밋 찾으면 종료
git bisect reset
```

### Worktree (멀티 브랜치 작업)

```bash
# 별도 디렉토리에서 다른 브랜치 작업
git worktree add ../feature-branch feature/new-feature
git worktree add ../hotfix hotfix/critical-bug

# Worktree 목록
git worktree list

# Worktree 제거
git worktree remove ../feature-branch
```

---

## ⚡ 성능 최적화

### 대용량 저장소 최적화

```bash
# 저장소 크기 확인
git count-objects -vH

# 가비지 컬렉션
git gc --aggressive --prune=now

# 리팩토링
git repack -ad

# 큰 파일 추적
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  awk '/^blob/ {print substr($0,6)}' | sort --numeric-sort --key=2 | tail -10
```

### Git 설정 최적화

```bash
# 성능 관련 설정
git config --global core.preloadindex true
git config --global core.fscache true
git config --global gc.auto 256

# 대용량 저장소용 설정
git config --global pack.threads 0
git config --global pack.deltaCacheSize 128m
git config --global pack.windowMemory 128m
```

### .gitignore 최적화

```bash
# 실무에서 자주 사용하는 .gitignore 패턴

# IDE & Editors
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Languages
## Java
target/
*.jar
*.war
*.class

## Go
vendor/
*.exe

## Node.js
node_modules/
npm-debug.log*

## Python
__pycache__/
*.pyc
venv/

# Build outputs
dist/
build/
out/

# Logs
*.log
logs/

# Environment
.env
.env.local
*.key
*.pem

# Database
*.db
*.sqlite
*.sqlite3

# Temporary
tmp/
temp/
*.tmp
```

---

## 🔗 통합 및 자동화

### Git Hooks 활용

```bash
# Pre-commit hook 예시 (.git/hooks/pre-commit)
#!/bin/sh
# 코드 포맷팅 체크
npm run lint
go fmt ./...
git diff --exit-code

# Commit-msg hook 예시 (.git/hooks/commit-msg)
#!/bin/sh
# Conventional Commits 검증
commit_regex='^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+'
if ! grep -qE "$commit_regex" "$1"; then
    echo "Invalid commit message format"
    exit 1
fi
```

### CI/CD와 연동

```yaml
# GitHub Actions 예시 (.github/workflows/ci.yml)
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # 전체 히스토리 가져오기
      
      - name: Run tests
        run: |
          git log --oneline -10
          make test
      
      - name: Check commit messages
        run: |
          npx commitlint --from origin/main --to HEAD
```

---

## 📋 Quick Reference

### 자주 사용하는 명령어 체크리스트

```bash
# 매일 사용
git status
git add .
git commit -m "message"
git push
git pull

# 브랜치 작업
git checkout -b feature/name
git merge main
git rebase main
git branch -d branch-name

# 문제 해결
git reset --soft HEAD~1
git stash
git stash pop
git diff

# 정보 확인
git log --oneline
git branch -a
git remote -v
git diff --staged
```

### 단축키 모음

```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
alias g='git'
alias ga='git add'
alias gc='git commit'
alias gco='git checkout'
alias gp='git push'
alias gl='git pull'
alias gs='git status'
alias gb='git branch'
alias gd='git diff'
alias glog='git log --oneline --graph'
```

---

**💡 실무 팁**: 
- 작은 단위로 자주 커밋하기
- 의미 있는 커밋 메시지 작성하기  
- 정기적으로 main 브랜치와 동기화하기
- 중요한 작업 전에는 백업하기
- 팀 컨벤션 준수하기

**🔗 관련 도구**: [GitHub CLI](https://cli.github.com/) | [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/) | [Conventional Commits](https://www.conventionalcommits.org/)