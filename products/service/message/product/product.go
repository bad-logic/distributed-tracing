package produceProductMessages

import (
	"fmt"
	"context"
	"go.opentelemetry.io/otel"
	"products/kafka/client"
	"products/kafka/topics"
	"products/service/product"
	"products/utils/otlp/telemetry"
	"products/utils/otlp/logs"
)


func ProduceProductCreatedMessage(ctx context.Context , id int64){
	_, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(ctx, fmt.Sprintf("kafka product.ProductCreated for product %d",id))

	defer span.End()

	product, err := productService.GetProduct(id)
	if err  != nil {
		logs.Error(span, err, logs.OtlpErrorOption{"critical",fmt.Sprintf("unable to produce message %v", err)});
		return;
	}
	message, err := kafkaClient.ProduceMessage(kafkaTopics.PRODUCT_CREATED,product)
	if err  != nil {
		logs.Error(span, err, logs.OtlpErrorOption{"critical",fmt.Sprintf("unable to produce message %v", err)});
		return;
	}
	logs.Log(span, message);
} 

func ProduceProductUpdatedMessage(ctx context.Context, id int64){
	_, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(ctx, fmt.Sprintf("kafka product.ProductUpdated for product %d",id))

	defer span.End()

	// send the updated product to kafka
	product,err := productService.GetProduct(id)
	if err  != nil{
		logs.Error(span, err, logs.OtlpErrorOption{"critical",fmt.Sprintf("unable to produce message %v", err)});
		return
	}

	message, err := kafkaClient.ProduceMessage(kafkaTopics.PRODUCT_UPDATED,product)

	if err  != nil {
		logs.Error(span, err, logs.OtlpErrorOption{"critical",fmt.Sprintf("unable to produce message %v", err)});
		return;
	}
	logs.Log(span, message);
}

func ProduceProductDeletedMessage(ctx context.Context, product productService.Product){
	_, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(ctx, fmt.Sprintf("kafka product.ProductDeleted for product %d",product.Id))

	defer span.End()

	message, err := kafkaClient.ProduceMessage(kafkaTopics.PRODUCT_DELETED, product)

	if err  != nil {
		logs.Error(span, err, logs.OtlpErrorOption{"critical",fmt.Sprintf("unable to produce message %v", err)});
		return;
	}
	logs.Log(span, message);
}