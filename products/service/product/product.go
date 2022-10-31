package productService

import (
	"context"
	"fmt"
	"errors"
	"time"
	"go.opentelemetry.io/otel"
	"database/sql"
	"products/db"
	"products/utils/otlp/logs"
	"products/utils/otlp/telemetry"
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

func GetAll(ctx context.Context) ([]Product, error){
	_, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(ctx, fmt.Sprintf("productService.GetAll"))

	defer span.End()

	products := make([]Product, 0)

	logs.Log(span,"Database Query => SELECT * FROM product")

	rows, err := connect.Db.Query("SELECT * FROM product");
	if err != nil{
		return nil, fmt.Errorf("error: %v",err)
	}	

	logs.Log(span,"Database Query completed")

	defer rows.Close()

	logs.Log(span,"scanning rows returned by db to create products array")

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
	logs.Log(span,"returning products array")

	return products,nil
}

func GetProduct(ctx context.Context, id int64) (Product, error){
	_, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(ctx, fmt.Sprintf("productService.GetProduct"))

	defer span.End()

	logs.Log(span,"Database Query => SELECT * FROM product WHERE id = ?")
	var product Product
	row := connect.Db.QueryRow("SELECT * FROM product WHERE id = ?",id)

	logs.Log(span,"Database Query completed")

	logs.Log(span,"scanning row returned by db to create product")

	if err := row.Scan(&product.Id, &product.Name, &product.ShortDesc, &product.Price, &product.CreatedAt, &product.UpdatedAt, &product.UserId); err != nil {
		if err == sql.ErrNoRows{
			return product, ErrProductUnknown
		}
		return product, fmt.Errorf("error: %v",err)
	}
	logs.Log(span,fmt.Sprintf("returning product %d", product.Id))

	return product, nil
}

func AddProduct(ctx context.Context, prod Product)(int64, error){
	_, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(ctx, fmt.Sprintf("productService.AddProduct"))

	defer span.End()

	logs.Log(span,"Database Query => INSERT INTO product (Name, Price, ShortDesc, UserID) VALUES (?,?,?,?)")

	result, err := connect.Db.Exec("INSERT INTO product (Name, Price, ShortDesc, UserID) VALUES (?,?,?,?)", prod.Name , prod.Price , prod.ShortDesc , prod.UserId)

	logs.Log(span,"Database Query completed")

	if err != nil{
		return 0, fmt.Errorf("error: %v", err)
	}
	id,err := result.LastInsertId()
	if err != nil{
		return 0, fmt.Errorf("error: %v", err)
	}
	logs.Log(span,fmt.Sprintf("returning id of the created product : %d", id))

	return id, nil
}

func UpdateProduct(ctx context.Context, id int64, prod Product)(int64, error){
	newCtx, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(ctx, fmt.Sprintf("productService.UpdateProduct"))

	defer span.End()

	product, err := GetProduct(newCtx, id)

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

	logs.Log(span,"Database Query => UPDATE product SET Name = ?, Price = ?, ShortDesc = ? WHERE id = ?")

	result, err := connect.Db.Exec("UPDATE product SET Name = ?, Price = ?, ShortDesc = ? WHERE id = ?", product.Name, product.Price, product.ShortDesc, id)

	logs.Log(span,"Database Query completed")


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

	logs.Log(span,fmt.Sprintf("returning id of the updated product : %d", id))

	return id, nil
}

func DeleteProduct(ctx context.Context, id int64) (Product, error){
	newCtx, span := otel.Tracer(telementaryUtils.SERVICE_NAME).Start(ctx, fmt.Sprintf("productService.DeleteProduct"))

	defer span.End()

	product, err := GetProduct(newCtx, id);

	if err != nil{
		return product, err;
	}

	logs.Log(span,"Database Query => DELETE FROM product WHERE Id = ?")

	result, err := connect.Db.Exec("DELETE FROM product WHERE Id = ?",id)

	logs.Log(span,"Database Query completed")

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

	logs.Log(span,fmt.Sprintf("returning id of the deleted product : %d", id))

	return product, nil
}

