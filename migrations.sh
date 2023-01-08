#!/bin/bash


usage() {
  cat << USAGE >&2
    Options:
        --help                      for help
    Commands:
        run                         to run pending migrations
        revert                      to revert last run migration
USAGE
  exit 1
}

run(){
    docker exec -it order-service-container sh -c "cd src ; alembic upgrade head"
}

revert(){
    docker exec -it order-service-container sh -c "cd src ; alembic downgrade -1"
}

if [ "$1" == "--help" ];
then
    usage
    
else
    if [ -n "$1" ];
    then
        case $1 in
        "run")
            run
            ;;
        "revert")
            revert
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