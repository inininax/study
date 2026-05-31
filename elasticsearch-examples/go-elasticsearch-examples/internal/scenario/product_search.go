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

const productsIndex = "products"

// RunProductSearchScenario는 PRD에서 정의한 상품 검색 시나리오를 실행합니다.
func RunProductSearchScenario(ctx context.Context, c *esclient.Client, reset bool) error {
	logging.L().Info("starting product search scenario", "reset", reset)

	if reset {
		if err := deleteIndexIfExists(ctx, c, productsIndex); err != nil {
			return err
		}
	}

	if err := ensureProductsIndex(ctx, c); err != nil {
		return err
	}

	if reset {
		if err := indexSampleProducts(ctx, c); err != nil {
			return err
		}
	}

	if err := runSampleProductQueries(ctx, c); err != nil {
		return err
	}

	logging.L().Info("product search scenario completed")
	return nil
}

func ensureProductsIndex(ctx context.Context, c *esclient.Client) error {
	res, err := c.Indices.Exists([]string{productsIndex})
	if err != nil {
		return fmt.Errorf("check products index exists: %w", err)
	}
	res.Body.Close()
	if res.StatusCode == 200 {
		logging.L().Debug("products index already exists", "index", productsIndex)
		return nil
	}

	mapping := map[string]interface{}{
		"mappings": map[string]interface{}{
			"properties": map[string]interface{}{
				"id": map[string]interface{}{"type": "keyword"},
				"name": map[string]interface{}{
					"type": "text",
					"fields": map[string]interface{}{
						"keyword": map[string]interface{}{"type": "keyword"},
					},
				},
				"description": map[string]interface{}{"type": "text"},
				"category":    map[string]interface{}{"type": "keyword"},
				"tags":        map[string]interface{}{"type": "keyword"},
				"price":       map[string]interface{}{"type": "double"},
				"created_at":  map[string]interface{}{"type": "date"},
			},
		},
	}

	body, err := json.Marshal(mapping)
	if err != nil {
		return fmt.Errorf("marshal products mapping: %w", err)
	}

	res, err = c.Indices.Create(productsIndex, c.Indices.Create.WithBody(bytes.NewReader(body)))
	if err != nil {
		return fmt.Errorf("create products index: %w", err)
	}
	defer res.Body.Close()
	if res.IsError() {
		return fmt.Errorf("create products index error: %s", res.String())
	}

	logging.L().Info("created products index", "index", productsIndex)
	return nil
}

type product struct {
	ID          string    `json:"id"`
	Name        string    `json:"name"`
	Description string    `json:"description"`
	Category    string    `json:"category"`
	Tags        []string  `json:"tags"`
	Price       float64   `json:"price"`
	CreatedAt   time.Time `json:"created_at"`
}

func sampleProducts() []product {
	now := time.Now().UTC()
	return []product{
		{"1", "Go 마이크로서비스 입문", "Go로 작성된 마이크로서비스 아키텍처 예제 책", "book", []string{"go", "microservice", "backend"}, 39.99, now.Add(-24 * time.Hour)},
		{"2", "Kotlin DDD 실전 가이드", "DDD 관점에서 Kotlin 백엔드 설계를 다룬 서적", "book", []string{"kotlin", "ddd", "architecture"}, 44.50, now.Add(-48 * time.Hour)},
		{"3", "Elasticsearch 운영 모니터링 대시보드", "Elasticsearch 클러스터 모니터링을 위한 템플릿 대시보드", "dashboard", []string{"elasticsearch", "observability"}, 0, now.Add(-72 * time.Hour)},
		{"4", "고성능 Redis 캐시 구성", "대규모 트래픽을 처리하기 위한 Redis 캐시 설계 예제", "article", []string{"redis", "performance", "cache"}, 0, now.Add(-2 * time.Hour)},
		{"5", "Kafka 기반 이벤트 스트리밍", "Kafka로 이벤트 드리븐 아키텍처를 구현하는 방법", "article", []string{"kafka", "event-driven"}, 0, now.Add(-3 * time.Hour)},
		{"6", "AWS 기반 서버리스 아키텍처", "Lambda, API Gateway를 활용한 서버리스 예제", "article", []string{"aws", "serverless"}, 0, now.Add(-4 * time.Hour)},
		{"7", "Next.js SEO 최적화 템플릿", "SEO를 고려한 Next.js 템플릿 프로젝트", "template", []string{"nextjs", "seo", "frontend"}, 0, now.Add(-5 * time.Hour)},
		{"8", "PostgreSQL 성능 튜닝 가이드", "인덱스 설계와 쿼리 최적화 기법을 다룸", "book", []string{"postgresql", "performance"}, 49.90, now.Add(-6 * time.Hour)},
		{"9", "RabbitMQ 메시지 패턴 모음", "토픽, 라우팅 키 등 메시징 패턴 예제", "article", []string{"rabbitmq", "messaging"}, 0, now.Add(-7 * time.Hour)},
		{"10", "LLM 기반 RAG 시스템 설계", "Python, FastAPI, LangChain으로 구현한 RAG 아키텍처", "article", []string{"llm", "rag", "python"}, 0, now.Add(-8 * time.Hour)},
	}
}

func indexSampleProducts(ctx context.Context, c *esclient.Client) error {
	products := sampleProducts()
	var buf bytes.Buffer

	for _, p := range products {
		meta := map[string]interface{}{
			"index": map[string]interface{}{
				"_index": productsIndex,
				"_id":    p.ID,
			},
		}
		metaBytes, err := json.Marshal(meta)
		if err != nil {
			return fmt.Errorf("marshal bulk meta: %w", err)
		}
		sourceBytes, err := json.Marshal(p)
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
		return fmt.Errorf("bulk index products: %w", err)
	}
	defer res.Body.Close()
	if res.IsError() {
		return fmt.Errorf("bulk index products error: %s", res.String())
	}

	logging.L().Info("indexed sample products", "count", len(products))
	return nil
}

func runSampleProductQueries(ctx context.Context, c *esclient.Client) error {
	// full-text + filter + sort + aggregation 예시
	query := map[string]interface{}{
		"query": map[string]interface{}{
			"bool": map[string]interface{}{
				"must": []interface{}{
					map[string]interface{}{
						"multi_match": map[string]interface{}{
							"query":  "성능",
							"fields": []string{"name", "description"},
						},
					},
				},
				"filter": []interface{}{
					map[string]interface{}{
						"terms": map[string]interface{}{
							"category": []string{"book", "article"},
						},
					},
				},
			},
		},
		"aggs": map[string]interface{}{
			"by_category": map[string]interface{}{
				"terms": map[string]interface{}{
					"field": "category",
				},
			},
		},
		"sort": []interface{}{
			map[string]interface{}{
				"price": map[string]interface{}{
					"order": "asc",
				},
			},
		},
	}

	body, err := json.MarshalIndent(query, "", "  ")
	if err != nil {
		return fmt.Errorf("marshal search query: %w", err)
	}
	logging.L().Debug("product search query DSL", "dsl", string(body))

	res, err := c.Search(
		c.Search.WithContext(ctx),
		c.Search.WithIndex(productsIndex),
		c.Search.WithBody(bytes.NewReader(body)),
		c.Search.WithPretty(),
	)
	if err != nil {
		return fmt.Errorf("execute search: %w", err)
	}
	defer res.Body.Close()
	if res.IsError() {
		return fmt.Errorf("search error: %s", res.String())
	}

	var r struct {
		Hits struct {
			Total struct {
				Value int `json:"value"`
			} `json:"total"`
			Hits []struct {
				ID     string                 `json:"_id"`
				Source map[string]interface{} `json:"_source"`
			} `json:"hits"`
		} `json:"hits"`
		Aggregations map[string]json.RawMessage `json:"aggregations"`
	}
	if err := json.NewDecoder(res.Body).Decode(&r); err != nil {
		return fmt.Errorf("decode search response: %w", err)
	}

	logging.L().Info("product search total hits", "total", r.Hits.Total.Value)
	for i, hit := range r.Hits.Hits {
		if i >= 5 {
			break
		}
		logging.L().Debug("product search hit",
			"position", i+1,
			"id", hit.ID,
			"name", hit.Source["name"],
			"category", hit.Source["category"],
			"price", hit.Source["price"],
		)
	}

	if aggRaw, ok := r.Aggregations["by_category"]; ok {
		var agg struct {
			Buckets []struct {
				Key      string `json:"key"`
				DocCount int    `json:"doc_count"`
			} `json:"buckets"`
		}
		if err := json.Unmarshal(aggRaw, &agg); err == nil {
			logging.L().Info("product search aggregation by_category")
			for _, b := range agg.Buckets {
				logging.L().Info("product search category bucket",
					"category", b.Key,
					"count", b.DocCount,
				)
			}
		}
	}

	return nil
}

