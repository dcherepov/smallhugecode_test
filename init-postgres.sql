-- init.sql

-- Create a sample table
CREATE TABLE IF NOT EXISTS sample_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Set correct replica type to make debezium show the diff
ALTER TABLE public.sample_table REPLICA IDENTITY FULL;

-- Insert some sample data
INSERT INTO sample_table (name) VALUES
    ('Postgres Item 1'),
    ('Postgres Item 2'),
    ('Postgres Item 3');
