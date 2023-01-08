#!/bin/bash

# docker containers
# kafka related
zk=zookeeper1
kfk=kafka1
kuis=kafka-ui-service
# logging related
jaegr=jaeger-container
zpkn=zipkin-container
otlcl=otel-collector-container
# fltc=fluentd-container
# application related
prods=product-service-container
prodsdb=products-db-container
ord=order-service-container
orddb=orders-db-container
cns=consumer-service-node-container
# ccs=consumer-service-cpp-container


kf=("zookeeper1" "kafka1" "kafka-ui-service")
lg=("jaeger-container","zipkin-container","otel-collector-container")

start_kafka(){
    docker-compose -f deploy/kafka-compose.yaml up --build 
}

start_logs(){
    docker-compose -f deploy/logs-compose.yaml up --build 
}

start_app(){
    docker-compose -f deploy/docker-compose.yaml up --build
}

start_kafka &
kafka_active=false
while [ $kafka_active == false ];
do
    kafka_active=true
    for i in "${kf[@]}"
    do
        if [ $kafka_active == true ];
        then
            kafka_active=$(docker container inspect -f '{{.State.Running}}' $i)
        fi
    done
done
echo "done with kafkas..."
start_logs &
logs_active=false
while [ $logs_active == false ];
do
    logs_active=true
    for i in "${lg[@]}"
    do
        if [ $logs_active == true ];
        then
            logs_active=$(docker container inspect -f '{{.State.Running}}' $i)
        fi
    done
    echo $logs_active
done
echo "done with logs..."
start_app &
wait