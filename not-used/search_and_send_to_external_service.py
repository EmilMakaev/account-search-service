from clickhouse_driver import Client
import requests

import os

external_service_url = 'https://pastebin.com/'

def search_and_send_to_external_service(task):
    clickhouse_client = Client(host=CH_HOST, port=CH_PORT, user=CH_USER, password=CH_PASSWORD, database=CH_DATABASE)
    ipv4, mac = task['ipv4'], task['mac']
    
    query = f"SELECT username FROM user_list_table WHERE ipv4 = '{ipv4}' AND mac = '{mac}' LIMIT 1"
    result = clickhouse_client.execute(query)

    if result:
        username = result[0][0]
        data = {'ipv4': ipv4, 'mac': mac, 'username': username}
        print(data)

        response = requests.post(external_service_url, json=data)
        
        if response.status_code == 200:
            with open('successful_searches.txt', 'a') as file:
                file.write(response.url + '\n')
            print(f"Successfully sent data for username {username} to external service!")
        else:
            print(f"Failed to send data for username {username} to external service")