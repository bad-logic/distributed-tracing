package productController 

import (
	"fmt"
	"strconv"
	"encoding/json"
	"net/http"
	"github.com/julienschmidt/httprouter"
	"go.opentelemetry.io/otel"
	"products/service/product"
	productMessages "products/service/message/product"
	"products/utils/struct"
	"products/utils/otlp/telemetry"
	"products/utils/otlp/logs"
)


func GetAllProductHandler(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
	// creating a new span for the same trace-id 
	newCtx, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(r.Context(), "ProductController.GetAllProductHandler")
	defer span.End()

	var reply response.ErrorResponse
	w.Header().Set("Content-Type", "application/json")
	
	products, err := productService.GetAll(newCtx)
	
	if err != nil{
		logs.Error(span,err,logs.OtlpErrorOption{"critical",fmt.Sprintf("response ended with %v status code",http.StatusInternalServerError)});

		w.WriteHeader(http.StatusInternalServerError)
		reply.Message ="Something went wrong."
		json.NewEncoder(w).Encode(reply)
		return
	}

	logs.Log(span, "products fetched successfully")
	
	json.NewEncoder(w).Encode(products)
}


func CreateProductHandler(w http.ResponseWriter, r *http.Request, _ httprouter.Params) {
	newCtx, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(r.Context(), "ProductController.CreateProductHandler")
	defer span.End()

	var reply response.ErrorResponse
	w.Header().Set("Content-Type", "application/json")

	decoder := json.NewDecoder(r.Body)
	var newProduct productService.Product

	err := decoder.Decode(&newProduct)

	if err != nil {
		logs.Error(span,err,logs.OtlpErrorOption{"critical",fmt.Sprintf("response ended with %v status code",http.StatusBadRequest)});

		w.WriteHeader(http.StatusBadRequest)
		reply.Message = "Bad Product"
		json.NewEncoder(w).Encode(reply)
		return
	}
	id, err := productService.AddProduct(newCtx,newProduct)

	if err != nil{
		logs.Error(span,err,logs.OtlpErrorOption{"critical",fmt.Sprintf("response ended with %v status code",http.StatusInternalServerError)});

		w.WriteHeader(http.StatusInternalServerError)
		reply.Message = "Something went wrong."
		json.NewEncoder(w).Encode(reply)
		return
	}

	logs.Log(span, fmt.Sprintf("product %d created successfully",id))
	
	productMessages.ProduceProductCreatedMessage(newCtx,id)
	json.NewEncoder(w).Encode(response.SuccessResponse {Id:id})
}

func UpdateProductByIdHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params) {
	newCtx, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(r.Context(), "ProductController.UpdateProductByIdHandler")
	defer span.End()

	var reply response.ErrorResponse
	w.Header().Set("Content-Type", "application/json")

	id, err := strconv.ParseInt(p.ByName("productId"),10,64)

	if err != nil {
		logs.Error(span,err,logs.OtlpErrorOption{"warn",fmt.Sprintf("response ended with %v status code",http.StatusBadRequest)});

		w.WriteHeader(http.StatusBadRequest)
		reply.Message = fmt.Sprintf("%s is not a valid product ID, it must be a number.", p.ByName("productId"))
		json.NewEncoder(w).Encode(reply)
		return
	}

	decoder := json.NewDecoder(r.Body)
	var updateProduct productService.Product

	err = decoder.Decode(&updateProduct)

	if err != nil {
		logs.Error(span,err,logs.OtlpErrorOption{"critical",fmt.Sprintf("response ended with %v status code",http.StatusBadRequest)});

		w.WriteHeader(http.StatusBadRequest)
		reply.Message = "Bad Product"
		json.NewEncoder(w).Encode(reply)
		return
	}

	id, err = productService.UpdateProduct(newCtx,id,updateProduct)

	if err == productService.ErrProductUnknown {
		logs.Error(span,err,logs.OtlpErrorOption{"warn",fmt.Sprintf("response ended with %v status code",http.StatusBadRequest)});

		w.WriteHeader(http.StatusBadRequest)
		reply.Message = "Product doesn't exist."
		json.NewEncoder(w).Encode(reply)
		return
	}

	if err == productService.ErrProductAlreadyUpToDate {
		logs.Error(span,err,logs.OtlpErrorOption{"warn",fmt.Sprintf("response ended with %v status code",http.StatusBadRequest)});

		w.WriteHeader(http.StatusBadRequest)
		reply.Message = "No new values to update"
		json.NewEncoder(w).Encode(reply)
		return
	}

	if err != nil{
		logs.Error(span,err,logs.OtlpErrorOption{"critical",fmt.Sprintf("response ended with %v status code",http.StatusInternalServerError)});

		w.WriteHeader(http.StatusInternalServerError)
		reply.Message = "Something went wrong."
		json.NewEncoder(w).Encode(reply)
		return
	}

	logs.Log(span, fmt.Sprintf("product %d updated successfully",id))
	
	productMessages.ProduceProductUpdatedMessage(newCtx,id)

	json.NewEncoder(w).Encode(response.SuccessResponse {Id:id})
}

func GetProductByIdHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params){

	newCtx, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(r.Context(), "ProductController.GetProductByIdHandler")
	defer span.End()

	var reply response.ErrorResponse
	w.Header().Set("Content-Type", "application/json")

	ID, err := strconv.ParseInt(p.ByName("productId"),10,64)

	if err != nil {
		logs.Error(span,err,logs.OtlpErrorOption{"warn",fmt.Sprintf("response ended with %v status code",http.StatusBadRequest)});

		w.WriteHeader(http.StatusBadRequest)
		reply.Message =fmt.Sprintf("%s is not a valid product ID, it must be a number.", p.ByName("productId"))
		json.NewEncoder(w).Encode(reply)
		return
	}

	product,err := productService.GetProduct(newCtx, ID)

	if err == productService.ErrProductUnknown {
		logs.Error(span,err,logs.OtlpErrorOption{"warn",fmt.Sprintf("response ended with %v status code",http.StatusBadRequest)});

		w.WriteHeader(http.StatusBadRequest)
		reply.Message = "Product doesn't exist."
		json.NewEncoder(w).Encode(reply)
		return
	}

	if err != nil {
		logs.Error(span,err,logs.OtlpErrorOption{"critical",fmt.Sprintf("response ended with %v status code",http.StatusInternalServerError)});

		w.WriteHeader(http.StatusInternalServerError)
		reply.Message = "Something went wrong."
		json.NewEncoder(w).Encode(reply)
		return
	}

	logs.Log(span, fmt.Sprintf("product %d fetched successfully",ID))

	json.NewEncoder(w).Encode(product)
}


func DeleteProductByIdHandler(w http.ResponseWriter, r *http.Request, p httprouter.Params){
	newCtx, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(r.Context(), "ProductController.DeleteProductByIdHandler")
	defer span.End()

	var reply response.ErrorResponse
	w.Header().Set("Content-Type", "application/json")

	ID, err := strconv.ParseInt(p.ByName("productId"),10,64)

	if err != nil {
		logs.Error(span,err,logs.OtlpErrorOption{"warn",fmt.Sprintf("response ended with %v status code",http.StatusBadRequest)});

		w.WriteHeader(http.StatusBadRequest)
		reply.Message = fmt.Sprintf("%s is not a valid product ID, it must be a number.", p.ByName("productId"))
		json.NewEncoder(w).Encode(reply)
		return
	}

	product,err := productService.DeleteProduct(newCtx, ID)

	if err == productService.ErrProductUnknown {
		logs.Error(span,err,logs.OtlpErrorOption{"warn",fmt.Sprintf("response ended with %v status code",http.StatusNotFound)});

		w.WriteHeader(http.StatusNotFound)
		reply.Message = "Product doesn't exist."
		json.NewEncoder(w).Encode(reply)
		return
	}

	if err != nil {
		logs.Error(span,err,logs.OtlpErrorOption{"critical",fmt.Sprintf("response ended with %v status code",http.StatusInternalServerError)});

		w.WriteHeader(http.StatusInternalServerError)
		reply.Message = "Something went wrong."
		json.NewEncoder(w).Encode(reply)
		return
	}

	logs.Log(span, fmt.Sprintf("product %d deleted successfully", ID))

	productMessages.ProduceProductDeletedMessage(newCtx, product)

	json.NewEncoder(w).Encode(response.SuccessResponse { Id:product.Id })
}