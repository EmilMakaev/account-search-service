#!/bin/bash

clickhouse_client="docker-compose exec clickhouse-server clickhouse-client --port 9000"

# Create the table
$clickhouse_client -q "CREATE TABLE user_list_table (
    username String,
    ipv4 String,
    mac String
) ENGINE = MergeTree ORDER BY username;"

# Fill the table with generated data
$clickhouse_client -q "INSERT INTO user_list_table (username, ipv4, mac)
SELECT
    hex(256 * rand()) as username,
    toString(IPv4NumToString(rand())) as ipv4,
    concat(hex(256 * rand()), ':', hex(256 * rand()), ':', hex(256 * rand()), ':', hex(256 * rand()), ':', hex(256 * rand()), ':', hex(256 * rand())) as mac
FROM system.numbers LIMIT 10;"
