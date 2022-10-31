package main 

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"github.com/julienschmidt/httprouter"
	"go.opentelemetry.io/otel"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	"products/db"
	"products/controllers/product"
	"products/controllers/app"
	"products/kafka/client"
	"products/utils/otlp/telemetry"
	mw "products/middlewares"
)



func init(){
	connect.ConnectToDatabase()
}

func init(){
	kafkaClient.SetupKafkaConnection()
}


func main(){
	
	port, err := strconv.Atoi(os.Getenv("PORT"))
	if err!= nil{
		log.Fatal("Cannot parse PORT env")
	}

	exp, err := telementaryUtils.NewTelemetryCollectorExporter(context.Background())
	if err!= nil{
		log.Fatal(err)
	}

	tp := sdktrace.NewTracerProvider(
		sdktrace.WithBatcher(exp),
		sdktrace.WithResource(telementaryUtils.NewOpenTelemetryResource()),
	)

	defer func() {
		if err := tp.Shutdown(context.Background()); err != nil {
			log.Fatal(err)
		}
	}()

	otel.SetTracerProvider(tp)

	
	router := httprouter.New()
  
	router.GET("/products", mw.TelemetryContextHandler(mw.PanicHandler(productController.GetAllProductHandler)))
	router.POST("/product", mw.TelemetryContextHandler(mw.PanicHandler(productController.CreateProductHandler)))
	router.GET("/product/:productId", mw.TelemetryContextHandler(mw.PanicHandler(productController.GetProductByIdHandler)))
	router.PUT("/product/:productId", mw.TelemetryContextHandler(mw.PanicHandler(productController.UpdateProductByIdHandler)))
	router.DELETE("/product/:productId", mw.TelemetryContextHandler(mw.PanicHandler(productController.DeleteProductByIdHandler)))

	router.NotFound = http.HandlerFunc(appController.Global404Handler)

	fmt.Printf("The  server is on tap now: http://localhost:%v\n",port);
	log.Fatal(http.ListenAndServe(":"+strconv.Itoa(port), router))
}