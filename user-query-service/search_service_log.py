from celery import Celery
import re

celery = Celery('search_service_log',
                broker='redis://localhost:6379/11',
                backend='redis://localhost:6379/11')

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def search_email_in_db(email):
    if not is_valid_email(email):
        return False 

    database = "../user-registration-service/usuarios_db.csv"
    try:
        with open(database, mode='r', encoding='utf-8') as file:
            for line in file:
                if re.search(rf"\b{email}\b", line): 
                    return True
    except IOError as e:
        print(f"Error al abrir/leer el archivo: {e}")
    return False 

@celery.task
def buscar_email_recibido(email):
    return search_email_in_db(email)
