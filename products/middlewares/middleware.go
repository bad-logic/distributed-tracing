package middleware

import (
	"fmt"
	"net/http"
	telementaryUtils "products/utils/otlp/telemetry"

	"github.com/julienschmidt/httprouter"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
)


func TelemetryContextHandler(n httprouter.Handle) httprouter.Handle{
	return func(w http.ResponseWriter, r *http.Request, ps httprouter.Params){	

		// starting with r.Context allows us to make sure to include the traceid and tracestate if the request
		// is made by any other service that has propagated the traceid or tracestatue
		ctx := r.Context()

		// create and store a span in the provided context
		newCtx , span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(ctx, fmt.Sprintf("%s:%s", r.Method, r.URL.Path))
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


func PanicHandler(n httprouter.Handle) httprouter.Handle{
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