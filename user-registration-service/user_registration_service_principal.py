from celery import Celery
#celery -A user_registration_service_principal.celery worker --loglevel=info
# Create a Celery instance
celery = Celery('tasks', broker='redis://localhost:6379/0')

def insert_user_in_db(email):
    file_name = "usuarios_db.csv"

    # Open the file in write mode ("w")
    with open(file_name, mode='a', encoding='utf-8') as file:
        # Write content into the file
        file.write(email+";principal"+"\n")
        #raise Exception("Falla a proposito. "+email)

# Define a Celery task
@celery.task
def registrar_usuario_principal(email):
    insert_user_in_db(email)