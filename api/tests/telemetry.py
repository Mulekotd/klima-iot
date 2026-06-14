import requests

# URL base para o servidor Uvicorn local
BASE_URL = "http://127.0.0.1:8000/api"

def test_telemetry():
    """Realiza uma requisição GET para buscar dados dos sensores."""
    print("\n-> Início do Teste: GET /telemetry\n")
    try:
        response = requests.get(f"{BASE_URL}/telemetry", timeout=1.5)
        # Lança exceção para erros HTTP (4XX ou 5XX)
        response.raise_for_status()
        
        data = response.json()
        print("[.] Status Code:", response.status_code)
        print("[.] Payload Recebido:\n", data)
        
    except requests.exceptions.RequestException as e:
        print(f"[!] Falha na requisição de telemetria: {e}")

if __name__ == "__main__":
    test_telemetry()
