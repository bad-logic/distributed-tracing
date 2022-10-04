package main 

import (
	"github.com/julienschmidt/httprouter"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"products/db"
	"products/controllers/product"
	"products/kafka/client"
)

type Message struct{
	Message string `json:"message"`
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
	
	router := httprouter.New()
  
	router.GET("/products", panicHandler(productController.GetAllProductHandler))
	router.POST("/product", panicHandler(productController.CreateProductHandler))
	router.GET("/product/:productId", panicHandler(productController.GetProductByIdHandler))
	router.PUT("/product/:productId", panicHandler(productController.UpdateProductByIdHandler))
	router.DELETE("/product/:productId", panicHandler(productController.DeleteProductByIdHandler))

	router.NotFound = http.HandlerFunc(func(w http.ResponseWriter, r *http.Request){
		w.WriteHeader(http.StatusNotFound)
		w.Header().Set("Content-Type", "application/json")
		response := Message{
			Message:"NOT FOUND",
		}
		json.NewEncoder(w).Encode(response)
	})

	fmt.Printf("The  server is on tap now: http://localhost:%v\n",port);
	log.Fatal(http.ListenAndServe(":"+strconv.Itoa(port), router))
}