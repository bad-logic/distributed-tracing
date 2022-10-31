package productController 

import (
	"fmt"
	"strconv"
	"encoding/json"
	"net/http"
	"github.com/julienschmidt/httprouter"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/codes"
	"go.opentelemetry.io/otel/trace"
	"go.opentelemetry.io/otel/attribute"
	"products/service/product"
	"products/utils/struct"
	"products/kafka/client"
	"products/kafka/topics"
	"products/utils/telemetry"
)


func GetAllProductHandler(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
	// creating a new span for the same trace-id 
	_, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(r.Context(), "ProductController.GetAllProductHandler")
	defer span.End()

	var reply response.ErrorResponse
	w.Header().Set("Content-Type", "application/json")
	
	products, err := productService.GetAll()
	
	if err != nil{
		fmt.Println("Error:",err)
		span.RecordError(err)
		span.SetStatus(codes.Error, err.Error())

		span.AddEvent("log",trace.WithAttributes(
			attribute.String("log.severity", "info"),
			attribute.String("log.message","Something went wrong."),
			attribute.Int("log.status",http.StatusInternalServerError),
		))

		w.WriteHeader(http.StatusInternalServerError)
		reply.Message ="Something went wrong."
		json.NewEncoder(w).Encode(reply)
		return
	}
	span.AddEvent("log",trace.WithAttributes(
		attribute.String("log.severity", "info"),
		attribute.String("log.message", "products fetched successfully"),
	))
	json.NewEncoder(w).Encode(products)
}


func CreateProductHandler(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
	var reply response.ErrorResponse
	w.Header().Set("Content-Type", "application/json")

	decoder := json.NewDecoder(r.Body)
	var newProduct productService.Product

	err := decoder.Decode(&newProduct)

	if err != nil {
		fmt.Println("Error :",err)
		w.WriteHeader(http.StatusBadRequest)
		reply.Message = "Bad Product"
		json.NewEncoder(w).Encode(reply)
		return
	}
	id, err := productService.AddProduct(newProduct)

	if err != nil{
		fmt.Println("Error :",err)
		w.WriteHeader(http.StatusInternalServerError)
		reply.Message = "Something went wrong."
		json.NewEncoder(w).Encode(reply)
		return
	}

	// send the created product to kafka
	product,err := productService.GetProduct(id)
	if err  != nil{
		fmt.Println("Error fetching created product:",err)
	}
	kafkaClient.ProduceMessage(kafkaTopics.PRODUCT_CREATED,product)
	json.NewEncoder(w).Encode(response.SuccessResponse {Id:id})
}

func UpdateProductByIdHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
	var reply response.ErrorResponse
	w.Header().Set("Content-Type", "application/json")

	id, err := strconv.ParseInt(p.ByName("productId"),10,64)

	if err != nil {
		fmt.Println("Error :",err)
		w.WriteHeader(http.StatusBadRequest)
		reply.Message = fmt.Sprintf("%s is not a valid product ID, it must be a number.", p.ByName("productId"))
		json.NewEncoder(w).Encode(reply)
		return
	}

	decoder := json.NewDecoder(r.Body)
	var updateProduct productService.Product

	err = decoder.Decode(&updateProduct)

	if err != nil {
		fmt.Println("Error :",err)
		w.WriteHeader(http.StatusBadRequest)
		reply.Message = "Bad Product"
		json.NewEncoder(w).Encode(reply)
		return
	}

	id, err = productService.UpdateProduct(id,updateProduct)

	if err == productService.ErrProductUnknown {
		fmt.Println("Error :",err)
		w.WriteHeader(http.StatusBadRequest)
		reply.Message = "Product doesn't exist."
		json.NewEncoder(w).Encode(reply)
		return
	}

	if err == productService.ErrProductAlreadyUpToDate {
		fmt.Println("Error :",err)
		w.WriteHeader(http.StatusBadRequest)
		reply.Message = "No new values to update"
		json.NewEncoder(w).Encode(reply)
		return
	}

	if err != nil{
		fmt.Println("Error :",err)
		w.WriteHeader(http.StatusInternalServerError)
		reply.Message = "Something went wrong."
		json.NewEncoder(w).Encode(reply)
		return
	}

	// send the updated product to kafka
	product,err := productService.GetProduct(id)
	if err  != nil{
		fmt.Println("Error fetching created product:",err)
	}
	kafkaClient.ProduceMessage(kafkaTopics.PRODUCT_UPDATED,product)
	json.NewEncoder(w).Encode(response.SuccessResponse {Id:id})
}

func GetProductByIdHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params){
	var reply response.ErrorResponse
	w.Header().Set("Content-Type", "application/json")

	ID, err := strconv.ParseInt(p.ByName("productId"),10,64)

	if err != nil {
		fmt.Println("Error :",err)
		w.WriteHeader(http.StatusBadRequest)
		reply.Message =fmt.Sprintf("%s is not a valid product ID, it must be a number.", p.ByName("productId"))
		json.NewEncoder(w).Encode(reply)
		return
	}

	product,err := productService.GetProduct(ID)

	if err == productService.ErrProductUnknown {
		fmt.Println("Error :",err)
		w.WriteHeader(http.StatusBadRequest)
		reply.Message = "Product doesn't exist."
		json.NewEncoder(w).Encode(reply)
		return
	}

	if err != nil {
		fmt.Println("Error :",err)
		w.WriteHeader(http.StatusInternalServerError)
		reply.Message = "Something went wrong."
		json.NewEncoder(w).Encode(reply)
		return
	}

	json.NewEncoder(w).Encode(product)
}


func DeleteProductByIdHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params){
	var reply response.ErrorResponse
	w.Header().Set("Content-Type", "application/json")

	ID, err := strconv.ParseInt(p.ByName("productId"),10,64)

	if err != nil {
		fmt.Println("Error :",err)
		w.WriteHeader(http.StatusBadRequest)
		reply.Message = fmt.Sprintf("%s is not a valid product ID, it must be a number.", p.ByName("productId"))
		json.NewEncoder(w).Encode(reply)
		return
	}

	product,err := productService.DeleteProduct(ID)

	if err == productService.ErrProductUnknown {
		fmt.Println("Error :",err)
		w.WriteHeader(http.StatusNotFound)
		reply.Message = "Product doesn't exist."
		json.NewEncoder(w).Encode(reply)
		return
	}

	if err != nil {
		fmt.Println("Error :",err)
		w.WriteHeader(http.StatusInternalServerError)
		reply.Message = "Something went wrong."
		json.NewEncoder(w).Encode(reply)
		return
	}

	kafkaClient.ProduceMessage(kafkaTopics.PRODUCT_DELETED,product)
	json.NewEncoder(w).Encode(response.SuccessResponse {Id:product.Id})
}