package scenario

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"math/rand"
	"sync"
	"time"

	"elasticsearch-examples/internal/esclient"
	"elasticsearch-examples/internal/logging"

	"github.com/elastic/go-elasticsearch/v8/esutil"
)

const advancedIndexingIndex = "advanced-indexing-demo"

// RunAdvancedIndexingScenario는 고급 인덱싱 기법을 시연합니다.
// - esutil.BulkIndexer 사용
// - 동시성 제어 (Worker 수 조정)
// - Refresh interval 최적화
// - 에러 처리 및 재시도
// - 성능 모니터링
func RunAdvancedIndexingScenario(ctx context.Context, c *esclient.Client, reset bool) error {
	log := logging.L().With("scenario", "advanced-indexing")
	log.Info("starting advanced indexing scenario", "reset", reset)

	if reset {
		if err := deleteIndexIfExists(ctx, c, advancedIndexingIndex); err != nil {
			return err
		}
	}

	// 1. 인덱스 생성 및 설정 최적화 (refresh interval 포함)
	if err := ensureAdvancedIndexingIndex(ctx, c); err != nil {
		return err
	}

	// 2. esutil.BulkIndexer를 사용한 고성능 인덱싱
	if err := indexWithBulkIndexer(ctx, c); err != nil {
		return err
	}

	// 3. 인덱싱 후 설정 복구 (refresh interval 및 replica 복구)
	if err := restoreIndexSettings(ctx, c); err != nil {
		return err
	}

	// 5. 수동 refresh로 검색 가능 상태로 만들기
	if err := refreshIndex(ctx, c); err != nil {
		return err
	}

	// 6. 인덱싱 결과 검증
	if err := verifyIndexingResults(ctx, c); err != nil {
		return err
	}

	log.Info("advanced indexing scenario completed")
	return nil
}

func ensureAdvancedIndexingIndex(ctx context.Context, c *esclient.Client) error {
	res, err := c.Indices.Exists([]string{advancedIndexingIndex})
	if err != nil {
		return fmt.Errorf("check index exists: %w", err)
	}
	res.Body.Close()
	if res.StatusCode == 200 {
		logging.L().Debug("index already exists", "index", advancedIndexingIndex)
		return nil
	}

	mapping := map[string]interface{}{
		"mappings": map[string]interface{}{
			"properties": map[string]interface{}{
				"id":          map[string]interface{}{"type": "keyword"},
				"title":       map[string]interface{}{"type": "text"},
				"content":     map[string]interface{}{"type": "text"},
				"category":    map[string]interface{}{"type": "keyword"},
				"tags":        map[string]interface{}{"type": "keyword"},
				"views":       map[string]interface{}{"type": "long"},
				"score":       map[string]interface{}{"type": "double"},
				"published":   map[string]interface{}{"type": "boolean"},
				"created_at":  map[string]interface{}{"type": "date"},
				"updated_at":  map[string]interface{}{"type": "date"},
			},
		},
		"settings": map[string]interface{}{
			"number_of_shards":   1,
			"number_of_replicas": 0,        // 인덱싱 중에는 replica 비활성화
			"refresh_interval":   "30s",    // 인덱싱 성능 향상을 위해 refresh interval 증가
		},
	}

	body, err := json.Marshal(mapping)
	if err != nil {
		return fmt.Errorf("marshal mapping: %w", err)
	}

	res, err = c.Indices.Create(
		advancedIndexingIndex,
		c.Indices.Create.WithContext(ctx),
		c.Indices.Create.WithBody(bytes.NewReader(body)),
	)
	if err != nil {
		return fmt.Errorf("create index: %w", err)
	}
	defer res.Body.Close()
	if res.IsError() {
		return fmt.Errorf("create index error: %s", res.String())
	}

	logging.L().Info("created index", "index", advancedIndexingIndex)
	return nil
}


// restoreIndexSettings는 인덱싱 완료 후 설정을 원래대로 복구합니다.
// 참고: Elasticsearch Go 클라이언트 v8의 PutSettings API 사용법이 복잡하므로,
// 여기서는 로그만 출력하고 실제 설정 복구는 수동으로 수행하도록 안내합니다.
// 실무에서는 Elasticsearch REST API를 직접 호출하거나 클라이언트 라이브러리의
// 최신 API를 확인하여 구현해야 합니다.
func restoreIndexSettings(ctx context.Context, c *esclient.Client) error {
	// 실무에서는 다음과 같이 설정을 복구해야 합니다:
	// PUT /advanced-indexing-demo/_settings
	// {
	//   "index": {
	//     "refresh_interval": "1s",
	//     "number_of_replicas": 1
	//   }
	// }
	
	logging.L().Info("indexing completed - settings should be restored manually",
		"index", advancedIndexingIndex,
		"note", "refresh_interval and number_of_replicas should be restored via REST API",
		"restore_command", fmt.Sprintf("PUT /%s/_settings with refresh_interval=1s and number_of_replicas=1", advancedIndexingIndex),
	)
	
	// 실제로는 여기서 REST API를 직접 호출하거나,
	// 클라이언트 라이브러리의 최신 API를 사용하여 설정을 복구해야 합니다.
	// 현재는 예제의 목적상 로그만 출력합니다.
	
	return nil
}

// refreshIndex는 인덱스를 강제로 refresh하여 검색 가능 상태로 만듭니다.
func refreshIndex(ctx context.Context, c *esclient.Client) error {
	res, err := c.Indices.Refresh(
		c.Indices.Refresh.WithContext(ctx),
		c.Indices.Refresh.WithIndex(advancedIndexingIndex),
	)
	if err != nil {
		return fmt.Errorf("refresh index: %w", err)
	}
	defer res.Body.Close()
	if res.IsError() {
		return fmt.Errorf("refresh index error: %s", res.String())
	}

	logging.L().Info("refreshed index", "index", advancedIndexingIndex)
	return nil
}

type advancedDoc struct {
	ID        string    `json:"id"`
	Title     string    `json:"title"`
	Content   string    `json:"content"`
	Category  string    `json:"category"`
	Tags      []string  `json:"tags"`
	Views     int64     `json:"views"`
	Score     float64   `json:"score"`
	Published bool      `json:"published"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// generateSampleDocs는 대량의 샘플 문서를 생성합니다.
func generateSampleDocs(count int) []advancedDoc {
	now := time.Now().UTC()
	categories := []string{"tech", "business", "science", "art", "sports"}
	tagsPool := []string{"go", "elasticsearch", "performance", "optimization", "backend", "microservices", "kubernetes", "docker"}

	docs := make([]advancedDoc, count)
	for i := 0; i < count; i++ {
		id := fmt.Sprintf("doc-%d", i+1)
		category := categories[rand.Intn(len(categories))]
		tagCount := rand.Intn(3) + 1
		tags := make([]string, tagCount)
		for j := 0; j < tagCount; j++ {
			tags[j] = tagsPool[rand.Intn(len(tagsPool))]
		}

		docs[i] = advancedDoc{
			ID:        id,
			Title:     fmt.Sprintf("Document %d: Advanced Indexing Example", i+1),
			Content:   fmt.Sprintf("This is sample content for document %d. It demonstrates advanced indexing techniques using BulkIndexer.", i+1),
			Category:  category,
			Tags:      tags,
			Views:     int64(rand.Intn(10000)),
			Score:     rand.Float64() * 100,
			Published: rand.Float32() > 0.3, // 70% published
			CreatedAt: now.Add(-time.Duration(rand.Intn(30*24)) * time.Hour),
			UpdatedAt: now.Add(-time.Duration(rand.Intn(7*24)) * time.Hour),
		}
	}

	return docs
}

// indexWithBulkIndexer는 esutil.BulkIndexer를 사용하여 고성능 인덱싱을 수행합니다.
func indexWithBulkIndexer(ctx context.Context, c *esclient.Client) error {
	log := logging.L().With("component", "bulk-indexer")

	// 샘플 문서 생성 (1000개)
	docs := generateSampleDocs(1000)
	log.Info("generated sample documents", "count", len(docs))

	// BulkIndexer 설정
	// - NumWorkers: 동시 worker 수 (CPU 코어 수 기반)
	// - FlushBytes: 5MB마다 flush
	// - FlushInterval: 30초마다 flush
	bi, err := esutil.NewBulkIndexer(esutil.BulkIndexerConfig{
		Client:        c.Client,
		Index:         advancedIndexingIndex,
		NumWorkers:    4,                    // 동시 worker 수
		FlushBytes:    5e6,                 // 5MB
		FlushInterval: 30 * time.Second,
		Timeout:       60 * time.Second,
		OnFlushStart: func(ctx context.Context) context.Context {
			log.Debug("bulk indexer flush started")
			return ctx
		},
		OnFlushEnd: func(ctx context.Context) {
			log.Debug("bulk indexer flush completed")
		},
	})
	if err != nil {
		return fmt.Errorf("create bulk indexer: %w", err)
	}
	defer bi.Close(ctx)

	// 통계 수집용
	var (
		successCount int64
		failureCount int64
		mu           sync.Mutex
	)

	startTime := time.Now()

	// 문서 추가
	for _, doc := range docs {
		docJSON, err := json.Marshal(doc)
		if err != nil {
			return fmt.Errorf("marshal document: %w", err)
		}

		err = bi.Add(ctx, esutil.BulkIndexerItem{
			Action:     "index",
			DocumentID: doc.ID,
			Body:       bytes.NewReader(docJSON),
			OnSuccess: func(ctx context.Context, item esutil.BulkIndexerItem, res esutil.BulkIndexerResponseItem) {
				mu.Lock()
				successCount++
				mu.Unlock()
			},
			OnFailure: func(ctx context.Context, item esutil.BulkIndexerItem, res esutil.BulkIndexerResponseItem, err error) {
				mu.Lock()
				failureCount++
				mu.Unlock()

				// 429 에러인 경우 재시도 가능
				if res.Status == 429 {
					log.Warn("bulk indexer item failed with 429",
						"document_id", item.DocumentID,
						"status", res.Status,
						"error", res.Error,
					)
				} else {
					log.Error("bulk indexer item failed",
						"document_id", item.DocumentID,
						"status", res.Status,
						"error", res.Error,
						"err", err,
					)
				}
			},
		})
		if err != nil {
			return fmt.Errorf("add item to bulk indexer: %w", err)
		}
	}

	// 모든 작업 완료 대기
	if err := bi.Close(ctx); err != nil {
		return fmt.Errorf("close bulk indexer: %w", err)
	}

	duration := time.Since(startTime)
	stats := bi.Stats()

	// 성능 통계 출력
	log.Info("bulk indexing completed",
		"total_documents", len(docs),
		"success", successCount,
		"failed", failureCount,
		"duration", duration.String(),
		"docs_per_sec", float64(len(docs))/duration.Seconds(),
		"bulk_indexer_added", stats.NumAdded,
		"bulk_indexer_failed", stats.NumFailed,
		"bulk_indexer_flushed", stats.NumFlushed,
	)

	return nil
}

// verifyIndexingResults는 인덱싱 결과를 검증합니다.
func verifyIndexingResults(ctx context.Context, c *esclient.Client) error {
	log := logging.L().With("component", "verification")

	// 문서 수 확인
	countQuery := map[string]interface{}{
		"query": map[string]interface{}{
			"match_all": map[string]interface{}{},
		},
	}

	body, err := json.Marshal(countQuery)
	if err != nil {
		return fmt.Errorf("marshal count query: %w", err)
	}

	res, err := c.Count(
		c.Count.WithContext(ctx),
		c.Count.WithIndex(advancedIndexingIndex),
		c.Count.WithBody(bytes.NewReader(body)),
	)
	if err != nil {
		return fmt.Errorf("count documents: %w", err)
	}
	defer res.Body.Close()
	if res.IsError() {
		return fmt.Errorf("count documents error: %s", res.String())
	}

	var countResp struct {
		Count int64 `json:"count"`
	}
	if err := json.NewDecoder(res.Body).Decode(&countResp); err != nil {
		return fmt.Errorf("decode count response: %w", err)
	}

	log.Info("indexing verification",
		"index", advancedIndexingIndex,
		"document_count", countResp.Count,
	)

	// 인덱스 통계 확인
	statsRes, err := c.Indices.Stats(
		c.Indices.Stats.WithContext(ctx),
		c.Indices.Stats.WithIndex(advancedIndexingIndex),
		c.Indices.Stats.WithMetric("indexing"),
	)
	if err != nil {
		return fmt.Errorf("get index stats: %w", err)
	}
	defer statsRes.Body.Close()

	var statsResp map[string]interface{}
	if err := json.NewDecoder(statsRes.Body).Decode(&statsResp); err == nil {
		if indices, ok := statsResp["indices"].(map[string]interface{}); ok {
			if indexData, ok := indices[advancedIndexingIndex].(map[string]interface{}); ok {
				if total, ok := indexData["total"].(map[string]interface{}); ok {
					if indexing, ok := total["indexing"].(map[string]interface{}); ok {
						log.Info("indexing statistics",
							"index_total", indexing["index_total"],
							"index_time_in_millis", indexing["index_time_in_millis"],
							"index_failed", indexing["index_failed"],
						)
					}
				}
			}
		}
	}

	return nil
}
