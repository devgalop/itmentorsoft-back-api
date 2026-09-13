# Plan de Pruebas — itmentorsoft

## Estado Actual

| Métrica | Valor |
|---------|-------|
| Tests colectados | 482 |
| Errores de import | 63 (dependencia privada `itmentorsoft_persistence`) |
| Cobertura de línea | 96.2% (reportada) |
| Cobertura de rama | 0% (no configurada) |
| Framework | pytest + pytest-asyncio + pytest-cov |

---

## Plan de Mejora de Cobertura

### FASE 1 — Tests Unitarios Críticos (Prioridad ALTA)

Módulos sin ninguna cobertura que son **críticos para la seguridad y estabilidad**:

| Módulo | Tipo de test | Complejidad |
|--------|-------------|-------------|
| `infrastructure/security/jwt_token_generator.py` | Unit tests: generación, validación, expiración, tokens malformados | Media |
| `infrastructure/security/simple_otp_generator.py` | Unit tests: generación, validación, expiración | Baja |
| `features/user_management/login/` | Handler + Service con mocks de repo y security | Media |
| `features/user_management/refresh_token/` | Handler + Service: token rotation, expired tokens | Media |
| `features/user_management/recovery_password/` | Handler + Service: flujo completo de recuperación | Media |
| `features/user_management/resend_otp/` | Handler + Service: reenvío OTP, rate limiting | Baja |
| `features/assessments/evaluate/` | Service: lógica de evaluación, scoring, edge cases | Alta |
| `main.py` | App startup, lifespan, exception handlers, router registration | Media |

### FASE 2 — Tests de Integración (Prioridad ALTA)

Puntos de integración con servicios externos que necesitan **tests con dependencias reales o test containers**:

| Integración | Estrategia | Qué probar |
|-------------|-----------|------------|
| **PostgreSQL** (repositorios) | SQLite in-memory para unit, PostgreSQL real para integración | CRUD operations, transacciones, constraints, queries complejos |
| **Valkey/Redis** (cache) | Mock para unit, test container para integración | Set/get/delete, TTL, serialización, error handling |
| **AWS SQS** (broker) | Mock (moto) para unit, LocalStack para integración | Publish, consume, retry, dead letter queue |
| **Brevo** (email) | Mock HTTP para unit | Template rendering, envío, error handling |
| **Groq/OpenAI** (LLM) | Mock responses para unit | Qualifier service, classifier service, timeout/retry |

### FASE 3 — Cobertura de Ramas y Edge Cases (Prioridad MEDIA)

| Acción | Detalle |
|--------|---------|
| Activar branch coverage | Agregar `branch = true` en `pyproject.toml` bajo `[tool.coverage.run]` |
| Tests de validación | Edge cases en validators: inputs vacíos, máximos, caracteres especiales |
| Error paths | Cada handler debe probar: 400, 401, 403, 404, 500 |
| Concurrent access | Tests de race conditions en operaciones críticas (assign_role, evaluate) |

### FASE 4 — Resolver los 63 Tests Rotos (Prioridad ALTA)

Los 63 tests fallan porque `itmentorsoft_persistence` no se puede instalar. Opciones:

1. **CI con GitHub token**: Configurar un PAT como secret para pip install del repo privado
2. **Mock del persistence layer**: Crear stubs/interfaces que no requieran el paquete real
3. **Test doubles**: Usar SQLite + repositorios in-memory que no dependendan de la librería privada

---

## Propuesta de CI Pipeline para PR

Pipeline robusto que se dispare en cada PR:

```yaml
# .github/workflows/pr-pipeline.yml
name: PR Pipeline

on:
  pull_request:
    branches: [main, develop]

jobs:
  lint-and-security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install ruff black bandit
      - run: ruff check src/
      - run: black --check src/
      - run: bandit -r src/ -q

  unit-tests:
    runs-on: ubuntu-latest
    needs: lint-and-security
    services:
      postgres:
        image: postgres:18
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports: ['5432:5432']
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - name: Install dependencies
        env:
          GITHUB_TOKEN: ${{ secrets.GH_PAT_FOR_PRIVATE_REPO }}
        run: |
          pip install -r requirements.txt
      - name: Run unit tests
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/test_db
        run: pytest tests/ --cov=src --cov-report=xml -m "not integration"
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage.xml

  integration-tests:
    runs-on: ubuntu-latest
    needs: lint-and-security
    services:
      postgres:
        image: postgres:18
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports: ['5432:5432']
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
      valkey:
        image: valkey/valkey:8.1
        ports: ['6379:6379']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - name: Install dependencies
        env:
          GITHUB_TOKEN: ${{ secrets.GH_PAT_FOR_PRIVATE_REPO }}
        run: pip install -r requirements.txt
      - name: Run integration tests
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/test_db
          VALKEY_HOST: localhost
          VALKEY_PORT: 6379
        run: pytest tests/ -m integration --cov=src --cov-report=xml
```

### Cambios necesarios para que funcione

| Cambio | Archivo | Detalle |
|--------|---------|---------|
| **1. PostgreSQL service** | `.github/workflows/pr-pipeline.yml` | Agregar `services: postgres` (hoy falta en `test.yml`) |
| **2. Auth para repo privado** | GitHub Secrets | Crear `GH_PAT_FOR_PRIVATE_REPO` con acceso a `itmentorsoft_persistence` |
| **3. Marcadores pytest** | `pyproject.toml` | Agregar markers: `integration`, `unit`, `slow` |
| **4. Fixtures de integración** | `tests/conftest.py` | Fixtures que levanten conexiones reales a PostgreSQL y Valkey |
| **5. Coverage thresholds** | `pyproject.toml` | Agregar `[tool.coverage.report]` con `fail_under = 80` |
| **6. Branch coverage** | `pyproject.toml` | Agregar `branch = true` en `[tool.coverage.run]` |

### Configuración recomendada para `pyproject.toml`

```toml
[tool.pytest.ini_options]
markers = [
    "unit: fast tests with mocks only",
    "integration: tests requiring external services",
    "slow: tests that take more than 5 seconds",
]

[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
fail_under = 80
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if __name__",
    "raise NotImplementedError",
]
```

---

## Resumen de Acciones

| # | Acción | Impacto | Esfuerzo |
|---|--------|---------|----------|
| 1 | Arreglar los 63 tests rotos (auth repo privado) | Desbloquea 13% de tests | Bajo |
| 2 | Agregar PostgreSQL service al CI | CI funciona de verdad | Bajo |
| 3 | Tests unitarios para security (JWT/OTP) | Seguridad crítica | Medio |
| 4 | Tests para handlers sin cobertura (login, evaluate, recovery) | Cobertura funcional | Medio |
| 5 | Tests de integración con Valkey y SQS | Confianza en infra | Alto |
| 6 | Branch coverage + thresholds | Calidad sostenida | Bajo |
| 7 | Pipeline unificado PR (lint → unit → integration) | Developer experience | Medio |
