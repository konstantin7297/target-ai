import asyncio
import websockets

async def test(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send(b"test audio chunk")  # Отправляем бинарный аудио-чанк (например, просто байты)
        response = await websocket.recv()  # Получаем ответ
        print("Ответ от сервера:", response)

asyncio.run(test("ws://localhost:8765"))