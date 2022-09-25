package productService

import (
	"fmt"
	"errors"
	"time"
	"database/sql"
	"products/db"
)

type Product struct {
	ID        		int64       `json:"id,string"`
	Name      		string    	`json:"name"`
	Price     		float32    	`json:"price,string"`
	ShortDesc 		string    	`json:"short_description"`
	CreatedAt   	time.Time 	`json:"createdAt,string"`
	UserID			int64 		`json:"userId,string"`
}

var ErrProductUnknown = errors.New("no such product exists")
var ErrProductDuplicate = errors.New("product already exists")
var ErrProductAlreadyUpToDate = errors.New("product is already up to date")

func GetAll() ([]Product, error){
	products := make([]Product, 0)
	rows, err := connect.Db.Query("SELECT * FROM product");
	if err != nil{
		return nil, fmt.Errorf("error: %v",err)
	}	

	defer rows.Close()

    for rows.Next() {
        var product Product
        if err := rows.Scan(&product.ID, &product.Name, &product.ShortDesc, &product.Price, &product.CreatedAt, &product.UserID); err != nil {
            return nil, fmt.Errorf("products error: %v", err)
        }
		products = append(products,product)
    }
	if err := rows.Err(); err != nil {
        return nil, fmt.Errorf("error: %v", err)
    }
	return products,nil
}

func AddProduct(prod Product)(int64, error){
	result, err := connect.Db.Exec("INSERT INTO product (Name, Price, ShortDesc, UserID) VALUES (?,?,?,?)", prod.Name , prod.Price , prod.ShortDesc , prod.UserID)

	if err != nil{
		return 0, fmt.Errorf("error: %v", err)
	}
	id,err := result.LastInsertId()
	if err != nil{
		return 0, fmt.Errorf("error: %v", err)
	}
	return id, nil
}

func UpdateProduct(id int64, prod Product)(int64, error){
	product, err := GetProduct(id)

	if err != nil {
		return 0, err
	}

	if prod.Name != "" {
		product.Name = prod.Name
	}

	if prod.Price > 1 {
		product.Price = prod.Price 
	}

	if prod.ShortDesc != "" {
		product.ShortDesc = prod.ShortDesc
	}

	result, err := connect.Db.Exec("UPDATE product SET Name = ?, Price = ?, ShortDesc = ? WHERE id = ?", product.Name, product.Price, product.ShortDesc, id)

	if err != nil{
		return 0, fmt.Errorf("error: %v",err)
	}

	count,err := result.RowsAffected()
	if err != nil{
		return 0, fmt.Errorf("error: %v",err)
	}
	
	if count != 1 {
		return 0, ErrProductAlreadyUpToDate
	}

	return id, nil
}


func GetProduct(id int64) (Product, error){
	var product Product
	row := connect.Db.QueryRow("SELECT * FROM product WHERE id = ?",id)
	if err := row.Scan(&product.ID, &product.Name, &product.ShortDesc, &product.Price, &product.CreatedAt, &product.UserID); err != nil {
		if err == sql.ErrNoRows{
			return product, ErrProductUnknown
		}
		return product, fmt.Errorf("error: %v",err)
	}
	return product, nil
}

func DeleteProduct(id int64) (int64, error){
	result, err := connect.Db.Exec("DELETE FROM product WHERE ID = ?",id)

	if err != nil{
		return 0, fmt.Errorf("error: %v",err)
	}

	count,err := result.RowsAffected()
	if err != nil{
		return 0, fmt.Errorf("error: %v",err)
	}
	
	if count != 1 {
		return 0, ErrProductUnknown
	}

	return id, nil
}