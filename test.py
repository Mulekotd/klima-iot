import requests
import time

# URL base para o servidor Uvicorn local
BASE_URL = "http://127.0.0.1:8000/api"

def test_telemetry():
    """Realiza uma requisição GET para buscar dados dos sensores."""
    print("-> Início do Teste: GET /telemetry")
    try:
        response = requests.get(f"{BASE_URL}/telemetry", timeout=1.5)
        # Lança exceção para erros HTTP (4XX ou 5XX)
        response.raise_for_status()
        
        data = response.json()
        print("Status Code:", response.status_code)
        print("Payload Recebido:", data)
        
    except requests.exceptions.RequestException as e:
        print(f"Falha na requisição de telemetria: {e}")

def test_control():
    """Realiza uma requisição POST para enviar um comando ao hardware."""
    print("\n-> Início do Teste: POST /control")
    
    # O payload espelha o modelo Pydantic do simulador
    payload = {
        "power": True,
        "target_temperature": 25.5,
        "timer_minutes": 60,
        "reset_filter": False
    }
    
    try:
        # The json parameter serializes the payload and sets Content-Type automatically
        response = requests.post(f"{BASE_URL}/control", json=payload, timeout=1.5)
        response.raise_for_status()
        
        print("Status Code:", response.status_code)
        print("Server Response:", response.json())
        
    except requests.exceptions.HTTPError as e:
        # Specific capture for randomly forced 504 timeout error from the API
        print(f"HTTP error from server: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_telemetry()
    time.sleep(1)  # Pause to make console output easier to read
    test_control()