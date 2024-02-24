from celery import Celery

celery = Celery('failures_search_user_log', broker='redis://localhost:6379/12')

def insert_failure_in_db(failure_data):
    file_name = "failures_search_user_log.csv"
    with open(file_name, mode='a', encoding='utf-8') as file:
        file.write(failure_data + "\n")

@celery.task
def registrar_falla_en_busqueda(failure_data):
    insert_failure_in_db(failure_data)
