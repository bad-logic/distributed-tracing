package produceProductMessages

import (
	"context"
	"fmt"
	kafkaClient "products/kafka/client"
	kafkaTopics "products/kafka/topics"
	productService "products/service/product"
	"products/utils/otlp/logs"
	telementaryUtils "products/utils/otlp/telemetry"

	"go.opentelemetry.io/otel"
)


func ProduceProductCreatedMessage(ctx context.Context , id int64){
	newCtx, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(ctx, fmt.Sprintf("kafka product.ProductCreated for product %d",id))

	defer span.End()

	product, err := productService.GetProduct(newCtx, id)
	if err  != nil {
		logs.Error(span, err, logs.OtlpErrorOption{"critical",fmt.Sprintf("unable to produce message %v", err)});
		return;
	}
	message, err := kafkaClient.ProduceMessage(newCtx, kafkaTopics.PRODUCT_CREATED,product)
	if err  != nil {
		logs.Error(span, err, logs.OtlpErrorOption{"critical",fmt.Sprintf("unable to produce message %v", err)});
		return;
	}
	logs.Log(span, message);
} 

func ProduceProductUpdatedMessage(ctx context.Context, id int64){
	newCtx, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(ctx, fmt.Sprintf("kafka product.ProductUpdated for product %d",id))

	defer span.End()

	// send the updated product to kafka
	product,err := productService.GetProduct(newCtx, id)
	if err  != nil{
		logs.Error(span, err, logs.OtlpErrorOption{"critical",fmt.Sprintf("unable to produce message %v", err)});
		return
	}

	message, err := kafkaClient.ProduceMessage(newCtx, kafkaTopics.PRODUCT_UPDATED,product)

	if err  != nil {
		logs.Error(span, err, logs.OtlpErrorOption{"critical",fmt.Sprintf("unable to produce message %v", err)});
		return;
	}
	logs.Log(span, message);
}

func ProduceProductDeletedMessage(ctx context.Context, product productService.Product){
	newCtx, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(ctx, fmt.Sprintf("kafka product.ProductDeleted for product %d",product.Id))

	defer span.End()

	message, err := kafkaClient.ProduceMessage(newCtx, kafkaTopics.PRODUCT_DELETED, product)

	if err  != nil {
		logs.Error(span, err, logs.OtlpErrorOption{"critical",fmt.Sprintf("unable to produce message %v", err)});
		return;
	}
	logs.Log(span, message);
}