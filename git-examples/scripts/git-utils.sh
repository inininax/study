#!/bin/bash

# Git 유틸리티 스크립트
# 다양한 Git 작업을 위한 편의 함수들

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# 로그 함수
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Git 저장소 백업
backup_repo() {
    local backup_name="backup-$(date +%Y%m%d-%H%M%S)"
    local repo_name=$(basename "$(git rev-parse --show-toplevel)")
    
    log_info "저장소 백업 생성 중..."
    
    # 백업 디렉토리 생성
    mkdir -p "../backups"
    
    # Git 번들 생성 (모든 브랜치와 태그 포함)
    git bundle create "../backups/${repo_name}-${backup_name}.bundle" --all
    
    # 워킹 디렉토리 압축
    tar -czf "../backups/${repo_name}-${backup_name}-workdir.tar.gz" \
        --exclude='.git' \
        --exclude='node_modules' \
        --exclude='vendor' \
        --exclude='target' \
        --exclude='build' \
        --exclude='dist' \
        .
    
    log_success "백업 완료: ../backups/${repo_name}-${backup_name}.*"
}

# 커밋 히스토리 정리 (Interactive Rebase)
clean_history() {
    local commits=${1:-5}
    
    log_warning "최근 $commits 개의 커밋을 정리합니다"
    echo "주의: 이미 Push된 커밋을 수정하면 협업에 문제가 될 수 있습니다"
    read -p "계속하시겠습니까? [y/N]: " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git rebase -i HEAD~$commits
        log_success "커밋 히스토리 정리 완료"
    else
        log_info "작업이 취소되었습니다"
    fi
}

# 충돌 해결 도우미
resolve_conflicts() {
    log_info "Git 충돌 상황 분석..."
    
    # 충돌 파일 목록
    local conflict_files=$(git diff --name-only --diff-filter=U)
    
    if [ -z "$conflict_files" ]; then
        log_success "현재 충돌이 없습니다"
        return 0
    fi
    
    echo -e "${PURPLE}📋 충돌 파일 목록:${NC}"
    echo "$conflict_files"
    echo ""
    
    # 각 파일의 충돌 마커 수
    echo -e "${PURPLE}🔍 충돌 상세 정보:${NC}"
    while IFS= read -r file; do
        local conflicts=$(grep -c "^<<<<<<< " "$file" 2>/dev/null || echo "0")
        echo "  $file: $conflicts 개의 충돌"
    done <<< "$conflict_files"
    
    echo ""
    echo -e "${YELLOW}💡 충돌 해결 방법:${NC}"
    echo "1. 각 파일을 열어 <<<<<<< , ======= , >>>>>>> 마커를 찾아 수정"
    echo "2. git add [해결된 파일]"
    echo "3. git commit (또는 git rebase --continue)"
    echo ""
    echo "또는 도구 사용:"
    echo "  git mergetool         # 설정된 merge 도구 사용"
    echo "  code --wait [파일]     # VS Code로 충돌 해결"
}

# 브랜치 비교
compare_branches() {
    local branch1=${1:-"main"}
    local branch2=${2:-$(git branch --show-current)}
    
    log_info "브랜치 비교: $branch1 vs $branch2"
    
    echo -e "${PURPLE}📊 커밋 차이:${NC}"
    echo "  $branch1에만 있는 커밋:"
    git log --oneline "$branch2..$branch1" | head -10
    echo ""
    echo "  $branch2에만 있는 커밋:"
    git log --oneline "$branch1..$branch2" | head -10
    
    echo ""
    echo -e "${PURPLE}📁 파일 차이:${NC}"
    git diff --name-status "$branch1" "$branch2"
}

# 태그 관리
manage_tags() {
    local action=$1
    local tag_name=$2
    local message=$3
    
    case $action in
        "list")
            log_info "태그 목록:"
            git tag -l --sort=-version:refname | head -20
            ;;
        "create")
            if [ -z "$tag_name" ]; then
                log_error "태그 이름을 입력해주세요"
                echo "사용법: $0 tag create [tag-name] [message]"
                return 1
            fi
            
            if [ -n "$message" ]; then
                git tag -a "$tag_name" -m "$message"
            else
                git tag "$tag_name"
            fi
            
            log_success "태그 생성: $tag_name"
            echo "원격에 Push하려면: git push origin $tag_name"
            ;;
        "delete")
            if [ -z "$tag_name" ]; then
                log_error "삭제할 태그 이름을 입력해주세요"
                return 1
            fi
            
            git tag -d "$tag_name"
            git push origin --delete "$tag_name" 2>/dev/null || true
            log_success "태그 삭제: $tag_name"
            ;;
        *)
            echo "태그 관리 사용법:"
            echo "  $0 tag list                    # 태그 목록"
            echo "  $0 tag create [name] [msg]     # 태그 생성"
            echo "  $0 tag delete [name]           # 태그 삭제"
            ;;
    esac
}

# 작업 임시 저장
stash_work() {
    local action=$1
    local stash_name=$2
    
    case $action in
        "save")
            if [ -z "$stash_name" ]; then
                stash_name="WIP-$(date +%Y%m%d-%H%M%S)"
            fi
            git stash push -m "$stash_name"
            log_success "작업 임시 저장: $stash_name"
            ;;
        "list")
            log_info "임시 저장된 작업 목록:"
            git stash list
            ;;
        "pop")
            git stash pop
            log_success "최근 임시 저장 작업 복원"
            ;;
        "apply")
            local stash_index=${2:-0}
            git stash apply "stash@{$stash_index}"
            log_success "임시 저장 작업 적용: stash@{$stash_index}"
            ;;
        "drop")
            local stash_index=${2:-0}
            git stash drop "stash@{$stash_index}"
            log_success "임시 저장 작업 삭제: stash@{$stash_index}"
            ;;
        *)
            echo "Stash 관리 사용법:"
            echo "  $0 stash save [name]           # 현재 작업 임시 저장"
            echo "  $0 stash list                  # 임시 저장 목록"
            echo "  $0 stash pop                   # 최근 저장 복원"
            echo "  $0 stash apply [index]         # 특정 저장 적용"
            echo "  $0 stash drop [index]          # 특정 저장 삭제"
            ;;
    esac
}

# 메인 실행 로직
ACTION=${1:-"help"}

case $ACTION in
    "backup")
        backup_repo
        ;;
    "clean")
        clean_history $2
        ;;
    "conflicts")
        resolve_conflicts
        ;;
    "compare")
        compare_branches $2 $3
        ;;
    "tag")
        manage_tags $2 $3 "$4"
        ;;
    "stash")
        stash_work $2 "$3"
        ;;
    "help"|*)
        echo "Git 유틸리티 도구"
        echo ""
        echo "사용법:"
        echo "  $0 backup                      저장소 백업"
        echo "  $0 clean [commits]             커밋 히스토리 정리"
        echo "  $0 conflicts                   충돌 상황 분석"
        echo "  $0 compare [branch1] [branch2] 브랜치 비교"
        echo "  $0 tag [action] [params...]    태그 관리"
        echo "  $0 stash [action] [params...]  작업 임시 저장"
        echo "  $0 help                        도움말"
        ;;
esac