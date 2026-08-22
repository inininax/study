package messaging

import (
	"context"
	"encoding/json"
	"fmt"
	"strconv"

	"github.com/IBM/sarama"
	commonerrors "github.com/kyungseok/msa-saga-go-examples/common/errors"
	"go.uber.org/zap"
)

// Publisher 이벤트 발행 인터페이스
type Publisher interface {
	Publish(ctx context.Context, topic string, key string, event interface{}) error
	Close() error
}

// Consumer 이벤트 구독 인터페이스
type Consumer interface {
	Subscribe(ctx context.Context, topics []string, handler MessageHandler) error
	Close() error
}

// MessageHandler 메시지 핸들러 함수 타입
type MessageHandler func(ctx context.Context, msg *Message) error

// Message 메시지 구조체
type Message struct {
	Topic     string
	Partition int32
	Offset    int64
	Key       []byte
	Value     []byte
}

// KafkaPublisher Kafka 기반 이벤트 발행자
type KafkaPublisher struct {
	producer sarama.SyncProducer
	logger   *zap.Logger
}

// NewKafkaPublisher Kafka 발행자 생성
func NewKafkaPublisher(brokers []string, logger *zap.Logger) (*KafkaPublisher, error) {
	config := sarama.NewConfig()
	config.Producer.Return.Successes = true
	config.Producer.RequiredAcks = sarama.WaitForAll
	config.Producer.Retry.Max = 5
	config.Producer.Idempotent = true
	config.Net.MaxOpenRequests = 1

	producer, err := sarama.NewSyncProducer(brokers, config)
	if err != nil {
		return nil, fmt.Errorf("failed to create kafka producer: %w", err)
	}

	return &KafkaPublisher{
		producer: producer,
		logger:   logger,
	}, nil
}

// Publish 이벤트 발행
func (p *KafkaPublisher) Publish(ctx context.Context, topic string, key string, event interface{}) error {
	payload, err := json.Marshal(event)
	if err != nil {
		return fmt.Errorf("failed to marshal event: %w", err)
	}

	msg := &sarama.ProducerMessage{
		Topic: topic,
		Key:   sarama.StringEncoder(key),
		Value: sarama.ByteEncoder(payload),
	}

	partition, offset, err := p.producer.SendMessage(msg)
	if err != nil {
		p.logger.Error("failed to send message",
			zap.Error(err),
			zap.String("topic", topic),
			zap.String("key", key))
		return fmt.Errorf("failed to send message: %w", err)
	}

	p.logger.Info("message sent successfully",
		zap.String("topic", topic),
		zap.Int32("partition", partition),
		zap.Int64("offset", offset))

	return nil
}

// Close 발행자 종료
func (p *KafkaPublisher) Close() error {
	return p.producer.Close()
}

// KafkaConsumer Kafka 기반 이벤트 구독자
type KafkaConsumer struct {
	consumerGroup sarama.ConsumerGroup
	handler       MessageHandler
	logger        *zap.Logger
}

// NewKafkaConsumer Kafka 구독자 생성
func NewKafkaConsumer(brokers []string, groupID string, logger *zap.Logger) (*KafkaConsumer, error) {
	config := sarama.NewConfig()
	config.Consumer.Group.Rebalance.Strategy = sarama.NewBalanceStrategyRoundRobin()
	config.Consumer.Offsets.Initial = sarama.OffsetOldest
	config.Consumer.Return.Errors = true

	consumerGroup, err := sarama.NewConsumerGroup(brokers, groupID, config)
	if err != nil {
		return nil, fmt.Errorf("failed to create consumer group: %w", err)
	}

	return &KafkaConsumer{
		consumerGroup: consumerGroup,
		logger:        logger,
	}, nil
}

// Subscribe 토픽 구독 (ctx가 취소되면 컨슘 루프도 종료된다)
func (c *KafkaConsumer) Subscribe(ctx context.Context, topics []string, handler MessageHandler) error {
	c.handler = handler

	consumerHandler := &consumerGroupHandler{
		consumer: c,
	}

	go func() {
		for {
			if err := c.consumerGroup.Consume(ctx, topics, consumerHandler); err != nil {
				c.logger.Error("error from consumer", zap.Error(err))
			}

			if ctx.Err() != nil {
				c.logger.Info("consumer loop stopped", zap.String("topics", fmt.Sprint(topics)))
				return
			}
		}
	}()

	return nil
}

// Close 구독자 종료
func (c *KafkaConsumer) Close() error {
	return c.consumerGroup.Close()
}

// consumerGroupHandler Kafka 컨슈머 그룹 핸들러
type consumerGroupHandler struct {
	consumer *KafkaConsumer
}

func (h *consumerGroupHandler) Setup(sarama.ConsumerGroupSession) error   { return nil }
func (h *consumerGroupHandler) Cleanup(sarama.ConsumerGroupSession) error { return nil }

func (h *consumerGroupHandler) ConsumeClaim(session sarama.ConsumerGroupSession, claim sarama.ConsumerGroupClaim) error {
	for message := range claim.Messages() {
		msg := &Message{
			Topic:     message.Topic,
			Partition: message.Partition,
			Offset:    message.Offset,
			Key:       message.Key,
			Value:     message.Value,
		}

		h.consumer.logger.Info("message received",
			zap.String("topic", message.Topic),
			zap.Int32("partition", message.Partition),
			zap.Int64("offset", message.Offset),
			zap.String("key", string(message.Key)))

		if err := h.consumer.handler(session.Context(), msg); err != nil {
			if commonerrors.IsBusinessError(err) {
				// 비즈니스 에러(독약 메시지, 도메인 거절 등)는 재시도해도 같은 결과 → 마킹 후 건너뛴다
				h.consumer.logger.Warn("business error handling message, skipping",
					zap.Error(err),
					zap.String("topic", message.Topic),
					zap.Int64("offset", message.Offset))
				session.MarkMessage(message, "")
				continue
			}
			// 기술 에러는 마킹 없이 세션을 종료한다. 리밸런스 후 마지막 커밋 오프셋부터 재소비된다.
			// (마킹 없이 continue만 하면 이후 파티션의 MarkMessage가 실패한 오프셋까지 함께 커밋해 유실됨)
			h.consumer.logger.Error("technical error handling message, ending session for redelivery",
				zap.Error(err),
				zap.String("topic", message.Topic),
				zap.Int32("partition", message.Partition),
				zap.Int64("offset", message.Offset))
			return err
		}

		session.MarkMessage(message, "")
	}

	return nil
}

// PublishOrderID Order ID를 키로 사용하여 발행하는 헬퍼 함수
func PublishWithOrderID(ctx context.Context, publisher Publisher, topic string, orderID int64, event interface{}) error {
	key := strconv.FormatInt(orderID, 10)
	return publisher.Publish(ctx, topic, key, event)
}
