package user 

type User struct {
	ID        		int64       `json:"id"`
	FirstName      	string    	`json:"firstName"`
	LastName     	string    	`json:"lastName"`
	email 		    string    	`json:"email"`
}