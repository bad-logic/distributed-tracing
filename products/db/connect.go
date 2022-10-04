package connect 


import (
	"database/sql"
	"time"
	"fmt"
	"os"
	"github.com/go-sql-driver/mysql"
)

var Db *sql.DB 

func initialDatabaseTableSetup(){
	if Db == nil{
		ConnectToDatabase()
	}

	_ , err := Db.Exec("CREATE TABLE IF NOT EXISTS product(Id INT NOT NULL AUTO_INCREMENT,Name VARCHAR(128) NOT NULL,ShortDesc VARCHAR(128),Price FLOAT NOT NULL,CreatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,UserId INT NOT NULL,PRIMARY KEY (`Id`))");

	if err != nil{
		fmt.Println("err creating product table")
	}

	_ , err1 := Db.Exec("CREATE TABLE IF NOT EXISTS user(Id INT  NOT NULL,FirstName VARCHAR(128) NOT NULL,LastName VARCHAR(128) NOT NULL,Email VARCHAR(128) NOT NULL,UNIQUE (Email),PRIMARY KEY (`Id`))")

	if err1 != nil{
		fmt.Println("err creating user table")
	}
}

func ConnectToDatabase(){
	cfg := mysql.Config{
		User: os.Getenv("DB_USERNAME"),
		Passwd: os.Getenv("DB_PASSWORD"),
		Net: "tcp",
		Addr: os.Getenv("DB_HOST")+":"+os.Getenv("DB_PORT"),
		DBName: os.Getenv("DB_NAME"),
		ParseTime: true,
	}
	
	var err error
	Db, err = sql.Open(os.Getenv("DB_DIALECT"),cfg.FormatDSN())
	if err != nil{
		panic(err)
	}

	Db.SetConnMaxLifetime(time.Minute * 3)
	Db.SetMaxOpenConns(10)
	Db.SetMaxIdleConns(10)

	pingErr := Db.Ping()
	if pingErr != nil{
		panic(pingErr)
	}
	initialDatabaseTableSetup()
	fmt.Println("Connected to sql server ✔️")
}

func GetConnection() *sql.DB {
	if Db == nil{
		ConnectToDatabase()
	}
	return Db;
}