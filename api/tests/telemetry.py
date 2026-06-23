import os
import requests


def get_base_url():
    try:
        return os.environ["BASE_URL"].rstrip("/")
    except KeyError:
        raise SystemExit(
            "Defina a variável de ambiente BASE_URL antes de executar este teste."
        ) from None


BASE_URL = get_base_url()

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
