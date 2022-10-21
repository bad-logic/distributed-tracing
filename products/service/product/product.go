package productService

import (
	"fmt"
	"errors"
	"time"
	"database/sql"
	"products/db"
)

type Product struct {
	Id        		int64       `json:"Id,string"`
	Name      		string    	`json:"Name"`
	Price     		float32    	`json:"Price,string"`
	ShortDesc 		string    	`json:"ShortDesc"`
	CreatedAt   	time.Time 	`json:"CreatedAt,string"`
	UpdatedAt   	time.Time 	`json:"UpdatedAt,string"`
	UserId			int64 		`json:"UserId,string"`
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
        if err := rows.Scan(&product.Id, &product.Name, &product.ShortDesc, &product.Price, &product.CreatedAt, &product.UpdatedAt, &product.UserId); err != nil {
            return nil, fmt.Errorf("products error: %v", err)
        }
		products = append(products,product)
    }
	if err := rows.Err(); err != nil {
        return nil, fmt.Errorf("error: %v", err)
    }
	return products,nil
}

func GetProduct(id int64) (Product, error){
	var product Product
	row := connect.Db.QueryRow("SELECT * FROM product WHERE id = ?",id)
	if err := row.Scan(&product.Id, &product.Name, &product.ShortDesc, &product.Price, &product.CreatedAt, &product.UpdatedAt, &product.UserId); err != nil {
		if err == sql.ErrNoRows{
			return product, ErrProductUnknown
		}
		return product, fmt.Errorf("error: %v",err)
	}
	return product, nil
}

func AddProduct(prod Product)(int64, error){
	result, err := connect.Db.Exec("INSERT INTO product (Name, Price, ShortDesc, UserID) VALUES (?,?,?,?)", prod.Name , prod.Price , prod.ShortDesc , prod.UserId)

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

	if prod.Price > 0 {
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

func DeleteProduct(id int64) (Product, error){
	product, err := GetProduct(id);

	if err != nil{
		return product, err;
	}

	result, err := connect.Db.Exec("DELETE FROM product WHERE Id = ?",id)

	if err != nil{
		return product, fmt.Errorf("error: %v",err)
	}

	count,err := result.RowsAffected()
	if err != nil{
		return product, fmt.Errorf("error: %v",err)
	}
	
	if count != 1 {
		return product, ErrProductUnknown
	}

	return product, nil
}