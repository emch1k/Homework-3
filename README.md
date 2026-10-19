# ДЗ-3: асинхронность в Python

## Запуск

```bash
uvicorn main:app --reload
```

Документация и тестирование запросов: http://127.0.0.1:8000/docs

## Эндпоинт `POST /calculate/`

Пример запроса:

```json
{
  "numbers": [5, 3, 10],
  "delays": [1, 2, 0.5]
}
```

Пример ответа:

```json
{
  "results": [
    {"number": 5, "square": 25, "delay": 1, "time": 1.0},
    {"number": 3, "square": 9, "delay": 2, "time": 2.0},
    {"number": 10, "square": 100, "delay": 0.5, "time": 0.5}
  ],
  "total_time": 2.0,
  "parallel_faster_than_sequential": true
}
```

Если длины списков `numbers` и `delays` не совпадают, сервер вернёт ошибку 400.
