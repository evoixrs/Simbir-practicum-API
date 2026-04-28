# Simbir Practicum API

API-автотесты для локального тестового стенда `test-service`.

## Что в проекте

- `pytest` + `requests`
- `pydantic`-модели для десериализации ответов
- API-клиент для ручек сервиса
- `Allure`-отчеты
- параллельный запуск через `pytest-xdist`
- запуск в GitHub Actions с публикацией Allure в GitHub Pages

## Структура

- [docs/test_cases.md](docs/test_cases.md) — тест-кейсы
- `api_client/` — API-клиент, endpoints, модели и payload
- `helpers/` — Allure-вложения, проверки и десериализация ответов
- `tests/` — API-тесты
- `pytest.ini` — настройки pytest
- `requirements.txt` — зависимости проекта

## Запуск стенда

Тестовый стенд должен быть доступен по адресу:

```text
http://localhost:8080
```

Swagger-документация:

```text
http://localhost:8080/api/_/docs/swagger/
```

## Запуск тестов

Обычный запуск:

```bash
pytest
```

Запуск с явным адресом стенда:

```bash
pytest --base-url=http://localhost:8080
```

Запуск отдельного теста:

```bash
pytest tests/test_create_entity.py
```

## Allure

Сгенерировать локальный отчет:

```bash
pytest
allure generate allure-results --clean -o allure-report
```
Открыть локальный отчет:

```bash
allure open allure-report
```

## CI

В GitHub Actions настроены:

- запуск тестового стенда
- установка зависимостей
- запуск API-тестов
- генерация Allure-отчета
- публикация отчета в GitHub Pages
