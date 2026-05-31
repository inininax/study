package scenario

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"time"

	"elasticsearch-examples/internal/esclient"
	"elasticsearch-examples/internal/logging"
)

const logsIndex = "app-logs-demo"

// RunLogAnalyticsScenario는 PRD에서 정의한 로그 분석 시나리오를 실행합니다.
func RunLogAnalyticsScenario(ctx context.Context, c *esclient.Client, reset bool) error {
	logging.L().Info("starting log analytics scenario", "reset", reset)

	if reset {
		if err := deleteIndexIfExists(ctx, c, logsIndex); err != nil {
			return err
		}
	}

	if err := ensureLogsIndex(ctx, c); err != nil {
		return err
	}

	if reset {
		if err := indexSampleLogs(ctx, c); err != nil {
			return err
		}
	}

	if err := runSampleLogQueries(ctx, c); err != nil {
		return err
	}

	logging.L().Info("log analytics scenario completed")
	return nil
}

func ensureLogsIndex(ctx context.Context, c *esclient.Client) error {
	res, err := c.Indices.Exists([]string{logsIndex})
	if err != nil {
		return fmt.Errorf("check logs index exists: %w", err)
	}
	res.Body.Close()
	if res.StatusCode == 200 {
		logging.L().Debug("logs index already exists", "index", logsIndex)
		return nil
	}

	mapping := map[string]interface{}{
		"mappings": map[string]interface{}{
			"properties": map[string]interface{}{
				"timestamp": map[string]interface{}{"type": "date"},
				"level":     map[string]interface{}{"type": "keyword"},
				"service":   map[string]interface{}{"type": "keyword"},
				"message":   map[string]interface{}{"type": "text"},
				"meta": map[string]interface{}{
					"properties": map[string]interface{}{
						"trace_id": map[string]interface{}{"type": "keyword"},
						"user_id":  map[string]interface{}{"type": "keyword"},
					},
				},
			},
		},
	}

	body, err := json.Marshal(mapping)
	if err != nil {
		return fmt.Errorf("marshal logs mapping: %w", err)
	}

	res, err = c.Indices.Create(logsIndex, c.Indices.Create.WithBody(bytes.NewReader(body)))
	if err != nil {
		return fmt.Errorf("create logs index: %w", err)
	}
	defer res.Body.Close()
	if res.IsError() {
		return fmt.Errorf("create logs index error: %s", res.String())
	}

	logging.L().Info("created logs index", "index", logsIndex)
	return nil
}

type logEntry struct {
	Timestamp time.Time              `json:"timestamp"`
	Level     string                 `json:"level"`
	Service   string                 `json:"service"`
	Message   string                 `json:"message"`
	Meta      map[string]interface{} `json:"meta"`
}

func sampleLogs() []logEntry {
	now := time.Now().UTC()
	return []logEntry{
		{now.Add(-5 * time.Minute), "INFO", "auth-service", "사용자 로그인 성공", map[string]interface{}{"trace_id": "t1", "user_id": "u1"}},
		{now.Add(-4 * time.Minute), "ERROR", "auth-service", "비밀번호 불일치", map[string]interface{}{"trace_id": "t2", "user_id": "u2"}},
		{now.Add(-3 * time.Minute), "WARN", "order-service", "결제 승인 지연", map[string]interface{}{"trace_id": "t3", "user_id": "u3"}},
		{now.Add(-2 * time.Minute), "ERROR", "order-service", "결제 승인 실패", map[string]interface{}{"trace_id": "t4", "user_id": "u4"}},
		{now.Add(-1 * time.Minute), "INFO", "api-gateway", "헬스 체크 성공", map[string]interface{}{"trace_id": "t5"}},
		{now.Add(-30 * time.Minute), "ERROR", "api-gateway", "다운스트림 타임아웃", map[string]interface{}{"trace_id": "t6"}},
		{now.Add(-45 * time.Minute), "INFO", "payment-service", "결제 완료", map[string]interface{}{"trace_id": "t7", "user_id": "u5"}},
		{now.Add(-50 * time.Minute), "ERROR", "payment-service", "외부 PG 에러", map[string]interface{}{"trace_id": "t8", "user_id": "u6"}},
	}
}

func indexSampleLogs(ctx context.Context, c *esclient.Client) error {
	logs := sampleLogs()
	var buf bytes.Buffer

	for _, l := range logs {
		meta := map[string]interface{}{
			"index": map[string]interface{}{
				"_index": logsIndex,
			},
		}
		metaBytes, err := json.Marshal(meta)
		if err != nil {
			return fmt.Errorf("marshal bulk meta: %w", err)
		}
		sourceBytes, err := json.Marshal(l)
		if err != nil {
			return fmt.Errorf("marshal bulk source: %w", err)
		}

		buf.Write(metaBytes)
		buf.WriteByte('\n')
		buf.Write(sourceBytes)
		buf.WriteByte('\n')
	}

	res, err := c.Bulk(bytes.NewReader(buf.Bytes()))
	if err != nil {
		return fmt.Errorf("bulk index logs: %w", err)
	}
	defer res.Body.Close()
	if res.IsError() {
		return fmt.Errorf("bulk index logs error: %s", res.String())
	}

	logging.L().Info("indexed sample logs", "count", len(logs))
	return nil
}

func runSampleLogQueries(ctx context.Context, c *esclient.Client) error {
	now := time.Now().UTC()
	// 최근 1시간 범위에서 서비스/레벨별 로그 수 집계
	query := map[string]interface{}{
		"query": map[string]interface{}{
			"range": map[string]interface{}{
				"timestamp": map[string]interface{}{
					"gte": now.Add(-1 * time.Hour),
					"lte": now,
				},
			},
		},
		"aggs": map[string]interface{}{
			"by_service": map[string]interface{}{
				"terms": map[string]interface{}{
					"field": "service",
				},
				"aggs": map[string]interface{}{
					"by_level": map[string]interface{}{
						"terms": map[string]interface{}{
							"field": "level",
						},
					},
				},
			},
		},
		"size": 0,
	}

	body, err := json.MarshalIndent(query, "", "  ")
	if err != nil {
		return fmt.Errorf("marshal logs agg query: %w", err)
	}
	logging.L().Debug("logs aggregation query DSL", "dsl", string(body))

	res, err := c.Search(
		c.Search.WithContext(ctx),
		c.Search.WithIndex(logsIndex),
		c.Search.WithBody(bytes.NewReader(body)),
		c.Search.WithTrackTotalHits(true),
		c.Search.WithPretty(),
	)
	if err != nil {
		return fmt.Errorf("execute logs agg search: %w", err)
	}
	defer res.Body.Close()
	if res.IsError() {
		return fmt.Errorf("logs agg search error: %s", res.String())
	}

	var r struct {
		Hits struct {
			Total struct {
				Value int `json:"value"`
			} `json:"total"`
		} `json:"hits"`
		Aggregations map[string]json.RawMessage `json:"aggregations"`
	}
	if err := json.NewDecoder(res.Body).Decode(&r); err != nil {
		return fmt.Errorf("decode logs agg response: %w", err)
	}

	logging.L().Info("logs in last hour", "total", r.Hits.Total.Value)

	if aggRaw, ok := r.Aggregations["by_service"]; ok {
		var agg struct {
			Buckets []struct {
				Key      string `json:"key"`
				DocCount int    `json:"doc_count"`
				Levels   struct {
					Buckets []struct {
						Key      string `json:"key"`
						DocCount int    `json:"doc_count"`
					} `json:"buckets"`
				} `json:"by_level"`
			} `json:"buckets"`
		}
		if err := json.Unmarshal(aggRaw, &agg); err == nil {
			logging.L().Info("logs aggregation by_service/by_level")
			for _, b := range agg.Buckets {
				logging.L().Info("logs service bucket",
					"service", b.Key,
					"total", b.DocCount,
				)
				var errorCount int
				for _, lb := range b.Levels.Buckets {
					logging.L().Info("logs level bucket",
						"service", b.Key,
						"level", lb.Key,
						"count", lb.DocCount,
					)
					if lb.Key == "ERROR" {
						errorCount = lb.DocCount
					}
				}
				if b.DocCount > 0 {
					errorRate := float64(errorCount) / float64(b.DocCount)
					logging.L().Info("logs service error rate",
						"service", b.Key,
						"error_rate", errorRate,
					)
				}
			}
		}
	}

	return nil
}

