# Git CLI 실습 가이드

> 단계별 실습을 통해 Git CLI 사용법을 익혀보세요

## 🎯 실습 목표

이 실습을 통해 다음을 익힐 수 있습니다:
- Git 기본 워크플로우 
- 브랜치 생성 및 관리
- 충돌 해결
- 팀 협업 시나리오

## 📋 사전 준비

```bash
# 1. Git 버전 확인
git --version

# 2. 사용자 정보 설정 (아직 안했다면)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 3. 실습용 디렉토리 생성
mkdir git-practice
cd git-practice
```

## 🚀 실습 1: 기본 워크플로우

### 1.1 저장소 초기화

```bash
# Git 저장소 초기화
git init

# 현재 상태 확인
git status

# 예상 결과: "On branch main, No commits yet"
```

### 1.2 첫 번째 파일 추가

```bash
# README 파일 생성
echo "# Git Practice Project" > README.md
echo "This is a practice project for learning Git CLI." >> README.md

# 파일 상태 확인
git status

# 파일을 staging area에 추가
git add README.md

# 다시 상태 확인
git status

# 첫 번째 커밋
git commit -m "Initial commit: Add README.md"

# 커밋 히스토리 확인
git log --oneline
```

### 1.3 파일 수정 및 추가 커밋

```bash
# 새 파일 생성
echo "console.log('Hello, Git!');" > main.js

# README 파일 수정
echo "## Features" >> README.md
echo "- Git basic workflow practice" >> README.md

# 변경사항 확인
git status
git diff

# 모든 변경사항 추가 및 커밋
git add .
git commit -m "Add main.js and update README"

# 히스토리 확인
git log --oneline --graph
```

## 🌿 실습 2: 브랜치 관리

### 2.1 Feature 브랜치 생성

```bash
# 새 브랜치 생성 및 전환
git checkout -b feature/add-functions

# 브랜치 목록 확인
git branch

# 새 함수 파일 생성
cat > functions.js << 'EOF'
// Utility functions
function add(a, b) {
    return a + b;
}

function multiply(a, b) {
    return a * b;
}

module.exports = { add, multiply };
EOF

# 변경사항 커밋
git add functions.js
git commit -m "feat: Add utility functions"
```

### 2.2 main 브랜치에서 추가 작업

```bash
# main 브랜치로 전환
git checkout main

# 다른 파일 추가 (충돌을 위한 준비)
cat > config.js << 'EOF'
// Configuration settings
const config = {
    version: '1.0.0',
    debug: true
};

module.exports = config;
EOF

git add config.js
git commit -m "Add configuration file"

# 히스토리 확인 (브랜치 분화 확인)
git log --graph --oneline --all
```

### 2.3 브랜치 병합

```bash
# feature 브랜치를 main으로 병합
git merge feature/add-functions

# 병합 후 히스토리 확인
git log --graph --oneline

# 사용 완료된 브랜치 삭제
git branch -d feature/add-functions
```

## ⚔️ 실습 3: 충돌 해결

### 3.1 충돌 상황 만들기

```bash
# 첫 번째 브랜치 생성
git checkout -b feature/update-readme-1

# README 파일 수정
cat > README.md << 'EOF'
# Git Practice Project
This is a practice project for learning Git CLI.

## Features
- Git basic workflow practice
- Branch management
- Conflict resolution practice

## Version
1.0.0
EOF

git add README.md
git commit -m "Update README with version info"

# main으로 돌아가서 두 번째 브랜치 생성
git checkout main
git checkout -b feature/update-readme-2

# 같은 파일을 다르게 수정
cat > README.md << 'EOF'
# Git Practice Project
This is a practice project for learning Git CLI.

## Features
- Git basic workflow practice
- Branch management
- Team collaboration

## Author
Your Name
EOF

git add README.md
git commit -m "Update README with author info"
```

### 3.2 충돌 발생시키기

```bash
# main 브랜치로 이동하여 첫 번째 브랜치 병합
git checkout main
git merge feature/update-readme-1

# 두 번째 브랜치 병합 시도 (충돌 발생!)
git merge feature/update-readme-2

# 충돌 상태 확인
git status
```

### 3.3 충돌 해결하기

```bash
# 충돌 파일 내용 확인
cat README.md

# 충돌 마커 제거하고 수동으로 병합
cat > README.md << 'EOF'
# Git Practice Project
This is a practice project for learning Git CLI.

## Features
- Git basic workflow practice
- Branch management
- Conflict resolution practice
- Team collaboration

## Version
1.0.0

## Author
Your Name
EOF

# 해결된 파일 추가
git add README.md

# 병합 커밋 완료
git commit -m "Merge feature/update-readme-2 with conflict resolution"

# 결과 확인
git log --graph --oneline

# 브랜치 정리
git branch -d feature/update-readme-1
git branch -d feature/update-readme-2
```

## 🔄 실습 4: 고급 기능

### 4.1 Stash 활용

```bash
# 새 작업 시작
git checkout -b feature/add-tests

# 파일 수정 중...
echo "// TODO: Add tests" > tests.js

# 급한 일이 생겨서 작업 임시 저장
git stash save "WIP: Adding test file"

# main 브랜치에서 급한 수정
git checkout main
echo "// Hotfix applied" >> main.js
git add main.js
git commit -m "hotfix: Apply urgent fix"

# 원래 작업으로 복귀
git checkout feature/add-tests
git stash pop

# 작업 완료
cat > tests.js << 'EOF'
// Test file for utility functions
const { add, multiply } = require('./functions');

function testAdd() {
    console.assert(add(2, 3) === 5, 'Add function test failed');
    console.log('Add function test passed');
}

function testMultiply() {
    console.assert(multiply(2, 3) === 6, 'Multiply function test failed');
    console.log('Multiply function test passed');
}

testAdd();
testMultiply();
EOF

git add tests.js
git commit -m "feat: Add test functions"
```

### 4.2 Interactive Rebase

```bash
# 커밋 히스토리 정리하기 위해 여러 작은 커밋 만들기
echo "// Documentation" >> functions.js
git add functions.js
git commit -m "Add documentation comment"

echo "// More documentation" >> functions.js
git add functions.js
git commit -m "Add more documentation"

echo "// Final documentation" >> functions.js
git add functions.js
git commit -m "Add final documentation"

# 최근 3개 커밋 정리
git rebase -i HEAD~3

# interactive 모드에서:
# - 첫 번째 커밋은 pick
# - 나머지는 squash로 변경
# 에디터가 열리면 적절히 수정

# 결과 확인
git log --oneline
```

### 4.3 Cherry-pick 실습

```bash
# main 브랜치로 이동
git checkout main

# feature 브랜치의 특정 커밋만 가져오기
# (feature/add-tests의 테스트 커밋 ID 확인)
git log --oneline feature/add-tests

# 특정 커밋을 cherry-pick
git cherry-pick [테스트 커밋의 ID]

# 결과 확인
git log --oneline
```

## 🏷️ 실습 5: 태그 관리

### 5.1 태그 생성

```bash
# 현재 상태를 v1.0.0으로 태그
git tag -a v1.0.0 -m "Release version 1.0.0"

# 태그 목록 확인
git tag

# 태그 정보 확인
git show v1.0.0
```

### 5.2 다음 버전 개발

```bash
# 새 기능 브랜치
git checkout -b feature/version-2

# package.json 파일 생성
cat > package.json << 'EOF'
{
  "name": "git-practice",
  "version": "2.0.0",
  "description": "Git CLI practice project",
  "main": "main.js",
  "scripts": {
    "test": "node tests.js"
  }
}
EOF

git add package.json
git commit -m "feat: Add package.json for version 2.0.0"

# main으로 병합
git checkout main
git merge feature/add-tests
git merge feature/version-2

# 새 태그 생성
git tag -a v2.0.0 -m "Release version 2.0.0 with tests and package.json"

# 브랜치 정리
git branch -d feature/add-tests
git branch -d feature/version-2
```

## 📊 실습 6: 히스토리 분석

### 6.1 로그 분석

```bash
# 전체 히스토리 그래프로 보기
git log --graph --oneline --all

# 특정 파일의 변경 히스토리
git log --oneline -- README.md

# 작성자별 커밋 통계
git shortlog -sn

# 특정 기간의 커밋
git log --since="1 hour ago" --oneline

# 커밋 메시지로 검색
git log --grep="feat" --oneline
```

### 6.2 변경사항 분석

```bash
# 태그 간 차이점 비교
git diff v1.0.0..v2.0.0

# 특정 파일의 blame 정보
git blame functions.js

# 특정 코드를 언제 추가했는지 찾기
git log -S "add(" --oneline
```

## 🔍 실습 완료 체크리스트

다음 명령어들을 실행해서 실습이 제대로 완료되었는지 확인하세요:

```bash
# ✅ 현재 브랜치가 main인지 확인
git branch --show-current

# ✅ 총 커밋 개수 확인 (10개 이상이어야 함)
git rev-list --count HEAD

# ✅ 태그 확인 (v1.0.0, v2.0.0이 있어야 함)
git tag

# ✅ 파일 목록 확인
ls -la

# ✅ 최종 히스토리 확인
git log --graph --oneline --all

# ✅ 원격 저장소 상태 (아직 없음을 확인)
git remote -v
```

## 🎉 다음 단계

실습을 완료했다면:

1. **GitHub 저장소 생성**: 이 프로젝트를 GitHub에 푸시해보세요
2. **팀 협업**: 다른 사람과 함께 협업 시나리오를 연습해보세요
3. **자동화**: 프로젝트 루트의 스크립트들을 활용해보세요
4. **고급 기능**: Worktree, Bisect 등 고급 기능들을 실습해보세요

### GitHub에 푸시하기

```bash
# GitHub에서 새 저장소 생성 후
git remote add origin https://github.com/your-username/git-practice.git
git push -u origin main
git push origin --tags
```

수고하셨습니다! 🎉 이제 Git CLI의 기본기를 익혔습니다.