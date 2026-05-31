# Git CLI 치트시트

> 실무에서 자주 사용하는 Git 명령어 빠른 참조

## 📋 기본 명령어

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `git init` | 저장소 초기화 | `git init my-project` |
| `git clone` | 저장소 복제 | `git clone https://github.com/user/repo.git` |
| `git status` | 상태 확인 | `git status -s` |
| `git add` | 파일 추가 | `git add .` |
| `git commit` | 커밋 생성 | `git commit -m "message"` |
| `git push` | 원격에 푸시 | `git push origin main` |
| `git pull` | 원격에서 가져오기 | `git pull origin main` |
| `git fetch` | 원격 정보만 가져오기 | `git fetch origin` |

## 🌿 브랜치 관리

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `git branch` | 브랜치 목록 | `git branch -a` |
| `git checkout` | 브랜치 전환 | `git checkout feature/auth` |
| `git switch` | 브랜치 전환 (신규) | `git switch feature/auth` |
| `git checkout -b` | 브랜치 생성+전환 | `git checkout -b feature/auth` |
| `git merge` | 브랜치 머지 | `git merge feature/auth` |
| `git rebase` | 리베이스 | `git rebase main` |
| `git branch -d` | 브랜치 삭제 | `git branch -d feature/auth` |

## 📝 로그 및 히스토리

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `git log` | 커밋 히스토리 | `git log --oneline` |
| `git show` | 커밋 상세보기 | `git show abc1234` |
| `git diff` | 차이점 확인 | `git diff HEAD~1` |
| `git blame` | 라인별 작성자 | `git blame filename.js` |
| `git shortlog` | 작성자별 요약 | `git shortlog -sn` |

## 🔄 변경사항 관리

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `git reset` | 커밋 취소 | `git reset --soft HEAD~1` |
| `git revert` | 커밋 되돌리기 | `git revert HEAD` |
| `git stash` | 임시 저장 | `git stash save "message"` |
| `git cherry-pick` | 특정 커밋 가져오기 | `git cherry-pick abc1234` |
| `git clean` | 추적안된 파일 삭제 | `git clean -fd` |

## 🔗 원격 저장소

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `git remote` | 원격 저장소 목록 | `git remote -v` |
| `git remote add` | 원격 저장소 추가 | `git remote add origin [url]` |
| `git push -u` | 업스트림 설정하며 푸시 | `git push -u origin main` |
| `git push --force-with-lease` | 안전한 강제 푸시 | `git push --force-with-lease` |

## 🏷️ 태그 관리

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `git tag` | 태그 목록 | `git tag -l "v1.*"` |
| `git tag -a` | 주석 태그 생성 | `git tag -a v1.0.0 -m "Release"` |
| `git push --tags` | 태그 푸시 | `git push origin --tags` |
| `git tag -d` | 태그 삭제 | `git tag -d v1.0.0` |

## 🔍 검색 및 찾기

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `git grep` | 내용 검색 | `git grep "function"` |
| `git log -S` | 코드 검색 | `git log -S "function_name"` |
| `git log --grep` | 커밋 메시지 검색 | `git log --grep="fix"` |
| `git bisect` | 이진 탐색 | `git bisect start` |

## ⚙️ 설정 관리

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `git config` | 설정 보기/변경 | `git config user.name` |
| `git config --global` | 전역 설정 | `git config --global user.email` |
| `git config --list` | 모든 설정 보기 | `git config --list --show-origin` |

## 🚨 응급 처치

### 실수한 커밋 되돌리기
```bash
git reset --soft HEAD~1    # 커밋만 취소, 파일은 유지
git reset --mixed HEAD~1   # 커밋+스테이징 취소, 파일은 유지
git reset --hard HEAD~1    # 모든 변경사항 취소
```

### 잘못된 브랜치에 커밋한 경우
```bash
git log --oneline -1       # 커밋 ID 확인
git reset --hard HEAD~1    # 현재 브랜치에서 커밋 제거
git checkout correct-branch # 올바른 브랜치로 이동
git cherry-pick abc1234    # 커밋 가져오기
```

### 머지 충돌 해결
```bash
git status                 # 충돌 파일 확인
# 파일 편집하여 충돌 해결
git add resolved-file.js   # 해결된 파일 추가
git commit                 # 머지 커밋 생성
```

### 실수로 삭제한 브랜치 복구
```bash
git reflog                 # 최근 작업 기록 확인
git checkout -b recovered-branch abc1234  # 삭제된 브랜치 복구
```

## 🎯 자주 사용하는 조합

### 새 기능 개발 시작
```bash
git checkout main && git pull origin main
git checkout -b feature/new-feature
```

### 작업 완료 후 푸시
```bash
git add . && git commit -m "feat: 새 기능 구현"
git push origin feature/new-feature
```

### 브랜치 최신화
```bash
git checkout main && git pull origin main
git checkout feature/my-feature && git rebase main
```

### 커밋 정리하기
```bash
git rebase -i HEAD~3  # 최근 3개 커밋 정리
git push --force-with-lease origin feature/my-feature
```

## 🔧 유용한 Alias

```bash
# ~/.gitconfig에 추가
[alias]
  st = status
  co = checkout
  br = branch
  ci = commit
  ca = commit -a
  cp = cherry-pick
  df = diff
  lg = log --graph --oneline --decorate --all
  unstage = reset HEAD --
  last = log -1 HEAD
  undo = reset --soft HEAD~1
  recommit = commit --amend --no-edit
  pushf = push --force-with-lease
  sync = !git checkout main && git pull origin main
```

## 📊 상태 확인 명령어

```bash
# 현재 상태 요약
git status -sb

# 브랜치 구조 시각화
git log --graph --oneline --all

# 최근 활동 확인
git reflog --oneline -10

# 원격 브랜치와 차이점
git log origin/main..HEAD --oneline

# 변경된 파일 목록
git diff --name-only

# 스테이징된 변경사항
git diff --cached
```

## 💡 Pro Tips

1. **커밋 전 항상 확인**: `git diff --cached`
2. **안전한 강제 푸시**: `git push --force-with-lease`
3. **작업 임시 저장**: `git stash save "의미있는 메시지"`
4. **브랜치 정리**: `git branch --merged | grep -v main | xargs git branch -d`
5. **원격 브랜치 정리**: `git remote prune origin`

이 치트시트를 북마크해두고 필요할 때마다 참고하세요!