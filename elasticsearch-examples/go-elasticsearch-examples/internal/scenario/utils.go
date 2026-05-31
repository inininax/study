package scenario

import (
	"context"
	"fmt"

	"elasticsearch-examples/internal/esclient"
)

// deleteIndexIfExists는 인덱스가 존재하면 삭제합니다.
func deleteIndexIfExists(ctx context.Context, c *esclient.Client, index string) error {
	res, err := c.Indices.Exists([]string{index})
	if err != nil {
		return fmt.Errorf("check index exists: %w", err)
	}
	defer res.Body.Close()
	if res.StatusCode == 404 {
		return nil
	}

	res, err = c.Indices.Delete([]string{index})
	if err != nil {
		return fmt.Errorf("delete index: %w", err)
	}
	defer res.Body.Close()
	if res.IsError() {
		return fmt.Errorf("delete index error: %s", res.String())
	}
	return nil
}

