from create_and_fill_table import create_and_fill_table
import redis
import json
from search_and_send_to_external_service import search_and_send_to_external_service

def main():
    create_and_fill_table()
    redis_client = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)

    while True:
        task = redis_client.brpop('queue:search_task', timeout=1)

        print("Waiting redis tasks")
        print(task)

        if task:
            try:
                task = json.loads(task[1])
                search_and_send_to_external_service(task)
            except Exception as e:
                print(f"Error processing task: {e}")
        else:
            print("No tasks in the queue...")

if __name__ == "__main__":
    main()