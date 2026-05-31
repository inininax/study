#!/bin/bash

# GitHub API 활용 스크립트
# GitHub CLI 또는 curl을 사용한 GitHub 작업 자동화

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# GitHub CLI 설치 확인
check_gh_cli() {
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI (gh)가 설치되지 않았습니다"
        echo "설치 방법:"
        echo "  macOS: brew install gh"
        echo "  Ubuntu: curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg"
        echo "         echo \"deb [arch=\$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main\" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null"
        echo "         sudo apt update && sudo apt install gh"
        return 1
    fi
    
    # 인증 확인
    if ! gh auth status &> /dev/null; then
        log_warning "GitHub CLI 인증이 필요합니다"
        echo "다음 명령어로 인증하세요: gh auth login"
        return 1
    fi
    
    return 0
}

# Pull Request 생성
create_pr() {
    local title="$1"
    local body="$2"
    local base="${3:-main}"
    local draft="${4:-false}"
    
    if [ -z "$title" ]; then
        log_error "PR 제목을 입력해주세요"
        echo "사용법: $0 pr \"PR 제목\" \"PR 설명\" [base-branch] [draft]"
        return 1
    fi
    
    check_gh_cli || return 1
    
    log_info "Pull Request 생성 중..."
    
    local draft_flag=""
    if [ "$draft" = "true" ]; then
        draft_flag="--draft"
    fi
    
    local pr_url
    if [ -n "$body" ]; then
        pr_url=$(gh pr create --title "$title" --body "$body" --base "$base" $draft_flag)
    else
        pr_url=$(gh pr create --title "$title" --base "$base" $draft_flag)
    fi
    
    log_success "Pull Request 생성 완료: $pr_url"
}

# Pull Request 목록 조회
list_prs() {
    local state="${1:-open}"
    local author="${2:-}"
    
    check_gh_cli || return 1
    
    log_info "Pull Request 목록 조회 (상태: $state)..."
    
    local cmd="gh pr list --state $state --limit 20"
    
    if [ -n "$author" ]; then
        if [ "$author" = "me" ]; then
            cmd="$cmd --author @me"
        else
            cmd="$cmd --author $author"
        fi
    fi
    
    eval $cmd
}

# Pull Request 상태 확인
check_pr_status() {
    local pr_number="$1"
    
    if [ -z "$pr_number" ]; then
        log_error "PR 번호를 입력해주세요"
        echo "사용법: $0 pr-status [PR번호]"
        return 1
    fi
    
    check_gh_cli || return 1
    
    log_info "PR #$pr_number 상태 확인 중..."
    
    echo -e "${BLUE}📋 PR 상세 정보:${NC}"
    gh pr view "$pr_number"
    
    echo ""
    echo -e "${BLUE}✅ CI/CD 체크 상태:${NC}"
    gh pr checks "$pr_number"
    
    echo ""
    echo -e "${BLUE}📝 리뷰 상태:${NC}"
    gh pr view "$pr_number" --json reviews | jq -r '.reviews[] | 
        "\(.author.login): \(.state) - \(.submittedAt)"'
}

# Pull Request 머지
merge_pr() {
    local pr_number="$1"
    local merge_method="${2:-squash}"
    local delete_branch="${3:-true}"
    
    if [ -z "$pr_number" ]; then
        log_error "PR 번호를 입력해주세요"
        echo "사용법: $0 pr-merge [PR번호] [merge방법] [브랜치삭제]"
        echo "merge방법: merge, squash, rebase"
        return 1
    fi
    
    check_gh_cli || return 1
    
    log_info "PR #$pr_number 머지 중 (방법: $merge_method)..."
    
    # CI/CD 상태 확인
    log_info "CI/CD 상태 확인 중..."
    if ! gh pr checks "$pr_number" --json state | jq -e '.[] | select(.state != "SUCCESS" and .state != "SKIPPED")' > /dev/null; then
        log_warning "일부 체크가 실패했거나 진행 중입니다. 계속하시겠습니까? [y/N]"
        read -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "머지가 취소되었습니다."
            return 1
        fi
    fi
    
    # 머지 실행
    local merge_cmd="gh pr merge $pr_number --$merge_method"
    
    if [ "$delete_branch" = "true" ]; then
        merge_cmd="$merge_cmd --delete-branch"
    fi
    
    eval $merge_cmd
    log_success "PR #$pr_number 머지 완료!"
}

# Pull Request 체크아웃
checkout_pr() {
    local pr_number="$1"
    
    if [ -z "$pr_number" ]; then
        log_error "PR 번호를 입력해주세요"
        echo "사용법: $0 pr-checkout [PR번호]"
        return 1
    fi
    
    check_gh_cli || return 1
    
    log_info "PR #$pr_number 체크아웃 중..."
    
    gh pr checkout "$pr_number"
    
    local branch_name=$(git branch --show-current)
    log_success "PR #$pr_number을 $branch_name 브랜치로 체크아웃했습니다."
    
    echo ""
    echo -e "${BLUE}💡 유용한 명령어들:${NC}"
    echo "  git log main..HEAD --oneline    # 변경된 커밋들 확인"
    echo "  git diff main..HEAD             # 전체 변경사항 확인"
    echo "  gh pr view $pr_number           # PR 상세 정보"
}

# Pull Request 리뷰
review_pr() {
    local pr_number="$1"
    local action="$2"  # approve, request-changes, comment
    local message="$3"
    
    if [ -z "$pr_number" ] || [ -z "$action" ]; then
        log_error "PR 번호와 리뷰 액션을 입력해주세요"
        echo "사용법: $0 pr-review [PR번호] [액션] [메시지]"
        echo "액션: approve, request-changes, comment"
        return 1
    fi
    
    check_gh_cli || return 1
    
    log_info "PR #$pr_number 리뷰 제출 중... (액션: $action)"
    
    local review_cmd="gh pr review $pr_number --$action"
    
    if [ -n "$message" ]; then
        review_cmd="$review_cmd --body \"$message\""
    fi
    
    eval $review_cmd
    log_success "리뷰 제출 완료!"
}

# Pull Request에 코멘트 추가
comment_pr() {
    local pr_number="$1"
    local message="$2"
    
    if [ -z "$pr_number" ] || [ -z "$message" ]; then
        log_error "PR 번호와 메시지를 입력해주세요"
        echo "사용법: $0 pr-comment [PR번호] \"코멘트 내용\""
        return 1
    fi
    
    check_gh_cli || return 1
    
    log_info "PR #$pr_number에 코멘트 추가 중..."
    
    gh pr comment "$pr_number" --body "$message"
    log_success "코멘트 추가 완료!"
}

# Pull Request Ready 상태로 변경
ready_pr() {
    local pr_number="$1"
    
    if [ -z "$pr_number" ]; then
        log_error "PR 번호를 입력해주세요"
        echo "사용법: $0 pr-ready [PR번호]"
        return 1
    fi
    
    check_gh_cli || return 1
    
    log_info "PR #$pr_number을 리뷰 준비 상태로 변경 중..."
    
    gh pr ready "$pr_number"
    log_success "PR #$pr_number이 리뷰 준비 상태로 변경되었습니다!"
}

# Issue 생성
create_issue() {
    local title="$1"
    local body="$2"
    local labels="$3"
    local assignee="$4"
    
    if [ -z "$title" ]; then
        log_error "Issue 제목을 입력해주세요"
        echo "사용법: $0 issue \"Issue 제목\" \"Issue 설명\" [labels] [assignee]"
        return 1
    fi
    
    check_gh_cli || return 1
    
    log_info "Issue 생성 중..."
    
    local cmd="gh issue create --title \"$title\""
    
    if [ -n "$body" ]; then
        cmd="$cmd --body \"$body\""
    fi
    
    if [ -n "$labels" ]; then
        cmd="$cmd --label \"$labels\""
    fi
    
    if [ -n "$assignee" ]; then
        cmd="$cmd --assignee \"$assignee\""
    fi
    
    local issue_url=$(eval $cmd)
    log_success "Issue 생성 완료: $issue_url"
}

# Repository 통계 조회
repo_stats() {
    check_gh_cli || return 1
    
    log_info "Repository 통계 조회 중..."
    
    # 기본 정보
    echo -e "${BLUE}📊 Repository 정보:${NC}"
    gh repo view --json name,description,url,stargazerCount,forkCount,primaryLanguage,createdAt,updatedAt | jq -r '
        "Name: \(.name)",
        "Description: \(.description // "N/A")",
        "URL: \(.url)",
        "Stars: \(.stargazerCount)",
        "Forks: \(.forkCount)",
        "Language: \(.primaryLanguage.name // "N/A")",
        "Created: \(.createdAt)",
        "Updated: \(.updatedAt)"
    '
    
    echo ""
    echo -e "${BLUE}🔀 Pull Requests:${NC}"
    gh pr list --state all --limit 5 --json number,title,state,createdAt | jq -r '.[] | "#\(.number): \(.title) (\(.state))"'
    
    echo ""
    echo -e "${BLUE}🐛 Issues:${NC}"
    gh issue list --state all --limit 5 --json number,title,state,createdAt | jq -r '.[] | "#\(.number): \(.title) (\(.state))"'
}

# Release 생성
create_release() {
    local tag="$1"
    local title="$2"
    local notes="$3"
    local prerelease="${4:-false}"
    
    if [ -z "$tag" ]; then
        log_error "Release 태그를 입력해주세요"
        echo "사용법: $0 release [tag] [title] [notes] [prerelease]"
        return 1
    fi
    
    check_gh_cli || return 1
    
    log_info "Release 생성 중: $tag"
    
    local cmd="gh release create \"$tag\""
    
    if [ -n "$title" ]; then
        cmd="$cmd --title \"$title\""
    fi
    
    if [ -n "$notes" ]; then
        cmd="$cmd --notes \"$notes\""
    fi
    
    if [ "$prerelease" = "true" ]; then
        cmd="$cmd --prerelease"
    fi
    
    eval $cmd
    log_success "Release 생성 완료: $tag"
}

# Workflow 상태 확인
check_workflows() {
    check_gh_cli || return 1
    
    log_info "GitHub Actions 워크플로우 상태 확인..."
    
    echo -e "${BLUE}🔄 최근 Workflow 실행:${NC}"
    gh run list --limit 10 --json status,conclusion,name,createdAt,htmlUrl | jq -r '.[] | 
        "\(.name): \(.status) \(if .conclusion then "(\(.conclusion))" else "" end) - \(.createdAt)"'
    
    echo ""
    echo -e "${BLUE}❌ 실패한 Workflow:${NC}"
    gh run list --status failure --limit 5 --json name,createdAt,htmlUrl | jq -r '.[] | 
        "\(.name) - \(.createdAt) - \(.htmlUrl)"'
}

# Repository 설정
setup_repo() {
    local repo_name="$1"
    local description="$2"
    local private="${3:-false}"
    
    if [ -z "$repo_name" ]; then
        log_error "Repository 이름을 입력해주세요"
        echo "사용법: $0 setup [repo-name] [description] [private]"
        return 1
    fi
    
    check_gh_cli || return 1
    
    log_info "Repository 생성 중: $repo_name"
    
    local visibility="public"
    if [ "$private" = "true" ]; then
        visibility="private"
    fi
    
    # Repository 생성
    local cmd="gh repo create \"$repo_name\" --$visibility"
    
    if [ -n "$description" ]; then
        cmd="$cmd --description \"$description\""
    fi
    
    eval $cmd
    
    # 로컬 Git 설정
    git remote add origin "https://github.com/$(gh api user --jq .login)/$repo_name.git"
    
    log_success "Repository 설정 완료: $repo_name"
    echo "원격 저장소: https://github.com/$(gh api user --jq .login)/$repo_name"
}

# 도움말
show_help() {
    echo "GitHub API 활용 도구 (GitHub CLI 기반)"
    echo ""
    echo "📋 Pull Request 관리:"
    echo "  $0 pr \"title\" \"body\" [base] [draft]      PR 생성"
    echo "  $0 pr-list [state] [author]                PR 목록 조회"
    echo "  $0 pr-status [PR번호]                      PR 상태 확인"
    echo "  $0 pr-merge [PR번호] [방법] [브랜치삭제]     PR 머지"
    echo "  $0 pr-checkout [PR번호]                    PR 체크아웃"
    echo "  $0 pr-review [PR번호] [액션] [메시지]       PR 리뷰"
    echo "  $0 pr-comment [PR번호] \"메시지\"            PR 코멘트"
    echo "  $0 pr-ready [PR번호]                       PR ready 상태로 변경"
    echo ""
    echo "🐛 Issue 관리:"
    echo "  $0 issue \"title\" \"body\" [labels] [assignee]  Issue 생성"
    echo ""
    echo "📊 Repository 관리:"
    echo "  $0 stats                                   Repository 통계"
    echo "  $0 release [tag] [title] [notes] [pre]     Release 생성"
    echo "  $0 workflows                               Workflow 상태 확인"
    echo "  $0 setup [name] [desc] [private]           Repository 설정"
    echo "  $0 help                                    도움말"
    echo ""
    echo "💡 예시:"
    echo "  $0 pr \"feat: 새로운 기능 추가\" \"상세 설명\" main false"
    echo "  $0 pr-list open me                         내가 생성한 열린 PR 목록"
    echo "  $0 pr-status 123                           PR #123 상태 확인"
    echo "  $0 pr-merge 123 squash true                PR #123을 squash merge"
    echo "  $0 pr-review 123 approve \"LGTM!\"          PR #123 승인"
    echo "  $0 issue \"버그 수정\" \"버그 상세 내용\" \"bug,priority-high\" \"username\""
    echo "  $0 release \"v1.0.0\" \"첫 번째 릴리스\" \"주요 기능 추가\" false"
    echo ""
    echo "🔧 사전 요구사항:"
    echo "  - GitHub CLI 설치: brew install gh (macOS) 또는 apt install gh (Ubuntu)"
    echo "  - GitHub 인증: gh auth login"
    echo ""
    echo "📖 더 자세한 PR 가이드:"
    echo "  examples/github-pr-guide.md 파일을 참조하세요"
}

# 메인 실행 로직
ACTION=${1:-"help"}

case $ACTION in
    "pr")
        create_pr "$2" "$3" "$4" "$5"
        ;;
    "pr-list")
        list_prs "$2" "$3"
        ;;
    "pr-status")
        check_pr_status "$2"
        ;;
    "pr-merge")
        merge_pr "$2" "$3" "$4"
        ;;
    "pr-checkout")
        checkout_pr "$2"
        ;;
    "pr-review")
        review_pr "$2" "$3" "$4"
        ;;
    "pr-comment")
        comment_pr "$2" "$3"
        ;;
    "pr-ready")
        ready_pr "$2"
        ;;
    "issue")
        create_issue "$2" "$3" "$4" "$5"
        ;;
    "stats")
        repo_stats
        ;;
    "release")
        create_release "$2" "$3" "$4" "$5"
        ;;
    "workflows")
        check_workflows
        ;;
    "setup")
        setup_repo "$2" "$3" "$4"
        ;;
    "help"|*)
        show_help
        ;;
esac