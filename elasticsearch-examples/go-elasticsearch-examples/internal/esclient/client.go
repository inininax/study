package esclient

import (
	"context"
	"fmt"
	"os"
	"time"

	"elasticsearch-examples/internal/logging"

	elasticsearch "github.com/elastic/go-elasticsearch/v8"
)

// Client는 elasticsearch.Client를 감싸는 래퍼입니다.
// 예제 코드에서 공통 설정과 헬스 체크를 제공하기 위해 사용합니다.
type Client struct {
	*elasticsearch.Client
}

// NewFromEnv는 환경 변수 기반으로 Elasticsearch 클라이언트를 생성합니다.
//
// 환경 변수:
//   - ELASTICSEARCH_URL (기본값: http://localhost:9200)
//   - ELASTICSEARCH_USERNAME (옵션)
//   - ELASTICSEARCH_PASSWORD (옵션)
func NewFromEnv() (*Client, error) {
	addr := getenv("ELASTICSEARCH_URL", "http://localhost:9200")

	cfg := elasticsearch.Config{
		Addresses: []string{addr},
	}

	if user := os.Getenv("ELASTICSEARCH_USERNAME"); user != "" {
		cfg.Username = user
		cfg.Password = os.Getenv("ELASTICSEARCH_PASSWORD")
	}

	es, err := elasticsearch.NewClient(cfg)
	if err != nil {
		return nil, fmt.Errorf("failed to create elasticsearch client: %w", err)
	}

	return &Client{Client: es}, nil
}

// Close는 Client 인터페이스를 맞추기 위한 더미 메서드입니다.
// github.com/elastic/go-elasticsearch/v8 클라이언트는 Close가 필요하지 않지만,
// 다른 리소스와의 일관성을 위해 정의해 둡니다.
func (c *Client) Close() error {
	return nil
}

// HealthCheck는 간단한 클러스터 헬스 체크를 수행하고 결과를 로그로 출력합니다.
func (c *Client) HealthCheck(ctx context.Context) error {
	// 타임아웃이 없는 ctx가 들어온 경우를 대비해, 기본 타임아웃을 부여합니다.
	if _, ok := ctx.Deadline(); !ok {
		var cancel context.CancelFunc
		ctx, cancel = context.WithTimeout(ctx, 5*time.Second)
		defer cancel()
	}

	res, err := c.Cluster.Health(
		c.Cluster.Health.WithContext(ctx),
	)
	if err != nil {
		return fmt.Errorf("cluster health request failed: %w", err)
	}
	defer res.Body.Close()

	if res.IsError() {
		logging.L().Error("cluster health error",
			"status", res.Status(),
		)
		return fmt.Errorf("cluster health returned error: %s", res.Status())
	}

	logging.L().Info("cluster health OK",
		"status", res.Status(),
	)
	return nil
}

func getenv(key, def string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return def
}

