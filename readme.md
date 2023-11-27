## Real-time analytics
### Postgres -> Kafka -> MongoDB

### To run:

`bash run.sh`

### Useful commands:
#### Connect to postgres:
`docker exec -it postgres psql -U postgres_admin -d postgres_database`
`select * from sample_table;`
Insert new values to see the changes in mongodb
`INSERT INTO sample_table (name) VALUES
    ('Postgres Item 1'),
    ('Postgres Item 2'),
    ('Postgres Item 3');`

#### Connect to mongodb:
`docker exec -it mongo  mongosh --host localhost --port 27017 --username mongo_admin --password mongo_admin_password --authenticationDatabase mongo_database`

`use mongo_database`
`db.aggregated_results.find()`

#### Connect to kafka:
List all the topics
`docker exec -it kafka kafka-topics.sh --bootstrap-server kafka:9092 --list`

Check what topic is receiving:
`docker exec -it kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 -topic postgres.public.sample_table --from-beginning`

### How to check the execution
1. Run the application
2. In a new terminal, connect to postgres database
3. In a new terminal, connect to mongo database
4. Read aggregated_results collection from mongo database, while inserting new values into sample_table in the postgres database. The collection shows the number of new records added to postgres database within a window of 10 seconds.