import os

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
CH_HOST = os.getenv('CLICKHOUSE_HOST', 'localhost')
CH_PORT = os.getenv('CLICKHOUSE_PORT', '9000')
CH_USER = os.getenv('CLICKHOUSE_USER', 'default')
CH_PASSWORD = os.getenv('CLICKHOUSE_PASSWORD', '')
CH_DATABASE = os.getenv('CLICKHOUSE_DATABASE', 'default')

EXTERNAL_SERVICE_URL = 'https://pastebin.com/'
