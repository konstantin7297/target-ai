import time
from multiprocessing import Queue

def audio_worker(audio_queue: Queue, result_queue: Queue):
    """
    Обработчик аудио-чанков: получает чанки, имитирует распознавание и отправляет результат.
    """
    while True:
        if audio_queue.empty():
            time.sleep(0.01)
            continue

        item = audio_queue.get()
        client_id = item.get('client_id')
        time.sleep(0.2)  # Имитация обработки (можно добавить задержку)
        transcript = "Это mock-транскрипция"  # audio_chunk = item.get('audio_chunk')  # Не используется в mock
        
        result_queue.put({
            'client_id': client_id,
            'transcript': transcript
        })
