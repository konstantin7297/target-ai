import asyncio
import json
import uuid
from typing import Dict
from multiprocessing import Queue

import websockets

audio_queue = Queue()
result_queue = Queue()
clients: Dict[str, websockets.WebSocketServerProtocol] = {}  # Словарь для хранения соответствия client_id <-> websocket

async def send_results():
    """Асинхронно отправляет результаты из result_queue клиентам."""
    while True:
        if result_queue.empty():
            await asyncio.sleep(0.01)
            continue

        result = result_queue.get()
        client_id = result.get('client_id')
        transcript = result.get('transcript')
        ws = clients.get(client_id)

        if not ws:
            continue

        response = json.dumps({"client_id": client_id, "transcript": transcript}, ensure_ascii=False)  # ensure_ascii - экранирование результата

        try:
            await ws.send(response)
        except Exception:
            pass  # Клиент мог отключиться
        
async def handler(websocket):
    client_id = str(uuid.uuid4())  # Генерируем уникальный client_id
    clients[client_id] = websocket

    try:
        async for message in websocket:
            if isinstance(message, bytes):  # Помещаем аудио-чанк и client_id в очередь для обработки
                audio_queue.put({"client_id": client_id, "audio_chunk": message})

            else:  # Неожиданный тип сообщения
                error = json.dumps({"error": "Ожидался бинарный аудио-чанк."})
                await websocket.send(error)

    except websockets.ConnectionClosed:
        pass
        
    finally:
        clients.pop(client_id, None)  # Удаляем клиента при отключении

async def main(host: str, port: int):
    async with websockets.serve(handler, host, port, max_size=2**24):
        await send_results()  # Запускаем отправку результатов

if __name__ == "__main__":
    asyncio.run(main(host="localhost", port=8765))
