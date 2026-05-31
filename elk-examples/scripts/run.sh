#!/bin/bash

# ELK Stack Example 실행 스크립트
# GitHub: https://github.com/kyungseok-lee/elk-examples

echo "🚀 ELK Stack Example 프로젝트를 시작합니다..."
echo "📚 GitHub: https://github.com/kyungseok-lee/elk-examples"
echo ""

# 로그 디렉토리 생성
echo "📁 로그 디렉토리를 생성합니다..."
mkdir -p logs

# Docker Compose로 모든 서비스 시작
echo "📦 Docker 컨테이너들을 시작합니다..."
docker compose up -d

# 서비스 상태 확인
echo "⏳ 서비스들이 준비될 때까지 대기합니다..."
sleep 45

# 서비스 상태 확인
echo "🔍 서비스 상태를 확인합니다..."
docker compose ps

echo ""
echo "✅ 모든 서비스가 시작되었습니다!"
echo ""
echo "🌐 접속 URL:"
echo "   Next.js 클라이언트: http://localhost:3000"
echo "   Go 서버 API:        http://localhost:8080"
echo "   Kibana 대시보드:    http://localhost:5601"
echo "   Elasticsearch:      http://localhost:9200"
echo ""
echo "📊 사용 방법:"
echo "   1. Next.js 클라이언트에서 로그 생성 및 조회"
echo "   2. Kibana에서 고급 분석 및 시각화"
echo "   3. Go 서버 API로 직접 로그 전송"
echo "   4. Filebeat를 통한 파일 로그 수집"
echo ""
echo "🔧 관리 명령어:"
echo "   서비스 중지:     docker compose down"
echo "   로그 확인:       docker compose logs -f"
echo "   상태 확인:       docker compose ps"
echo "   재시작:          docker compose restart"
echo ""
echo "📁 데이터 위치:"
echo "   Elasticsearch:   ./data/elasticsearch/"
echo "   로그 파일:       ./logs/"
echo "   설정 파일:       ./data/"
