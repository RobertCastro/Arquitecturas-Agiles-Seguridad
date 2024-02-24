from celery import Celery

# Create a Celery instance
celery = Celery('tasks1', broker='redis://localhost:6379/3')


def insert_user_in_db(email):
    file_name = "database/usuarios_db.csv"

    # Open the file in write mode ("w")
    with open(file_name, mode='a', encoding='utf-8') as file:
        # Write content into the file
        file.write(email + ";redundancia1" + "\n")
        # raise Exception("Falla a proposito. "+email)


# Define a Celery task
@celery.task(name="queues.queue_user_registration_service_redundancia2.registrar_usuario_redundancia1")
def registrar_usuario_redundancia1(email):
    insert_user_in_db(email)
