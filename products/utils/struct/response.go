package response 

type SuccessResponse struct {
	Id int64 `json:"id"`
}
 
type ErrorResponse struct {
	Message string `json:"message"`
}