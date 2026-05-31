# Level 3: Milvus 고급 (Advanced)

## 학습 목표

대규모 운영 환경 구축 및 성능 튜닝 전문가가 된다.

## 예상 학습 시간

2-3주 (하루 2-3시간 기준)

---

## 📚 학습 내용

### 1. Performance Tuning
**파일**: `01_performance_tuning.py`

**학습 내용**:
- Query 최적화
- Resource allocation
- Cache optimization
- Batch processing optimization

**핵심 개념**:
- Performance profiling
- Bottleneck identification
- Optimization strategies
- Benchmark methodologies

---

### 2. Monitoring & Metrics
**파일**: `02_monitoring_metrics.py`

**학습 내용**:
- Prometheus 메트릭 수집
- Grafana 대시보드 구성
- 커스텀 메트릭 생성
- Alert 설정

**핵심 개념**:
- Key performance indicators
- Metric types (Counter, Gauge, Histogram)
- Alerting thresholds
- Dashboard design

---

### 3. High Availability
**파일**: `03_high_availability.py`

**학습 내용**:
- 클러스터 구성
- Failover 전략
- Load balancing
- Data replication

**핵심 개념**:
- Cluster architecture
- Consistency models
- Recovery procedures
- Disaster recovery

---

### 4. Scalability Patterns
**파일**: `04_scalability_patterns.py`

**학습 내용**:
- Horizontal scaling
- Vertical scaling
- Auto-scaling 구현
- Sharding strategies

**핵심 개념**:
- Scale-out architecture
- Resource management
- Capacity planning
- Load distribution

---

## 🎯 실습 프로젝트

### 프로젝트 1: Production-Ready Milvus Cluster

**요구사항**:
1. 고가용성 클러스터 구성
2. 실시간 모니터링 대시보드
3. Auto-scaling 구현
4. 성능 튜닝 및 벤치마킹

**구현 파일**: `projects/production_cluster/`

---

## 📊 진도 체크리스트

- [ ] Prometheus + Grafana 모니터링 구축
- [ ] 고가용성 클러스터 구성
- [ ] 부하 테스트 및 성능 튜닝 (P99 < 100ms)
- [ ] Auto-scaling 구현
- [ ] Production 클러스터 프로젝트 완성

---

## ⏭️ 다음 단계

Level 3를 완료하면 [Level 4: 실전 프로젝트](../level_4_production/README.md)로 진행하세요.
