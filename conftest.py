import os

# Ensure mandatory env vars exist before any test module is imported.
# itmentorsoft_persistence reads DATABASE_URL at import time (module scope),
# so without these defaults, test collection fails with a KeyError.
_TEST_ENV_DEFAULTS = {
    "DATABASE_URL": "postgresql+asyncpg://test:test@localhost:5432/test",
    "JWT_SECRET_KEY": "test-secret-key",
    "JWT_ALGORITHM": "HS256",
    "JWT_EXPIRATION_DELTA_SECONDS": "1800",
    "RANDOM_TOKEN_EXPIRATION_DELTA_SECONDS": "1800",
    "REFRESH_TOKEN_EXPIRATION_DELTA_SECONDS": "604800",
    "DB_POOL_SIZE": "5",
    "DB_MAX_OVERFLOW": "10",
    "DB_POOL_TIMEOUT": "30",
    "DB_POOL_RECYCLE": "3600",
}

for key, value in _TEST_ENV_DEFAULTS.items():
    os.environ.setdefault(key, value)
