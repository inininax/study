# GitHub Pull Request 완전 가이드

> GitHub CLI와 Git을 활용한 Pull Request 생성, 관리, 리뷰 전략

## 📚 목차

1. [PR 기본 개념](#-pr-기본-개념)
2. [GitHub CLI 설정](#️-github-cli-설정)
3. [PR 생성 워크플로우](#-pr-생성-워크플로우)
4. [PR 관리 및 업데이트](#-pr-관리-및-업데이트)
5. [코드 리뷰 프로세스](#-코드-리뷰-프로세스)
6. [PR 자동화](#-pr-자동화)
7. [고급 PR 기법](#-고급-pr-기법)
8. [팀 협업 전략](#-팀-협업-전략)

---

## 🎯 PR 기본 개념

### Pull Request란?

Pull Request(PR)는 코드 변경사항을 메인 브랜치에 병합하기 전에 팀원들이 검토할 수 있도록 하는 GitHub의 협업 도구입니다.

```bash
# PR의 일반적인 플로우
feature branch → PR 생성 → 코드 리뷰 → 승인 → 병합 → 브랜치 삭제
```

### PR vs 직접 Push 비교

| PR 사용 | 직접 Push |
|---------|-----------|
| ✅ 코드 리뷰 가능 | ❌ 리뷰 없이 반영 |
| ✅ 품질 관리 | ⚠️ 품질 보장 어려움 |
| ✅ 팀 지식 공유 | ❌ 개별 작업 |
| ✅ CI/CD 검증 | ⚠️ 사후 확인 |
| ✅ 히스토리 추적 | ⚠️ 추적 제한적 |

---

## ⚙️ GitHub CLI 설정

### GitHub CLI 설치

```bash
# macOS
brew install gh

# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh

# Windows (with winget)
winget install GitHub.cli
```

### GitHub 인증

```bash
# 브라우저를 통한 인증
gh auth login

# Personal Access Token으로 인증
gh auth login --with-token < your-token.txt

# 인증 상태 확인
gh auth status

# 현재 사용자 정보 확인
gh api user --jq '.login, .name, .email'
```

### 기본 설정

```bash
# 기본 에디터 설정
gh config set editor "code --wait"

# 기본 프로토콜 설정 (HTTPS 권장)
gh config set git_protocol https

# 현재 설정 확인
gh config list
```

---

## 🚀 PR 생성 워크플로우

### 1. Feature 브랜치 생성

```bash
# main 브랜치에서 시작
git checkout main
git pull origin main

# feature 브랜치 생성
git checkout -b feature/user-authentication

# 또는 스크립트 사용
./scripts/git-workflow.sh feature user-authentication
```

### 2. 개발 및 커밋

```bash
# 개발 작업 수행...

# 변경사항 확인
git status
git diff

# 의미있는 단위로 커밋
git add src/auth/
git commit -m "feat(auth): JWT 토큰 기반 사용자 인증 구현

- JWT 토큰 생성 및 검증 로직 추가
- 사용자 로그인/로그아웃 엔드포인트 구현
- 인증 미들웨어 추가
- 단위 테스트 작성

Closes #123"
```

### 3. 브랜치 푸시

```bash
# 첫 번째 푸시
git push -u origin feature/user-authentication

# 이후 푸시
git push origin feature/user-authentication

# 또는 스크립트 사용
./scripts/git-workflow.sh complete "feat(auth): 사용자 인증 구현"
```

### 4. PR 생성 (GitHub CLI)

```bash
# 기본 PR 생성
gh pr create --title "feat: 사용자 인증 시스템 구현" --body "상세 설명..."

# 템플릿을 사용한 PR 생성
gh pr create --title "feat: 사용자 인증 시스템 구현" --body-file .github/pull_request_template.md

# Draft PR 생성
gh pr create --draft --title "WIP: 사용자 인증 시스템 구현"

# 특정 리뷰어 지정
gh pr create --title "feat: 사용자 인증 시스템 구현" --reviewer "team-lead,senior-dev"

# 라벨 및 마일스톤 지정
gh pr create --title "feat: 사용자 인증 시스템 구현" --label "feature,backend" --milestone "v2.0.0"
```

### 5. PR 템플릿 활용

```markdown
<!-- .github/pull_request_template.md -->
## 📋 변경사항 요약

<!-- 이 PR에서 변경한 내용을 간단히 설명해주세요 -->

## 🎯 변경 이유

<!-- 왜 이 변경이 필요한지 설명해주세요 -->
- Closes #이슈번호

## 🧪 테스트 방법

<!-- 이 변경사항을 어떻게 테스트했는지 설명해주세요 -->
- [ ] 단위 테스트 통과
- [ ] 통합 테스트 통과
- [ ] 수동 테스트 완료

## 📸 스크린샷 (UI 변경 시)

<!-- UI 변경이 있다면 스크린샷을 첨부해주세요 -->

## ✅ 체크리스트

- [ ] 코드가 프로젝트 스타일 가이드를 따름
- [ ] 새로운 코드에 대한 테스트 추가됨
- [ ] 기존 테스트가 모두 통과함
- [ ] 문서가 업데이트됨 (필요한 경우)
- [ ] CHANGELOG.md가 업데이트됨 (필요한 경우)

## 📝 추가 정보

<!-- 리뷰어가 알아야 할 추가 정보가 있다면 작성해주세요 -->
```

---

## 📊 PR 관리 및 업데이트

### PR 상태 확인

```bash
# 현재 리포지토리의 PR 목록
gh pr list

# 내가 생성한 PR 목록
gh pr list --author "@me"

# 특정 상태의 PR 목록
gh pr list --state open
gh pr list --state closed
gh pr list --state merged

# 특정 PR 상세 정보
gh pr view 123
gh pr view feature/user-authentication

# PR 상태 확인 (CI/CD 포함)
gh pr checks 123
```

### PR 업데이트

```bash
# 추가 커밋 후 업데이트
git add .
git commit -m "fix: 리뷰 피드백 반영"
git push origin feature/user-authentication

# PR 정보 수정
gh pr edit 123 --title "새로운 제목"
gh pr edit 123 --body "새로운 설명"
gh pr edit 123 --add-reviewer "new-reviewer"
gh pr edit 123 --add-label "priority-high"

# Draft 상태 변경
gh pr ready 123  # Draft → Open
gh pr convert-to-draft 123  # Open → Draft
```

### Force Push 시 주의사항

```bash
# 안전한 force push (다른 사람이 수정하지 않았을 때만)
git push --force-with-lease origin feature/user-authentication

# 위험한 force push (절대 사용하지 말 것)
# git push --force origin feature/user-authentication

# Interactive rebase 후 force push 예시
git rebase -i HEAD~3
git push --force-with-lease origin feature/user-authentication
```

---

## 👥 코드 리뷰 프로세스

### 리뷰어 관점

```bash
# PR 체크아웃하여 로컬에서 테스트
gh pr checkout 123

# 변경사항 확인
git diff main..feature/user-authentication
git log main..feature/user-authentication --oneline

# 테스트 실행
npm test  # 또는 프로젝트에 맞는 테스트 명령어
go test ./...
```

### 리뷰 코멘트 작성

```bash
# PR에 일반 코멘트 추가
gh pr comment 123 --body "전반적으로 좋은 구현입니다!"

# 특정 라인에 코멘트 (GitHub 웹에서 권장)
# 파일의 특정 라인에 대한 리뷰 코멘트는 웹 인터페이스에서 작성

# 리뷰 승인
gh pr review 123 --approve --body "LGTM! 코드 품질이 우수합니다."

# 변경 요청
gh pr review 123 --request-changes --body "몇 가지 수정이 필요합니다."

# 일반 리뷰 (승인/거부 없이)
gh pr review 123 --comment --body "몇 가지 제안사항이 있습니다."
```

### 작성자의 리뷰 반영

```bash
# 피드백 반영 후 커밋
git add .
git commit -m "refactor: 코드 리뷰 피드백 반영

- 변수명을 더 명확하게 수정
- 에러 핸들링 로직 개선
- 중복 코드 제거
- 테스트 케이스 추가"

git push origin feature/user-authentication

# 리뷰어에게 응답
gh pr comment 123 --body "피드백 주신 내용 모두 반영했습니다. 다시 확인 부탁드립니다!"
```

---

## 🤖 PR 자동화

### GitHub Actions와 PR 연동

```yaml
# .github/workflows/pr-checks.yml
name: PR Checks

on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Run linting
        run: npm run lint
      
      - name: Check code coverage
        run: npm run test:coverage

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run security audit
        run: npm audit --audit-level high

  auto-approve:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'
    steps:
      - name: Auto-approve dependabot PRs
        run: gh pr review ${{ github.event.pull_request.number }} --approve
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 자동 라벨링

```yaml
# .github/workflows/label-pr.yml
name: Label PRs

on:
  pull_request:
    types: [opened]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Label based on files changed
        uses: actions/labeler@v4
        with:
          repo-token: "${{ secrets.GITHUB_TOKEN }}"
```

```yaml
# .github/labeler.yml
'backend':
  - 'src/api/**/*'
  - 'src/services/**/*'

'frontend':
  - 'src/components/**/*'
  - 'src/pages/**/*'

'documentation':
  - 'docs/**/*'
  - '*.md'

'tests':
  - 'tests/**/*'
  - '**/*.test.*'
```

### PR 자동 생성 스크립트

```bash
#!/bin/bash
# scripts/create-pr.sh

set -e

BRANCH=$(git branch --show-current)
TITLE="$1"
BODY="$2"

if [ "$BRANCH" = "main" ]; then
    echo "❌ main 브랜치에서는 PR을 생성할 수 없습니다"
    exit 1
fi

# 최신 상태로 업데이트
git fetch origin
git rebase origin/main

# 푸시
git push -u origin "$BRANCH"

# PR 생성
gh pr create \
    --title "$TITLE" \
    --body "$BODY" \
    --reviewer "team-lead" \
    --label "needs-review" \
    --draft

echo "✅ Draft PR이 생성되었습니다"
echo "준비가 되면 'gh pr ready'로 리뷰 요청하세요"
```

---

## 🔄 고급 PR 기법

### 대규모 PR 분할 전략

```bash
# 큰 기능을 여러 PR로 분할
git checkout -b feature/user-auth-base
# 기본 구조만 구현
git commit -m "feat: 사용자 인증 기본 구조"
gh pr create --title "feat: 사용자 인증 기본 구조" --base main

# 첫 번째 PR이 머지된 후
git checkout main && git pull origin main
git checkout -b feature/user-auth-jwt
# JWT 로직 구현
git commit -m "feat: JWT 토큰 처리 로직"
gh pr create --title "feat: JWT 토큰 처리 로직" --base main

# 두 번째 PR이 머지된 후
git checkout main && git pull origin main
git checkout -b feature/user-auth-middleware
# 미들웨어 구현
git commit -m "feat: 인증 미들웨어"
gh pr create --title "feat: 인증 미들웨어" --base main
```

### Stack PR (의존적 PR) 관리

```bash
# 기본 PR
git checkout -b feature/base-structure
# ... 개발 ...
git push -u origin feature/base-structure
gh pr create --title "feat: 기본 구조" --base main

# 의존적 PR (첫 번째 PR 위에 구축)
git checkout -b feature/advanced-logic
# ... 개발 ...
git push -u origin feature/advanced-logic
gh pr create --title "feat: 고급 로직" --base feature/base-structure

# 첫 번째 PR이 머지된 후, 두 번째 PR의 base 변경
gh pr edit feature/advanced-logic --base main
```

### Fixup Commits 활용

```bash
# 리뷰 피드백을 fixup 커밋으로 처리
git add .
git commit --fixup=abc1234  # 수정하려는 원본 커밋 ID

# Interactive rebase로 fixup 자동 적용
git rebase -i --autosquash HEAD~5

# Force push
git push --force-with-lease origin feature/user-authentication
```

---

## 🏢 팀 협업 전략

### PR 템플릿 전략

```markdown
<!-- .github/pull_request_template.md -->
## 📋 PR 타입
- [ ] 🚀 새로운 기능 (feature)
- [ ] 🐛 버그 수정 (bugfix)
- [ ] 📚 문서 업데이트 (docs)
- [ ] 🎨 코드 스타일 변경 (style)
- [ ] ♻️ 리팩토링 (refactor)
- [ ] ⚡ 성능 개선 (performance)
- [ ] ✅ 테스트 추가 (test)
- [ ] 🔧 빌드/설정 변경 (chore)

## 🎯 변경사항
<!-- 무엇을 변경했는지 간단히 설명 -->

## 🤔 변경 이유
<!-- 왜 이 변경이 필요한지 설명 -->

## 🧪 테스트
- [ ] 기존 테스트 통과
- [ ] 새로운 테스트 추가
- [ ] 수동 테스트 완료

## 📋 리뷰 가이드
<!-- 리뷰어가 특별히 확인해야 할 부분 -->

## 🚀 배포 영향도
- [ ] Breaking Changes 없음
- [ ] 데이터베이스 마이그레이션 필요
- [ ] 환경 변수 추가/수정 필요
- [ ] 의존성 업데이트 필요

## 📸 스크린샷 (해당하는 경우)
<!-- UI 변경이 있다면 Before/After 스크린샷 -->
```

### Branch Protection Rules

```bash
# GitHub CLI로 브랜치 보호 규칙 설정은 웹에서 하는 것이 더 편리하지만,
# API를 통해서도 가능합니다

# 현재 보호 규칙 확인
gh api repos/:owner/:repo/branches/main/protection

# 웹에서 설정 권장:
# Settings > Branches > Add rule
# - Require pull request reviews before merging
# - Require status checks to pass before merging
# - Require branches to be up to date before merging
# - Require conversation resolution before merging
# - Include administrators
```

### 팀 PR 리뷰 가이드라인

```markdown
## 🔍 코드 리뷰 체크리스트

### 기능적 검토
- [ ] 요구사항을 정확히 구현했는가?
- [ ] 엣지 케이스가 고려되었는가?
- [ ] 에러 핸들링이 적절한가?

### 코드 품질
- [ ] 코드가 읽기 쉽고 이해하기 쉬운가?
- [ ] 함수와 변수명이 명확한가?
- [ ] 중복 코드가 없는가?
- [ ] 적절한 주석이 있는가?

### 성능 및 보안
- [ ] 성능상 문제가 없는가?
- [ ] 보안 취약점이 없는가?
- [ ] 메모리 누수 가능성은 없는가?

### 테스트
- [ ] 충분한 테스트 커버리지를 가지는가?
- [ ] 테스트가 의미있고 신뢰할 수 있는가?

### 문서화
- [ ] 필요한 문서가 업데이트되었는가?
- [ ] API 변경사항이 문서화되었는가?
```

---

## 🔧 PR 관련 스크립트 및 도구

### 유용한 Git Aliases

```bash
# ~/.gitconfig에 추가
[alias]
    # PR 관련 aliases
    pr-create = "!f() { gh pr create --title \"$1\" --body \"$2\"; }; f"
    pr-list = "!gh pr list"
    pr-checkout = "!f() { gh pr checkout $1; }; f"
    pr-merge = "!f() { gh pr merge $1 --squash; }; f"
    
    # 유용한 정보 aliases
    pr-diff = "!f() { git diff main..$(git branch --show-current); }; f"
    pr-log = "!f() { git log main..$(git branch --show-current) --oneline; }; f"
    pr-stats = "!f() { git diff --stat main..$(git branch --show-current); }; f"
```

### Shell 함수

```bash
# ~/.bashrc 또는 ~/.zshrc에 추가

# PR 생성 헬퍼
pr() {
    local title="$1"
    local body="$2"
    
    if [ -z "$title" ]; then
        echo "Usage: pr \"Title\" \"Body\""
        return 1
    fi
    
    # 현재 브랜치 확인
    local branch=$(git branch --show-current)
    if [ "$branch" = "main" ]; then
        echo "Cannot create PR from main branch"
        return 1
    fi
    
    # 푸시 및 PR 생성
    git push -u origin "$branch"
    gh pr create --title "$title" --body "$body" --draft
    
    echo "Draft PR created. Use 'gh pr ready' when ready for review."
}

# PR 상태 확인
pr-status() {
    local pr_number="$1"
    if [ -z "$pr_number" ]; then
        gh pr list --author "@me"
    else
        gh pr view "$pr_number"
        gh pr checks "$pr_number"
    fi
}

# PR 정리 (머지된 브랜치 삭제)
pr-cleanup() {
    git branch --merged main | grep -v main | xargs -n 1 git branch -d
    git remote prune origin
    echo "Cleaned up merged branches"
}
```

---

## 📊 PR 메트릭스 및 분석

### PR 통계 확인

```bash
# 리포지토리 PR 통계
gh api repos/:owner/:repo/pulls --paginate | jq '
    group_by(.state) | 
    map({state: .[0].state, count: length}) | 
    sort_by(.state)'

# 내 PR 통계
gh pr list --author "@me" --state all --json number,title,state,createdAt | jq '
    group_by(.state) | 
    map({state: .[0].state, count: length})'

# 최근 한 달 PR 활동
gh pr list --state all --json number,title,state,createdAt,closedAt | jq '
    [.[] | select(.createdAt > (now - 30*24*3600 | strftime("%Y-%m-%dT%H:%M:%SZ")))] | 
    length'
```

### 리뷰 성능 분석

```bash
# 평균 리뷰 시간 계산 (복잡한 쿼리이므로 웹 도구 사용 권장)
# GitHub Insights나 외부 도구 활용

# 가장 활발한 리뷰어 확인
gh api repos/:owner/:repo/pulls/comments --paginate | jq '
    group_by(.user.login) | 
    map({reviewer: .[0].user.login, comments: length}) | 
    sort_by(.comments) | reverse'
```

---

## 💡 Pro Tips

### 1. PR 크기 관리
```bash
# PR이 너무 클 때 - 라인 수 확인
git diff --stat main..HEAD

# 권장: 한 PR당 200-400 라인 이내
# 1000 라인 이상이면 분할 고려
```

### 2. 커밋 메시지 품질
```bash
# 좋은 커밋 메시지 예시
git commit -m "feat(auth): implement JWT token authentication

- Add JWT token generation and validation
- Implement login/logout endpoints  
- Add authentication middleware
- Include comprehensive unit tests

Closes #123
Breaking Change: Auth header format changed"
```

### 3. CI/CD 최적화
```bash
# PR에서만 특정 테스트 실행
if [ "$GITHUB_EVENT_NAME" = "pull_request" ]; then
    npm run test:integration
fi
```

### 4. 자동화 도구 활용
- **Dependabot**: 의존성 업데이트 자동 PR
- **CodeQL**: 보안 스캔 자동화
- **Auto-merge**: 조건 만족 시 자동 머지
- **PR Size Labeler**: PR 크기별 라벨 자동 추가

---

이 가이드를 통해 GitHub PR을 효율적으로 활용하여 팀 협업 품질을 높이고 코드 리뷰 문화를 개선할 수 있습니다. 각 팀의 상황에 맞게 워크플로우를 조정하여 사용하세요!

**🔗 관련 도구**: [GitHub CLI](https://cli.github.com/) | [GitHub Desktop](https://desktop.github.com/) | [Conventional Commits](https://www.conventionalcommits.org/)