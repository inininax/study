#!/bin/bash

# Git 워크플로우 자동화 스크립트
# 사용법: ./git-workflow.sh [action] [parameters...]

set -e

ACTION=${1:-"help"}

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로그 함수들
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Feature 브랜치 생성 및 전환
create_feature() {
    local feature_name=$1
    if [ -z "$feature_name" ]; then
        log_error "Feature 이름을 입력해주세요"
        echo "사용법: $0 feature [feature-name]"
        exit 1
    fi
    
    log_info "Feature 브랜치 생성: feature/$feature_name"
    git checkout main
    git pull origin main
    git checkout -b "feature/$feature_name"
    log_success "Feature 브랜치 생성 완료: feature/$feature_name"
}

# Hotfix 브랜치 생성 및 전환
create_hotfix() {
    local hotfix_name=$1
    if [ -z "$hotfix_name" ]; then
        log_error "Hotfix 이름을 입력해주세요"
        echo "사용법: $0 hotfix [hotfix-name]"
        exit 1
    fi
    
    log_info "Hotfix 브랜치 생성: hotfix/$hotfix_name"
    git checkout main
    git pull origin main
    git checkout -b "hotfix/$hotfix_name"
    log_success "Hotfix 브랜치 생성 완료: hotfix/$hotfix_name"
}

# 현재 브랜치 정리 및 최신화
sync_branch() {
    local current_branch=$(git branch --show-current)
    log_info "현재 브랜치 최신화: $current_branch"
    
    if [ "$current_branch" = "main" ]; then
        git pull origin main
    else
        git checkout main
        git pull origin main
        git checkout "$current_branch"
        git rebase main
    fi
    log_success "브랜치 최신화 완료"
}

# 작업 완료 후 자동 Push
complete_work() {
    local message=$1
    if [ -z "$message" ]; then
        log_error "커밋 메시지를 입력해주세요"
        echo "사용법: $0 complete \"커밋 메시지\""
        exit 1
    fi
    
    local current_branch=$(git branch --show-current)
    log_info "작업 완료 처리: $current_branch"
    
    # 변경사항 확인
    if [ -z "$(git status --porcelain)" ]; then
        log_warning "변경된 파일이 없습니다"
        return 0
    fi
    
    # 변경사항 커밋
    git add .
    git commit -m "$message"
    
    # 원격 브랜치에 Push
    git push origin "$current_branch"
    log_success "작업 완료 및 Push: $current_branch"
    
    # Pull Request 생성 안내
    log_info "GitHub에서 Pull Request를 생성하세요:"
    echo "https://github.com/$(git remote get-url origin | sed 's/.*github.com[:/]\([^/]*\/[^/]*\).*/\1/' | sed 's/\.git$//')/compare/$current_branch?expand=1"
}

# 브랜치 삭제 (로컬 + 원격)
delete_branch() {
    local branch_name=$1
    if [ -z "$branch_name" ]; then
        log_error "삭제할 브랜치 이름을 입력해주세요"
        echo "사용법: $0 delete [branch-name]"
        exit 1
    fi
    
    local current_branch=$(git branch --show-current)
    if [ "$current_branch" = "$branch_name" ]; then
        log_info "main 브랜치로 전환 중..."
        git checkout main
    fi
    
    log_info "브랜치 삭제: $branch_name"
    git branch -D "$branch_name" 2>/dev/null || log_warning "로컬 브랜치가 존재하지 않습니다"
    git push origin --delete "$branch_name" 2>/dev/null || log_warning "원격 브랜치가 존재하지 않습니다"
    log_success "브랜치 삭제 완료: $branch_name"
}

# 브랜치 목록 및 상태 확인
show_status() {
    log_info "Git 상태 확인"
    echo ""
    echo "📋 현재 브랜치:"
    git branch --show-current
    echo ""
    echo "🌿 모든 브랜치:"
    git branch -a
    echo ""
    echo "📊 변경사항:"
    git status --short
    echo ""
    echo "📝 최근 커밋:"
    git log --oneline -5
}

# 도움말
show_help() {
    echo "Git 워크플로우 자동화 도구"
    echo ""
    echo "사용법:"
    echo "  $0 feature [name]       Feature 브랜치 생성"
    echo "  $0 hotfix [name]        Hotfix 브랜치 생성"
    echo "  $0 sync                 현재 브랜치 최신화"
    echo "  $0 complete \"message\"   작업 완료 및 Push"
    echo "  $0 delete [branch]      브랜치 삭제"
    echo "  $0 status               상태 확인"
    echo "  $0 help                 도움말 표시"
    echo ""
    echo "예시:"
    echo "  $0 feature user-login"
    echo "  $0 complete \"feat: 사용자 로그인 기능 구현\""
    echo "  $0 delete feature/user-login"
}

# 메인 실행 로직
case $ACTION in
    "feature")
        create_feature $2
        ;;
    "hotfix")
        create_hotfix $2
        ;;
    "sync")
        sync_branch
        ;;
    "complete")
        complete_work "$2"
        ;;
    "delete")
        delete_branch $2
        ;;
    "status")
        show_status
        ;;
    "help"|*)
        show_help
        ;;
esac