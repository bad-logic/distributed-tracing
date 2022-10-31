package appController 

import (
	"encoding/json"
	"net/http"
	"products/utils/struct"
)

func Global404Handler (w http.ResponseWriter, r *http.Request){
	var reply response.ErrorResponse
	w.WriteHeader(http.StatusNotFound)
	w.Header().Set("Content-Type", "application/json")
	reply.Message = "NOT FOUND"
	json.NewEncoder(w).Encode(reply)
}