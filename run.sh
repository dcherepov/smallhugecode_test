#!/bin/bash

docker compose up &
(
    CONTAINER_NAME="debezium"
    # Check if the container is running
    while [ "$(docker inspect -f '{{.State.Status}}' $CONTAINER_NAME 2>/dev/null)" != "running" ]; do
        sleep 1
    done

    # Wait some time more to start completely and pass the connector parameters
    sleep 30
    curl -H 'Content-Type: application/json' localhost:8083/connectors --data @postgres-connector.json
)