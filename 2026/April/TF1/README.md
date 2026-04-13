# MPU-6050 3D Visualizer (WebSocket + Three.js)

Real-time 3D visualization of MPU-6050 sensor data using WebSocket for low-latency streaming and Three.js for smooth rendering.

## Setup

### 1. Install Python dependencies
```bash
pip install websockets pyserial numpy
```

### 2. Start the WebSocket server
```bash
python server.py
```

This will:
- Auto-detect Arduino on USB (or run in fake/demo mode)
- Start WebSocket server on `ws://localhost:8765`
- Stream sensor data at 60 fps

### 3. Open the visualizer
Open `index.html` in a web browser (or serve via HTTP):
```bash
# Option A: Direct file (may have CORS issues on some browsers)
open index.html

# Option B: Python simple HTTP server
python -m http.server 8000
# Then visit http://localhost:8000
```

## Features

- **Real-time 3D board visualization** – PCB rotates with actual sensor orientation
- **Acceleration vector** – Red arrow shows current acceleration direction and magnitude
- **Live data display** – Accel, gyro, angles, temperature
- **Smooth interpolation** – Linear interpolation between sensor readings for butter-smooth motion
- **Auto-reconnect** – Gracefully handles disconnects and reconnects
- **FPS counter** – Monitor rendering performance

## Architecture

### `server.py`
- Reads from Arduino (MPU-6050 connected via serial)
- Calculates roll/pitch from accelerometer
- Broadcasts latest reading to all connected WebSocket clients
- Falls back to synthetic data if no Arduino detected

### `index.html`
- Three.js 3D scene with PCB board mesh
- Receives sensor updates via WebSocket
- Interpolates between readings for smooth sub-frame motion
- Renders at requestAnimationFrame rate (typically 60 fps)

## Interpolation Details

The visualizer uses **zero-latency linear interpolation**:

1. Each sensor reading updates `currReading` with timestamp
2. Render loop calculates: `t = (now - prevTime) / (currTime - prevTime)`, clamped 0..1
3. Display values are lerped: `value = prev + (curr - prev) * t`
4. Result: Smooth sub-frame motion with no added lag

This works because:
- Sensor data arrives ~40 Hz (every ~25 ms)
- Rendering runs ~60 fps (every ~16.7 ms)
- Linear interpolation bridges the gap smoothly without lag

## Troubleshooting

**"Disconnected" status:**
- Check server is running: `python server.py`
- Verify ws://localhost:8765 is accessible
- Check browser console for errors

**Jerky motion:**
- Ensure server is broadcasting at 60 fps
- Check network latency
- Verify sensor is sending stable data

**Arduino not detected:**
- Server falls back to fake mode (synthetic data)
- Check serial port detection in server.py
- Manually set `FAKE_MODE = True` in server.py if desired

## Customization

- **Smooth more/less:** Adjust interpolation in `getDisplayState()` (line ~180 in index.html)
- **Board appearance:** Modify `boardMat` color and material properties
- **Arrow color/size:** Edit `updateArrow()` function
- **Server broadcast rate:** Change `await asyncio.sleep(1/60)` in `broadcast_loop()`
