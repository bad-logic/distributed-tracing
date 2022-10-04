package kafkaTopics 

type Topics string

const (
	PRODUCT_CREATED Topics = "productService.productCreated"
	PRODUCT_UPDATED  Topics = "productService.productUpdated"
	PRODUCT_DELETED Topics = "productService.productDeleted"
)