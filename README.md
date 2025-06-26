# WebSocket сервис для mock-транскрипции аудио

## Описание

Этот проект реализует локальный WebSocket-сервис на Python 3.10+, который:
- Принимает бинарные аудио-чанки от клиентов
- Передаёт их в отдельный процесс-воркер через очередь (IPC)
- Получает от воркера mock-транскрипты (имитация распознавания)
- Возвращает транскрипты клиентам в формате JSON

## Архитектура

- **WebSocket-сервер** (асинхронный, поддерживает несколько клиентов)
- **IPC**: две очереди (`audio_queue`, `result_queue`) для обмена между сервером и воркером
- **Воркер**: отдельный процесс, имитирует обработку аудио и возвращает mock-результат

## Структура проекта

```
src/
├── run.py           # Точка входа, orchestration
├── server.py        # WebSocket-сервер
├── auto_worker.py        # Обработчик аудио (воркер)
├── ipc.py           # IPC: очереди, структуры обмена
```

## Установка и запуск

1. **Создайте виртуальное окружение:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Запустите сервис:**
   ```bash
   python3 src/run.py
   ```
   Вы увидите сообщение:
   ```
   Сервис запущен. WebSocket-сервер на ws://localhost:8765/
   ```

4. **Запустите параллельно тестовый клиент:**
    ```bash
    python3 test_client.py
    ```

## Пример тестового клиента

```python
import asyncio
import websockets

async def test():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send(b"test audio chunk")
        response = await websocket.recv()
        print("Ответ от сервера:", response)

asyncio.run(test())
```

## Формат сообщений

- **Клиент → сервер:** бинарные данные (аудио-чанк)
- **Сервер → клиент:**
  - Успех: `{ "client_id": "...", "transcript": "Это mock-транскрипция" }`
  - Ошибка: `{ "error": "Ожидался бинарный аудио-чанк." }`
