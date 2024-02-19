import redis
import json
from threading import Thread
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define SQLAlchemy engine and session
engine = create_engine('sqlite:///usuarios.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Define SQLAlchemy base model
Base = declarative_base()

# Define Usuario model
class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))

# Create the table in the database
Base.metadata.create_all(engine)

# Connect to Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Subscribe to the 'cola-comando' channel
p = r.pubsub()
p.subscribe('cola-comando')

# Function to handle incoming messages
def handle_message(message):
    if message['type'] == 'message':
        data = json.loads(message['data'].decode('utf-8'))
        print(f"Received JSON data: {data}")
        # Call the registrar_usuario function
        registrar_usuario(data['usuario'])

# Function to register a new user
def registrar_usuario(nombre_usuario):
    usuario = Usuario(nombre=nombre_usuario)
    session.add(usuario)
    session.commit()
    print('Usuario registrado con éxito')

# Listen for incoming messages in a separate thread
for message in p.listen():
    handle_message(message)