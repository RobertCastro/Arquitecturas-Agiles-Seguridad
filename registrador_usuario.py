import redis
import json



# Connect to Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Subscribe to the 'cola-comando' channel
p = r.pubsub()
p.subscribe('cola-comando')

# Listen for incoming messages
for message in p.listen():
    if message['type'] == 'message':
        data = json.loads(message['data'].decode('utf-8'))
        print(f"Received JSON data: {data}")
