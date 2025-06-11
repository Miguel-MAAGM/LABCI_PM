import asyncio
import websockets
import serial
import struct
import json

async def usb_to_ws(websocket):
    try:
        ser = serial.Serial('COM25', baudrate=115200, timeout=1)
        print("[INFO] Puerto COM25 abierto")
    except Exception as e:
        print(f"[ERROR] No se pudo abrir COM25: {e}")
        return

    N = 100
    try:
        while True:
            data = ser.read(2 * N * 2)
            if len(data) == 2 * N * 2:
                values = struct.unpack('<' + 'H' * 2 * N, data)
                ch1 = values[0::2]
                ch2 = values[1::2]
                payload = json.dumps({'ch1': ch1, 'ch2': ch2})
                await websocket.send(payload)
            await asyncio.sleep(0.1)
    except websockets.exceptions.ConnectionClosed:
        print("[INFO] Cliente WebSocket desconectado.")
    finally:
        ser.close()
        print("[INFO] Puerto COM25 cerrado.")

async def main():
    async with websockets.serve(usb_to_ws, "localhost", 8765):
        print("[INFO] WebSocket en ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
