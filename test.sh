################################################################
#
# Author: RB
# Version 1
# This script is used for testing open telemetry logs
#
################################################################


if [ ! -x $(which curl)  ];then
    echo "Please install curl command to execute the task"
    exit 1
fi

echo "creating products..."
for i in `seq 1 230`;
do
  curl -X POST -H "Content-Type: application/json" -d  "{\"name\": \"summer-collection\",\"price\": \"99.99\",\"userId\": \"$((i * 5))\"}" localhost:8082/product;
  printf "\n";
done

echo "get individual product"
for i in `seq 1 145`;
do
  curl -X GET localhost:8082/product/"$i";
  printf "\n";
done

echo "updating short description"
for i in `seq 1 95`;
do
  curl -X PUT -H "Content-Type: application/json" -d  "{\"ShortDesc\": \"this product is very comfortable\"}" localhost:8082/product/"$i";
  printf "\n";
done

curl -X GET localhost:8082/products;
printf "\n";

echo "get individual product after short description update"
for i in `seq 1 95`;
do
  curl -X GET localhost:8082/product/"$i";
  printf "\n";
done

echo "updating name"
for i in `seq 25 85`;
do
  curl -X PUT -H "Content-Type: application/json" -d  "{\"name\": \"winter-collection\"}" localhost:8082/product/"$i";
  printf "\n";
done

echo "updating price"
for i in `seq 25 250`;
do
  price="$((i * 5)).99"
  curl -X PUT -H "Content-Type: application/json" -d  "{\"price\": \"$price\"}" localhost:8082/product/"$i";
  printf "\n";
done

curl -X GET localhost:8082/products;
printf "\n";

echo "get individual product after name description update"
for i in `seq 1 250`;
do
  curl -X GET localhost:8082/product/"$i";
  printf "\n";
done


curl -X GET localhost:8082/products;
printf "\n";

echo "creating orders"
for i in `seq 1 65`;
do
  prod="[$((i + 1)), $((i + 3)) , $((i + 5))]"
  curl -X POST -H "Content-Type: application/json" -d  "{\"User\": $i,\"Product\": $prod,\"Address\": \"xyz\" }" localhost:8083/order/;
  printf "\n";
done

echo "deleting products"
for i in `seq 10 15`;
do
  curl -X DELETE localhost:8082/product/"$i";
  printf "\n";
done

echo "updating orders product"
for i in `seq 1 9`;
do
  prod="[$((i + 2)), $((i + 3)) , $((i + 6))]"
  curl -X PATCH -H "Content-Type: application/json" -d  "{\"Product\": $prod }" localhost:8083/order/"$i"/product;
  printf "\n";
done

echo "updating orders status"
for i in `seq 9 18`;
do
  curl -X PATCH -H "Content-Type: application/json" -d  "{\"Status\": \"ORDER_ON_ROUTE\"}" localhost:8083/order/"$i"/status;
  printf "\n";
done

echo "updating orders status"
for i in `seq 18 25`;
do
  curl -X PATCH -H "Content-Type: application/json" -d  "{\"Status\": \"ORDER_DELIVERED\"}" localhost:8083/order/"$i"/status;
  printf "\n";
done

echo "updating orders address"
for i in `seq 1 25`;
do
  address="$i street, xyz  $((i + 3))$((i + 1))$((i + 2))$((1 + 9))"
  curl -X PATCH -H "Content-Type: application/json" -d  "{\"Address\": \"$address\" }" localhost:8083/order/"$i"/address;
  printf "\n";
done

echo "deleting orders"
for i in `seq 1 5`;
do
  curl -X DELETE  localhost:8083/order/"$i";
  printf "\n";
done

