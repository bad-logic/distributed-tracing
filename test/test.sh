
order="localhost:8083/order/"
product="localhost:8082/product"

if [ ! -x $(which curl)  ];then
        echo "Please install curl command to execute the task"
        exit 1
fi

for i in `seq 1 20`;
do $(which curl) -s -X POST -d  @$PWD/product.json ${product} -H 'Content-Type: application/json';
done

for i in `seq 1 4`;
do $(which curl) -s -X POST -d  @$PWD/order.json ${order} -H 'Content-Type: application/json';
done


