package kafkaClient

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"
	kafkaTopics "products/kafka/topics"
	productService "products/service/product"

	"github.com/Shopify/sarama"
	"go.opentelemetry.io/contrib/instrumentation/github.com/Shopify/sarama/otelsarama"
	"go.opentelemetry.io/otel"
)

var kafkaProducer sarama.SyncProducer 

func SetupKafkaConnection(){
	brokers := []string{os.Getenv("KAFKA_BROKERS")}
	
	config := sarama.NewConfig()
    config.Producer.Partitioner = sarama.NewRandomPartitioner 
	config.Producer.RequiredAcks = sarama.WaitForAll      
	config.Producer.Return.Successes = true

	producer, err := sarama.NewSyncProducer(brokers,config)
	if err != nil{
		log.Panicf("cannot create kafka producer: %v",err)
	}

	kafkaProducer = otelsarama.WrapSyncProducer(config, producer)
}

func ProduceMessage(ctx context.Context, topic kafkaTopics.Topics, data productService.Product) (string, error){
	product,err := json.Marshal(data)
	if err != nil{
        return "", fmt.Errorf("kafka send msg failed: %v",err)
	}
	msg := sarama.ProducerMessage{
		Topic: fmt.Sprintf("%v",topic),
		Value: sarama.ByteEncoder(product),
	}

	otel.GetTextMapPropagator().Inject(ctx, otelsarama.NewProducerMessageCarrier(&msg))

	pid, offset, err := kafkaProducer.SendMessage(&msg)
    if err != nil {
        return "", fmt.Errorf("kafka send msg failed: %v",err)
    }
	
	return fmt.Sprintf("Produced Message on topic:%s with pid:%v, offset:%v",topic, pid, offset), nil
}