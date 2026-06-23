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

def test_control():
    """Realiza uma requisição POST para enviar um comando ao hardware."""
    print("\n-> Início do Teste: POST /control\n")
    
    # O payload espelha o modelo Pydantic do simulador
    payload = {
        "power": True,
        "target_temperature": 25.5,
        "timer_minutes": 60,
        "reset_filter": False
    }
    
    try:
        # O parâmetro json serializa o payload e define automaticamente o Content-Type
        response = requests.post(f"{BASE_URL}/control", json=payload, timeout=1.5)
        response.raise_for_status()
        
        print("[.] Status Code:", response.status_code)
        print("[.] Server Response:\n", response.json())
        
    except requests.exceptions.HTTPError as e:
        # Captura específica para o erro 504 de timeout forçado aleatoriamente pela API
        print(f"[!] Erro HTTP do servidor: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Falha na conexão: {e}")

if __name__ == "__main__":
    test_control()
