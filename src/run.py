import asyncio
import multiprocessing
from ipc import init_ipc_queues
from audio_worker import audio_worker
import server

if __name__ == "__main__":
    audio_queue, result_queue = init_ipc_queues()  # Инициализация очередей для IPC

    # Запуск воркера в отдельном процессе
    worker_process = multiprocessing.Process(
        target=audio_worker,
        args=(audio_queue, result_queue),
        daemon=True
    )
    worker_process.start()

    # Передача очередей в сервер и запуск сервера
    server.audio_queue = audio_queue
    server.result_queue = result_queue

    print("Сервис запущен. WebSocket-сервер на ws://localhost:8765/")
    asyncio.run(server.main(host="localhost", port=8765))
