"""
WebSocket server for streaming MPU-6050 sensor data.
Connects to Arduino serial + broadcasts to all connected clients.

Install: pip install websockets pyserial numpy
Run:     python server.py
"""

import asyncio
import json
import time
import math
import threading
import serial
import serial.tools.list_ports
import numpy as np
from collections import deque

# ─── Config ───────────────────────────────────────────────────────────────────
BAUD_RATE    = 9600
HISTORY_LEN  = 300
WS_HOST      = "0.0.0.0"
WS_PORT      = 8765
FAKE_MODE    = False

# ─── Shared state ─────────────────────────────────────────────────────────────
clients = set()
lock = threading.Lock()

latest = {"ax":0,"ay":0,"az":1,"gx":0,"gy":0,"gz":0,"temp":25.0,
          "roll":0.0,"pitch":0.0,"ts":0}

# ─── Sensor helpers ───────────────────────────────────────────────────────────
def angles_from_accel(ax, ay, az):
    """Calculate roll and pitch from accelerometer."""
    roll  = math.degrees(math.atan2(ay, az))
    pitch = math.degrees(math.atan2(-ax, math.sqrt(ay**2 + az**2)))
    return roll, pitch

def ingest(row):
    """Update latest reading."""
    global latest
    roll, pitch = angles_from_accel(row["ax"], row["ay"], row["az"])
    row["roll"] = roll
    row["pitch"] = pitch
    row["ts"] = time.time()
    with lock:
        latest = row.copy()

async def broadcast(message):
    """Send message to all connected clients."""
    if clients:
        data = json.dumps(message)
        # Create list of tasks to send to all clients
        tasks = [client.send(data) for client in clients]
        await asyncio.gather(*tasks, return_exceptions=True)

# ─── Data sources ─────────────────────────────────────────────────────────────
def fake_thread():
    """Generate synthetic sensor data."""
    t = 0.0
    while True:
        t += 0.04
        ax = 0.35 * math.sin(t * 0.9)
        ay = 0.35 * math.cos(t * 0.65)
        az = math.sqrt(max(0.0, 1.0 - ax**2 - ay**2))
        ingest({
            "ax": ax, "ay": ay, "az": az,
            "gx": 8*math.cos(t), "gy": 8*math.sin(t*0.8), "gz": 3*math.sin(t*1.3),
            "temp": 24.5 + 0.1*math.sin(t*0.1)
        })
        time.sleep(0.025)

def serial_thread(port):
    """Read from Arduino serial port."""
    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=1)
        print(f"[serial] connected → {port}")
        time.sleep(2)
        while True:
            try:
                raw = ser.readline().decode("utf-8", errors="ignore").strip()
                parts = [p for p in raw.split("\t") if p]
                if len(parts) >= 8:
                    ingest({
                        "ax": float(parts[1]), "ay": float(parts[2]),
                        "az": float(parts[3]), "gx": float(parts[4]),
                        "gy": float(parts[5]), "gz": float(parts[6]),
                        "temp": float(parts[7])
                    })
            except (ValueError, IndexError):
                pass
    except Exception as e:
        print(f"[serial] connection failed: {e} → fake mode")
        fake_thread()

# ─── WebSocket handler ─────────────────────────────────────────────────────────
async def handler(websocket, path):
    """Handle new WebSocket connection."""
    clients.add(websocket)
    print(f"[ws] client connected ({len(clients)} total)")
    
    try:
        # Send initial state
        with lock:
            await websocket.send(json.dumps({"type": "init", "data": latest}))
        
        # Keep connection alive and wait for messages
        async for message in websocket:
            pass  # Echo or handle client commands if needed
    except asyncio.CancelledError:
        pass
    finally:
        clients.remove(websocket)
        print(f"[ws] client disconnected ({len(clients)} total)")

# ─── Main broadcast loop ───────────────────────────────────────────────────────
async def broadcast_loop():
    """Send sensor data to clients at 60fps."""
    last_ts = None
    while True:
        with lock:
            row = latest.copy()
        
        # Only broadcast if data changed
        if row.get("ts") != last_ts:
            await broadcast({"type": "sensor", "data": row})
            last_ts = row.get("ts")
        
        await asyncio.sleep(1/60)  # 60 fps target

# ─── Server startup ───────────────────────────────────────────────────────────
async def main():
    # Start data thread (serial or fake)
    port = None
    if not FAKE_MODE:
        for p in serial.tools.list_ports.comports():
            if any(k in p.description for k in
                   ["Arduino","CH340","USB Serial","ttyUSB","ttyACM"]):
                port = p.device
                break
    
    src = (threading.Thread(target=serial_thread, args=(port,), daemon=True)
           if port else
           threading.Thread(target=fake_thread, daemon=True))
    if not port:
        print("[main] no Arduino → fake/demo mode")
    src.start()
    time.sleep(0.5)
    
    # Start WebSocket server
    async with websockets.serve(handler, WS_HOST, WS_PORT):
        print(f"[ws] server listening on ws://{WS_HOST}:{WS_PORT}")
        
        # Start broadcast loop
        await broadcast_loop()

if __name__ == "__main__":
    import websockets
    asyncio.run(main())
