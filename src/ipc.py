from typing import Tuple
from multiprocessing import Queue

# Очередь для передачи аудио-чанков от сервера к воркеру
def create_audio_queue() -> Queue:
    """Создать очередь для аудио-чанков."""
    return Queue()

# Очередь для передачи результатов от воркера к серверу
def create_result_queue() -> Queue:
    """Создать очередь для результатов транскрипции."""
    return Queue()

# Вспомогательная функция для инициализации обеих очередей
def init_ipc_queues() -> Tuple[Queue, Queue]:
    """Создать и вернуть обе очереди для IPC."""
    return create_audio_queue(), create_result_queue()
