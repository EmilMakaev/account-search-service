from clickhouse_driver import Client
from variables import *

def create_and_fill_table():
  clickhouse_client = Client(host=CH_HOST, port=CH_PORT, user=CH_USER, password=CH_PASSWORD, database=CH_DATABASE)

  clickhouse_client.execute('''
      CREATE TABLE IF NOT EXISTS default.user_list_table (
          username String,
          ipv4 String,
          mac String
      ) ENGINE = MergeTree
      ORDER BY username;
  ''')

  # Check if the table is empty
  clickhouse_table_count = clickhouse_client.execute('SELECT COUNT(*) FROM default.user_list_table')

  # If the table is empty, insert the data
  if clickhouse_table_count[0][0] == 0:
    clickhouse_client.execute('''
      INSERT INTO default.user_list_table (username, ipv4, mac) 
        SELECT
          hex(256 * rand()) as username,
          toString(IPv4NumToString(rand())) as ipv4,
          concat(hex(256 * rand()), ':', hex(256 * rand()), ':', hex(256 * rand()), ':', hex(256 * rand()), ':', hex(256 * rand()), ':', hex(256 * rand())) as mac
        FROM system.numbers LIMIT 100
    ''')