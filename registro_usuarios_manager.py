import redis
import json

# Connect to Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Publish messages to the 'channel' channel
contador=0
while contador<10:
    usuario = input("Nombre Usuario a Registrar: ")
    
    message = json.dumps({'comando':'registrar_usuario','usuario': usuario})
    r.publish('cola-comando', message)
    contador+=1