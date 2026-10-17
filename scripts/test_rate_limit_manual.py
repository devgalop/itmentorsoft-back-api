"""Script para probar rate limiting manualmente.

Hace múltiples requests al endpoint de login y verifica:
1. Headers de rate limit (X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset)
2. HTTP 429 cuando se excede el límite
3. Header Retry-After en respuesta 429

Uso:
    .venv\\Scripts\\python.exe scripts/test_rate_limit_manual.py

Requisitos:
    - Docker corriendo con: docker-compose up postgres valkey api
    - Endpoint de login accesible en http://localhost:8000/users/login
"""

import httpx
import time

BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = "/users/sessions"
NUM_REQUESTS = 120


def test_rate_limit():
    """Hace N requests al login y muestra el comportamiento del rate limiter."""
    print(f"🧪 Probando rate limiting en {BASE_URL}{LOGIN_ENDPOINT}")
    print(f"📊 Enviando {NUM_REQUESTS} requests consecutivos...\n")
    print("-" * 80)

    payload = {"email": "test@example.com", "password": "wrong_password"}  # nosec

    with httpx.Client(timeout=10.0) as client:
        for i in range(1, NUM_REQUESTS + 1):
            try:
                response = client.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json=payload)

                # Extraer headers de rate limit
                limit = response.headers.get("X-RateLimit-Limit", "N/A")
                remaining = response.headers.get("X-RateLimit-Remaining", "N/A")
                reset = response.headers.get("X-RateLimit-Reset", "N/A")
                retry_after = response.headers.get("Retry-After", "N/A")

                # Mostrar resultado
                status_emoji = (
                    "✅"
                    if response.status_code == 200
                    else "⚠️" if response.status_code == 401 else "🚫"
                )
                print(f"\n{status_emoji} Request #{i}")
                print(f"   Status: {response.status_code}")
                print(f"   X-RateLimit-Limit: {limit}")
                print(f"   X-RateLimit-Remaining: {remaining}")

                if reset != "N/A":
                    reset_time = time.strftime("%H:%M:%S", time.localtime(int(reset)))
                    print(f"   X-RateLimit-Reset: {reset} ({reset_time})")

                if retry_after != "N/A":
                    print(f"   Retry-After: {retry_after} segundos")
                    print("   🔴 RATE LIMIT EXCEDIDO - Request bloqueado")

                # Si recibimos 429, mostrar el body también
                if response.status_code == 429:
                    print(f"   Body: {response.json()}")

            except httpx.RequestError as e:
                print(f"\n❌ Request #{i} - Error de conexión: {e}")
                print(f"   ¿Está corriendo la app en {BASE_URL}?")
                break

    print("\n" + "=" * 80)
    print("✅ Prueba completada")
    print("\n📝 Resultados esperados:")
    print(
        "   - Requests 1-5: Status 401 (credenciales inválidas) con headers de rate limit"
    )
    print("   - Request 6+: Status 429 (Too Many Requests) con Retry-After")
    print("   - X-RateLimit-Remaining debería decrementar: 4, 3, 2, 1, 0")
    print("\n💡 Si no ves 429, revisá:")
    print("   1. RATE_LIMIT_ENABLED=true en .env")
    print("   2. Valkey está corriendo: docker ps | grep valkey")
    print("   3. La app está usando la rama feature/rate-limit")


if __name__ == "__main__":
    test_rate_limit()
