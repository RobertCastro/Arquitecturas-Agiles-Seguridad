import requests
import csv
from datetime import datetime
import os

url = 'http://localhost:5000/login'
n_requests = 100

login_data_template = {
    "username": "robert@gmail.com",
    "password": "Password1&",
    "code": "424496"
}

xss_scripts = [
    "<script>alert('XSS1')</script>",
    "onmouseenter=alert(3)",
    "setTimeout('alert(5)', 0)",
    "<script>alert('')</script>",
    "onload=alert(3)",
    "javascript:void(window.alert('XSS5'))"
]

csv_file_name = 'pruebas_experimento/resultados_experimentos/experimento_integridad_001_XSS.csv'

if not os.path.exists('resultados_experimentos'):
    os.makedirs('resultados_experimentos')

csv_headers = ['fecha', 'nombre_experimento', 'categoria', 'id_request', 'request', 'request_response', 'tipo_resultado', 'resultado_esperado', 'resultado_obtenido', 'LOGIN_LIMITER_MAX']

with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    writer.writerow(csv_headers)

    for i in range(n_requests):
        malicious_username = f"robert{xss_scripts[i % len(xss_scripts)]}@gmail.com"
        login_data = login_data_template.copy()
        login_data['username'] = malicious_username
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.post(url, json=login_data, headers=headers)

        csv_data = [
            datetime.now().strftime('%d/%m/%Y'),
            'experimento_integridad_001_XSS',
            'integridad', 
            i + 1,
            str(login_data),
            response.text,
            'status_code',
            400,
            response.status_code,
            1
        ]

        writer.writerow(csv_data)
        print(f"Request {i + 1}: Status Code = {response.status_code}, Response = {response.text}")
