package scenario

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"

	"elasticsearch-examples/internal/esclient"
	"elasticsearch-examples/internal/logging"
)

const autocompleteIndex = "products-autocomplete"

// RunAutocompleteScenario는 PRD에서 정의한 자동완성 시나리오를 실행합니다.
func RunAutocompleteScenario(ctx context.Context, c *esclient.Client, reset bool) error {
	logging.L().Info("starting autocomplete scenario", "reset", reset)

	if reset {
		if err := deleteIndexIfExists(ctx, c, autocompleteIndex); err != nil {
			return err
		}
	}

	if err := ensureAutocompleteIndex(ctx, c); err != nil {
		return err
	}

	if reset {
		if err := indexSampleAutocompleteDocs(ctx, c); err != nil {
			return err
		}
	}

	if err := runSampleAutocompleteQueries(ctx, c); err != nil {
		return err
	}

	logging.L().Info("autocomplete scenario completed")
	return nil
}

func ensureAutocompleteIndex(ctx context.Context, c *esclient.Client) error {
	res, err := c.Indices.Exists([]string{autocompleteIndex})
	if err != nil {
		return fmt.Errorf("check autocomplete index exists: %w", err)
	}
	res.Body.Close()
	if res.StatusCode == 200 {
		logging.L().Debug("autocomplete index already exists", "index", autocompleteIndex)
		return nil
	}

	mapping := map[string]interface{}{
		"mappings": map[string]interface{}{
			"properties": map[string]interface{}{
				"id":   map[string]interface{}{"type": "keyword"},
				"name": map[string]interface{}{"type": "text"},
				"name_suggest": map[string]interface{}{
					"type": "completion",
				},
			},
		},
	}

	body, err := json.Marshal(mapping)
	if err != nil {
		return fmt.Errorf("marshal autocomplete mapping: %w", err)
	}

	res, err = c.Indices.Create(autocompleteIndex, c.Indices.Create.WithBody(bytes.NewReader(body)))
	if err != nil {
		return fmt.Errorf("create autocomplete index: %w", err)
	}
	defer res.Body.Close()
	if res.IsError() {
		return fmt.Errorf("create autocomplete index error: %s", res.String())
	}

	logging.L().Info("created autocomplete index", "index", autocompleteIndex)
	return nil
}

type autocompleteDoc struct {
	ID          string                 `json:"id"`
	Name        string                 `json:"name"`
	NameSuggest map[string]interface{} `json:"name_suggest"`
}

func sampleAutocompleteDocs() []autocompleteDoc {
	return []autocompleteDoc{
		{"1", "Go 마이크로서비스 입문", map[string]interface{}{"input": []string{"go 마이크로서비스 입문", "go microservices"}}},
		{"2", "Go 고성능 서버 튜닝", map[string]interface{}{"input": []string{"go 고성능", "go performance"}}},
		{"3", "Kotlin 백엔드 실전", map[string]interface{}{"input": []string{"kotlin backend"}}},
		{"4", "Kafka 이벤트 스트리밍", map[string]interface{}{"input": []string{"kafka streaming"}}},
		{"5", "Redis 캐시 베스트 프랙티스", map[string]interface{}{"input": []string{"redis cache"}}},
		{"6", "Elasticsearch 검색 최적화", map[string]interface{}{"input": []string{"elasticsearch search optimization"}}},
	}
}

func indexSampleAutocompleteDocs(ctx context.Context, c *esclient.Client) error {
	docs := sampleAutocompleteDocs()
	var buf bytes.Buffer

	for _, d := range docs {
		meta := map[string]interface{}{
			"index": map[string]interface{}{
				"_index": autocompleteIndex,
				"_id":    d.ID,
			},
		}
		metaBytes, err := json.Marshal(meta)
		if err != nil {
			return fmt.Errorf("marshal bulk meta: %w", err)
		}
		sourceBytes, err := json.Marshal(d)
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
		return fmt.Errorf("bulk index autocomplete docs: %w", err)
	}
	defer res.Body.Close()
	if res.IsError() {
		return fmt.Errorf("bulk index autocomplete docs error: %s", res.String())
	}

	logging.L().Info("indexed autocomplete docs", "count", len(docs))
	return nil
}

func runSampleAutocompleteQueries(ctx context.Context, c *esclient.Client) error {
	// "go" prefix에 대한 suggest 예시
	suggestBody := map[string]interface{}{
		"suggest": map[string]interface{}{
			"product-suggest": map[string]interface{}{
				"prefix": "go",
				"completion": map[string]interface{}{
					"field": "name_suggest",
				},
			},
		},
	}

	body, err := json.MarshalIndent(suggestBody, "", "  ")
	if err != nil {
		return fmt.Errorf("marshal suggest body: %w", err)
	}
	logging.L().Debug("autocomplete suggest query DSL", "dsl", string(body))

	res, err := c.Search(
		c.Search.WithContext(ctx),
		c.Search.WithIndex(autocompleteIndex),
		c.Search.WithBody(bytes.NewReader(body)),
		c.Search.WithPretty(),
	)
	if err != nil {
		return fmt.Errorf("execute suggest search: %w", err)
	}
	defer res.Body.Close()
	if res.IsError() {
		return fmt.Errorf("suggest search error: %s", res.String())
	}

	var r struct {
		Suggest map[string][]struct {
			Text    string `json:"text"`
			Options []struct {
				Text  string  `json:"text"`
				Score float64 `json:"score"`
			} `json:"options"`
		} `json:"suggest"`
	}
	if err := json.NewDecoder(res.Body).Decode(&r); err != nil {
		return fmt.Errorf("decode suggest response: %w", err)
	}

	if entries, ok := r.Suggest["product-suggest"]; ok {
		for _, e := range entries {
			logging.L().Info("autocomplete suggest input", "input", e.Text)
			for _, opt := range e.Options {
				logging.L().Info("autocomplete suggestion",
					"input", e.Text,
					"suggestion", opt.Text,
					"score", opt.Score,
				)
			}
		}
	}

	return nil
}

