#!/usr/bin/env sh

echo "Executing......"

for entry in ./bin/*;
do
  echo "$entry"
done

echo "Starting appp...."
exec "$@"