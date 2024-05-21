from clickhouse_driver import Client
from create_and_fill_table import create_and_fill_table
import redis
import json
import requests
from multiprocessing import Pool
from variables import *

def process_queue(item):
    clickhouse_client = Client(host=CH_HOST, port=CH_PORT, user=CH_USER, password=CH_PASSWORD, database=CH_DATABASE)
    task = json.loads(item)
    ipv4, mac = task['ipv4'], task['mac']

    print(f"Redis task: {task}")

    query = f"SELECT * FROM default.user_list_table WHERE ipv4 = '{ipv4}' AND mac = '{mac}' LIMIT 1"
    result = clickhouse_client.execute(query)

    if result:
        username = result[0][0]
        data = {'ipv4': ipv4, 'mac': mac, 'username': username}

        response = requests.post(EXTERNAL_SERVICE_URL, json=data)

        print(response.status_code)
        
        if response.status_code == 200:
            with open('successful_searches.txt', 'a') as file:
                file.write(response.url + '\n')
            print(f"Successfully sent data for username {username} to external service!")
        else:
            print(f"Failed to send data for username {username} to external service")

def main():
    create_and_fill_table()
    
    redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    
    redis_queue = "queue:search_task"
    queue_items = redis_client.lrange(redis_queue, 0, -1)
    num_processes = 2

    with Pool(num_processes) as pool:
        pool.map(process_queue, queue_items)

if __name__ == "__main__":
    main()