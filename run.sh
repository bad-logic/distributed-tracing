#!/bin/bash
################################################################
#
# Author: RB
# Version 1
# This script is used for running container apps
#
################################################################

usage(){
  cat << EOF

  Usage: bash run.sh

   Options:
           --h                         for help
       Commands:
           start                       start the applications
           stop                        stop the applications
EOF
}

external_networks=("dstrace_kafka_network" "dstrace_log_network")

create_external_network(){
  for i in "${external_networks[@]}"
      do
         if docker network ls | grep "$i"; then
              echo "network already exists"
          else
              docker network create "$i"
              echo "✔ $i created"
        fi
      done
}

delete_external_network(){
  for i in "${external_networks[@]}"
      do
         if docker network ls | grep "$i"; then
           docker network rm "$i"
           echo "✔ $i deleted"
        else
          echo "network already exists"
        fi
      done
}

start_kafka(){
    docker compose -f deploy/kafka-compose.yaml up --build -d
    echo "✔ kafka infrastructure setup complete"
}

stop_kafka(){
    docker compose -f deploy/kafka-compose.yaml down
    echo "✔ kafka infrastructure destroyed"
}

start_logs(){
    docker compose -f deploy/logs-compose.yaml up --build -d
    echo "✔ logging infrastructure setup complete"
}

stop_logs(){
    docker compose -f deploy/logs-compose.yaml down
    echo "✔ logging infrastructure destroyed"
}

start_app(){
    docker compose -f deploy/docker-compose.yaml up --build -d
    echo "✔ started application in detached mode"
}

stop_app(){
    docker compose -f deploy/docker-compose.yaml down
    echo "✔ application containers stopped"
}

start(){
  create_external_network
  start_kafka
  start_logs
  start_app
}

stop(){
  stop_app
  stop_logs
  stop_kafka
  delete_external_network
  echo "✔ stopped the application"
}

test(){
  bash test/test.sh
}

if [ "$1" == "--h" ];
then
    usage
else
  if [ -n "$1" ];
      then
          case $1 in
          "start")
              start
              ;;
          "stop")
              stop
              ;;
          *)
              echo "unknown command $1"
              usage
              ;;
          esac
      else
          echo "unknown command $1"
          usage
      fi

fi