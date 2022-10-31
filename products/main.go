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
	"go.opentelemetry.io/otel/attribute"
	"products/db"
	"products/controllers/product"
	"products/controllers/app"
	"products/kafka/client"
	"products/utils/otlp/telemetry"
)

func setTelemetryContext(n httprouter.Handle) httprouter.Handle{
	return func(w http.ResponseWriter, r *http.Request, ps httprouter.Params){	

		// starting with r.Context allows us to make sure to include the traceid and tracestate if the request
		// is made by any other service that has propagated the traceid or tracestatue
		ctx := r.Context()

		// create and store a span in the provided context
		newCtx , span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(ctx, fmt.Sprintf("%s:%s", r.Method, r.URL))
		span.SetAttributes(
			attribute.String("http.method", r.Method),
			attribute.String("http.route", r.URL.Path),
		)
		defer span.End()

		// saving the context with the created span as a part of the request object
		r = r.WithContext(newCtx)
		n(w,r,ps)
	}
}


func panicHandler(n httprouter.Handle) httprouter.Handle{
	return func(w http.ResponseWriter, r *http.Request, ps httprouter.Params){
	  defer func(){
		if err:= recover();err!=nil{
		  w.WriteHeader(http.StatusInternalServerError);
		  fmt.Println("panic averted",err)
		  return;
		}
	  }()
	  n(w,r,ps)
	}
}


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
  
	router.GET("/products", setTelemetryContext(panicHandler(productController.GetAllProductHandler)))
	router.POST("/product", setTelemetryContext(panicHandler(productController.CreateProductHandler)))
	router.GET("/product/:productId", setTelemetryContext(panicHandler(productController.GetProductByIdHandler)))
	router.PUT("/product/:productId", setTelemetryContext(panicHandler(productController.UpdateProductByIdHandler)))
	router.DELETE("/product/:productId", setTelemetryContext(panicHandler(productController.DeleteProductByIdHandler)))

	router.NotFound = http.HandlerFunc(appController.Global404Handler)

	fmt.Printf("The  server is on tap now: http://localhost:%v\n",port);
	log.Fatal(http.ListenAndServe(":"+strconv.Itoa(port), router))
}