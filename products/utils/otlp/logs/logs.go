package logs 

import (
	"fmt"
	"go.opentelemetry.io/otel/codes"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/trace"
)

// otlp => open telemetry specification

type ERROR_LEVEL string 

const (
	WARN ERROR_LEVEL = "warn"
	CRITICAL  ERROR_LEVEL = "critical"
)

type OtlpErrorOption struct {
	ErrLevel ERROR_LEVEL
	Message string
}

func Log(span trace.Span, message string){
	span.AddEvent("log",trace.WithAttributes(
		attribute.String("severity", "info"),
		attribute.String("message", message),
	))
}

func Error(span trace.Span, err error, opts OtlpErrorOption){
	fmt.Println("Error:",err)

	// default value for error
	newError := &OtlpErrorOption{
		ErrLevel : WARN,
		Message: err.Error(),
	}
	
	if(opts.ErrLevel != ""){
		newError.ErrLevel = opts.ErrLevel 
	}
	if(opts.Message != ""){
		newError.Message = opts.Message
	}

	code := codes.Ok;

	if(newError.ErrLevel == CRITICAL){
		code = codes.Error
	}
		
	span.RecordError(err)
	span.SetStatus(code, newError.Message)

	span.AddEvent("log",trace.WithAttributes(
		attribute.String("severity", fmt.Sprintf("%v",newError.ErrLevel)),
		attribute.String("message",newError.Message),
	))
}



