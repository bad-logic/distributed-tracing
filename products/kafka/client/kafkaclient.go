
package kafkaClient 

import (
	"fmt"
	"log"
	"os"
	"github.com/Shopify/sarama"
	"products/kafka/topics"
	"products/service/product"
	"encoding/json"
)

var kafkaProducer sarama.SyncProducer 

func SetupKafkaConnection(){
    var err error
	brokers := []string{os.Getenv("KAFKA_BROKERS")}
	
	config := sarama.NewConfig()
    config.Producer.Partitioner = sarama.NewRandomPartitioner 
	config.Producer.RequiredAcks = sarama.WaitForAll      
	config.Producer.Return.Successes = true
	kafkaProducer, err = sarama.NewSyncProducer(brokers,config)

	if err != nil{
		log.Fatal("cannot create kafka producer ",err)
	}
}

func ProduceMessage(topic kafkaTopics.Topics, data productService.Product) (string, error){
	product,err := json.Marshal(data)
	if err != nil{
        return "", fmt.Errorf("kafka send msg failed: %v",err)
	}
	msg := &sarama.ProducerMessage{
		Topic: fmt.Sprintf("%v",topic),
		Value: sarama.ByteEncoder(product),
	}

	pid, offset, err := kafkaProducer.SendMessage(msg)
    if err != nil {
        return "", fmt.Errorf("kafka send msg failed: %v",err)
    }
	
	return fmt.Sprintf("Produced Message on topic:%s with pid:%v, offset:%v",topic, pid, offset), nil
}