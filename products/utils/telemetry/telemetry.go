package telementaryUtils 

import (
	"context"
	"fmt"
	"os"
	semconv "go.opentelemetry.io/otel/semconv/v1.12.0"
	"go.opentelemetry.io/otel/exporters/stdout/stdouttrace"
	"go.opentelemetry.io/otel/sdk/trace"
	"go.opentelemetry.io/otel/sdk/resource"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
	"google.golang.org/grpc"
)

const SERVICE_NAME = "product_service"

/*
	Exporter to export data to the console/terminal
*/
func NewTelemetryStdOutExporter() (trace.SpanExporter,error){
	return stdouttrace.New(
		stdouttrace.WithWriter(os.Stdout),
	)
}

/*
	Exporter to export data to the otlp collector
*/
func NewTelemetryCollectorExporter(ctx context.Context)(*otlptrace.Exporter,error){
	client := otlptracegrpc.NewClient( 
		otlptracegrpc.WithInsecure(),
        otlptracegrpc.WithEndpoint(os.Getenv("LOG_COLLECTOR_ENDPOINT")),
        otlptracegrpc.WithDialOption(grpc.WithBlock()),
    )
	
	exporter, err := otlptrace.New(ctx, client)
	if err != nil {
		return nil, fmt.Errorf("creating OTLP trace exporter: %w", err)
	}
	return exporter,nil
}

func NewOpenTelemetryResource() *resource.Resource {

	containerId := os.Getenv("HOSTNAME")

	r, _ := resource.Merge(
		resource.Default(),
		resource.NewWithAttributes(
			semconv.SchemaURL,
			semconv.ServiceNamespaceKey.String("Shop"), // service.namespace
			semconv.ServiceNameKey.String(SERVICE_NAME), // service.name
			semconv.ServiceInstanceIDKey.String(containerId), // service.instance.id
			semconv.ServiceVersionKey.String("v1.0.0"), // service.version
		),
	)
	return r
}