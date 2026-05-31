# Git Command Scripts

실무에서 자주 사용하는 Git 명령어들을 자동화한 Shell 스크립트 모음입니다. GitHub 없이도 효율적인 Git 워크플로우를 구성할 수 있도록 도와줍니다.

## 🚀 주요 기능

- **Git 초기 설정 자동화**: 리포지토리 생성부터 기본 설정까지
- **브랜치 관리**: Feature/Hotfix 브랜치 생성 및 관리
- **워크플로우 자동화**: 작업 완료부터 Push까지 원클릭
- **충돌 해결 지원**: 머지 충돌 상황 분석 및 해결 가이드
- **백업 및 복구**: 안전한 저장소 백업 시스템
- **GitHub API 연동**: GitHub CLI를 활용한 고급 기능

## 📖 Git CLI 기본 가이드

### 💡 핵심 문서
- **👉 [Git CLI 실무 가이드](docs/git-cli-guide.md)** - Git 명령어 기초부터 고급 기법까지
- **⚡ [Git 명령어 치트시트](examples/git-cheatsheet.md)** - 자주 사용하는 명령어 빠른 참조

### 📚 실무 예제
- **📅 [일일 워크플로우](examples/daily-workflow.md)** - 매일 사용하는 Git 패턴
- **👥 [팀 협업 시나리오](examples/team-scenarios.md)** - 실제 협업 상황별 해결책
- **🎯 [실습 가이드](examples/hands-on-practice.md)** - 단계별 실습으로 Git 마스터
- **🔀 [GitHub PR 가이드](examples/github-pr-guide.md)** - Pull Request 생성/관리/리뷰 완전 가이드

> 스크립트 없이 순수 Git 명령어를 사용한 워크플로우, 협업 시나리오, 문제 해결 방법을 상세히 설명합니다.

## 📋 스크립트 목록

### 1. git-setup.sh
Git 리포지토리 초기 설정을 자동화합니다.

```bash
# 기본 사용법
./scripts/git-setup.sh [repository-name] [remote-url]

# 예시
./scripts/git-setup.sh my-project https://github.com/username/my-project.git
```

**주요 기능:**
- Git 리포지토리 초기화
- 기본 브랜치를 main으로 설정
- .gitignore 파일 자동 생성
- Remote origin 설정

### 2. git-workflow.sh
일상적인 Git 워크플로우를 자동화합니다.

```bash
# Feature 브랜치 생성
./scripts/git-workflow.sh feature user-authentication

# 작업 완료 및 Push
./scripts/git-workflow.sh complete "feat: 사용자 인증 기능 구현"

# 브랜치 동기화
./scripts/git-workflow.sh sync

# 브랜치 삭제
./scripts/git-workflow.sh delete feature/user-authentication

# 상태 확인
./scripts/git-workflow.sh status
```

**주요 기능:**
- Feature/Hotfix 브랜치 자동 생성
- 브랜치 최신화 (rebase 기반)
- 작업 완료 후 자동 커밋 및 Push
- 브랜치 정리 (로컬 + 원격)
- 현재 상태 확인

### 3. git-utils.sh
고급 Git 작업을 위한 유틸리티 모음입니다.

```bash
# 저장소 백업
./scripts/git-utils.sh backup

# 커밋 히스토리 정리 (최근 5개)
./scripts/git-utils.sh clean 5

# 충돌 상황 분석
./scripts/git-utils.sh conflicts

# 브랜치 비교
./scripts/git-utils.sh compare main feature/new-feature

# 태그 관리
./scripts/git-utils.sh tag create v1.0.0 "첫 번째 릴리스"
./scripts/git-utils.sh tag list
./scripts/git-utils.sh tag delete v1.0.0

# 작업 임시 저장
./scripts/git-utils.sh stash save "진행 중인 작업"
./scripts/git-utils.sh stash list
./scripts/git-utils.sh stash pop
```

**주요 기능:**
- Git 번들 기반 전체 백업
- Interactive rebase를 통한 커밋 정리
- 머지 충돌 분석 및 해결 가이드
- 브랜치 간 차이점 비교
- 태그 생성/삭제/관리
- 작업 임시 저장 (stash) 관리

### 4. github-api.sh
GitHub CLI를 활용한 고급 GitHub 기능입니다.

```bash
# Pull Request 생성
./scripts/github-api.sh pr "새로운 기능 추가" "상세 설명" main false

# Pull Request 관리
./scripts/github-api.sh pr-list                    # PR 목록 조회
./scripts/github-api.sh pr-status 123              # PR 상태 확인
./scripts/github-api.sh pr-merge 123 squash        # PR 머지

# Issue 생성
./scripts/github-api.sh issue "버그 수정" "버그 내용" "bug,high-priority" "username"

# 저장소 통계
./scripts/github-api.sh stats

# Release 생성
./scripts/github-api.sh release v1.0.0 "첫 번째 릴리스" "주요 변경사항"

# GitHub Actions 상태 확인
./scripts/github-api.sh workflows

# 새 저장소 생성 및 설정
./scripts/github-api.sh setup my-new-repo "프로젝트 설명" false
```

**사전 요구사항:**
- GitHub CLI 설치: `brew install gh` (macOS) 또는 `apt install gh` (Ubuntu)
- GitHub 인증: `gh auth login`

## 🛠️ 설치 및 설정

### 1. 스크립트 실행 권한 부여

```bash
chmod +x scripts/*.sh
```

### 2. PATH 추가 (선택사항)

```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
export PATH="$PATH:$(pwd)/scripts"

# 그 후 reload
source ~/.bashrc  # 또는 source ~/.zshrc
```

### 3. Alias 설정 (권장)

```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
alias gs='./scripts/git-setup.sh'
alias gw='./scripts/git-workflow.sh'
alias gu='./scripts/git-utils.sh'
alias gh-api='./scripts/github-api.sh'
```

## 📚 사용 시나리오

### 새 프로젝트 시작

```bash
# 1. 프로젝트 초기 설정
./scripts/git-setup.sh my-project https://github.com/username/my-project.git

# 2. 초기 커밋
git add .
git commit -m "Initial commit"
git push -u origin main
```

### Feature 개발 워크플로우

```bash
# 1. Feature 브랜치 생성
./scripts/git-workflow.sh feature user-login

# 2. 개발 작업 수행...

# 3. 작업 완료 및 Push
./scripts/git-workflow.sh complete "feat: 사용자 로그인 기능 구현"

# 4. GitHub에서 Pull Request 생성 또는 GitHub CLI 사용
gh pr create --title "feat: 사용자 로그인 기능 구현" --body "상세 설명..."

# 5. 머지 후 브랜치 정리
./scripts/git-workflow.sh delete feature/user-login
```

### 팀 협업 시나리오

```bash
# 1. 최신 변경사항 동기화
./scripts/git-workflow.sh sync

# 2. 충돌 발생 시 분석
./scripts/git-utils.sh conflicts

# 3. 브랜치 상태 확인
./scripts/git-workflow.sh status

# 4. 백업 생성 (중요한 작업 전)
./scripts/git-utils.sh backup
```

## ⚡ 성능 최적화 팁

1. **브랜치 전략**: GitFlow 대신 GitHub Flow 사용으로 단순화
2. **커밋 메시지**: Conventional Commits 규칙 적용
3. **백업 전략**: 주기적 자동 백업 스케줄링
4. **충돌 최소화**: 자주 sync하여 브랜치 최신화

## 🔒 보안 고려사항

- GitHub Personal Access Token 사용 시 환경변수 설정
- 민감한 정보는 .env 파일로 분리
- 백업 파일의 안전한 저장소 관리

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`./scripts/git-workflow.sh feature amazing-feature`)
3. Commit your Changes (`./scripts/git-workflow.sh complete "feat: Add some amazing feature"`)
4. Push to the Branch
5. Open a Pull Request

## 📝 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📞 지원

- **Issues**: 버그 리포트나 기능 요청
- **Discussions**: 사용법 문의나 아이디어 공유
- **Wiki**: 상세한 사용 가이드 및 FAQ

---

**💡 Pro Tip**: 각 스크립트는 `help` 옵션을 지원합니다. 예: `./scripts/git-workflow.sh help`

## 🔗 관련 도구

- [GitHub CLI](https://cli.github.com/)
- [Git](https://git-scm.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitFlow](https://nvie.com/posts/a-successful-git-branching-model/)