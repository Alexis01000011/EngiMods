# 0001. Stack base

- Estado: Aceptada
- Fecha: 2026-11-03
- Historia: EM-001

## Contexto

El equipo ya decidió usar Django. Varias personas trabajarán en paralelo, algunas a través de agentes de código, así que el entorno debe ser reproducible y la verificación automática.

## Decisión

- **Django 5.2 LTS** en lugar de la versión más reciente (6.1). Es versión con soporte extendido hasta abril de 2028 según el calendario de Django, lo que cubre el piloto y la operación posterior sin migraciones de versión forzadas.
- **Python 3.12+.**
- **uv** para dependencias y entorno virtual, con `uv.lock` versionado: todos instalan exactamente lo mismo con `uv sync`.
- **django-environ** para leer configuración de variables de entorno y `DATABASE_URL`.
- **SQLite** en desarrollo, **PostgreSQL** en producción.
- **pytest + pytest-django** para pruebas y **ruff** para lint y formato.
- **GitHub Actions** corre lint, formato, chequeo de migraciones y pruebas en cada PR.
- Plantillas de Django en el servidor, sin frontend separado. El enfoque de estilos queda abierto (EM-004).

## Consecuencias

- Un solo comando reproduce el entorno; la CI atrapa errores de agentes y personas por igual.
- Pasar a Django 6.x más adelante es posible y se registrará en un nuevo ADR.
- Diferencias entre SQLite y PostgreSQL pueden aparecer; el entorno de staging (EM-005) usa PostgreSQL para detectarlas.
