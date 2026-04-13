"""
mpu_gl.py  —  MPU-6050 live visualizer
GPU-rendered via pygame + PyOpenGL. Runs at true 60 fps.

Install:  pip install pygame PyOpenGL PyOpenGL_accelerate pyserial numpy
Run:      python mpu_gl.py
"""

import os, sys, json, threading, time, math
from collections import deque

import numpy as np
import serial
import serial.tools.list_ports

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# ─── Config ───────────────────────────────────────────────────────────────────
BAUD_RATE     = 9600
HISTORY_LEN   = 300
DATA_FILE     = "mpu_data.json"
FAKE_MODE     = False          # auto-set if no Arduino found
TARGET_FPS    = 60

WIN_W, WIN_H  = 1400, 800
GRAPH_X       = 680            # pixel x where graphs start
GRAPH_PAD     = 14

# ─── Shared state ─────────────────────────────────────────────────────────────
lock  = threading.Lock()
buf   = {k: deque(maxlen=HISTORY_LEN) for k in
         ["ax","ay","az","gx","gy","gz","roll","pitch"]}
latest = {"ax":0,"ay":0,"az":1,"gx":0,"gy":0,"gz":0,"temp":25.0,
          "roll":0.0,"pitch":0.0}

# ── Interpolation: lerp between the two most recent readings ─────────────────
# _ra = reading that arrived BEFORE _rb
# _rb = most recent reading
# When render calls get_display(), we calculate how far we are between _ra→_rb
# based on elapsed time, and linearly interpolate.
# This has ZERO added latency — we're always showing the true position now.

_KEYS = ["roll","pitch","ax","ay","az","gx","gy","gz","temp"]

_ra   = {"roll":0.0,"pitch":0.0,"ax":0.0,"ay":0.0,"az":1.0,
         "gx":0.0,"gy":0.0,"gz":0.0,"temp":25.0}
_rb   = {k: v for k, v in _ra.items()}
_t_ra = [time.time() - 0.02]  # Start with 20ms gap
_t_rb = [time.time()]
_read_lock = threading.Lock()

def _push_reading(row):
    """Shift the reading window: rb becomes ra, new row becomes rb."""
    with _read_lock:
        for k in _KEYS:
            _ra[k] = _rb[k]
            _rb[k] = row.get(k, _rb[k])
        _t_ra[0] = _t_rb[0]
        _t_rb[0] = time.time()

def get_display():
    """Interpolate between _ra and _rb based on elapsed time since _t_ra."""
    with _read_lock:
        span = _t_rb[0] - _t_ra[0]
        if span < 1e-6:
            return dict(_rb)
        # How far between _ra (t=0) and _rb (t=1) are we right now?
        t = max(0.0, min(1.0, (time.time() - _t_ra[0]) / span))
        return {k: _ra[k] + (_rb[k] - _ra[k]) * t for k in _KEYS}

# ─── File I/O ─────────────────────────────────────────────────────────────────
def write_data_file(row):
    snap = {"latest": row,
            "history": {k: list(buf[k])[-20:] for k in buf}}
    tmp = DATA_FILE + ".tmp"
    try:
        with open(tmp, "w") as f:
            json.dump(snap, f, indent=2)
        try:
            os.replace(tmp, DATA_FILE)       # atomic on POSIX
        except OSError:
            # Windows: os.replace can fail if dst is locked — just overwrite
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            os.rename(tmp, DATA_FILE)
    except Exception:
        # file I/O is non-critical — write directly as fallback
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(snap, f, indent=2)
        except Exception:
            pass

# ─── Sensor helpers ───────────────────────────────────────────────────────────
def angles(ax, ay, az):
    roll  = math.degrees(math.atan2(ay, az))
    pitch = math.degrees(math.atan2(-ax, math.sqrt(ay**2 + az**2)))
    return roll, pitch

def ingest(row):
    global latest
    r, p = angles(row["ax"], row["ay"], row["az"])
    row["roll"] = r; row["pitch"] = p
    with lock:
        latest = row.copy()
        for k in ["ax","ay","az","gx","gy","gz","roll","pitch"]:
            buf[k].append(row[k])
    _push_reading(row)
    write_data_file(row)

# ─── Data sources ─────────────────────────────────────────────────────────────
def fake_thread():
    t = 0.0
    while True:
        t += 0.04
        ax = 0.35 * math.sin(t * 0.9)
        ay = 0.35 * math.cos(t * 0.65)
        az = math.sqrt(max(0.0, 1.0 - ax**2 - ay**2))
        ingest({"ax":ax,"ay":ay,"az":az,
                "gx":8*math.cos(t),"gy":8*math.sin(t*0.8),
                "gz":3*math.sin(t*1.3),"temp":24.5})
        time.sleep(0.025)

def serial_thread(port):
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
                pass   # bad line — skip, keep reading
    except Exception as e:
        print(f"[serial] connection failed: {e} → fake mode")
        fake_thread()

# ─── OpenGL 3D rendering ──────────────────────────────────────────────────────
# Board vertices (unit scale, Z-up)
_W, _H, _D = 0.48, 0.76, 0.055
_V = [(-_W,-_H,-_D),( _W,-_H,-_D),( _W, _H,-_D),(-_W, _H,-_D),
      (-_W,-_H, _D),( _W,-_H, _D),( _W, _H, _D),(-_W, _H, _D)]
# face definitions (vertex indices) + per-face color (dark PCB green shades)
_FACES = [
    ([0,1,2,3], (0.05,0.18,0.07)),   # bottom
    ([4,5,6,7], (0.07,0.22,0.09)),   # top
    ([0,1,5,4], (0.06,0.20,0.08)),   # front
    ([2,3,7,6], (0.06,0.20,0.08)),   # back
    ([0,3,7,4], (0.04,0.15,0.06)),   # left
    ([1,2,6,5], (0.04,0.15,0.06)),   # right
]
# per-face normals
def _face_normal(idxs):
    a = np.array(_V[idxs[1]]) - np.array(_V[idxs[0]])
    b = np.array(_V[idxs[2]]) - np.array(_V[idxs[0]])
    n = np.cross(a, b); return n / (np.linalg.norm(n) + 1e-9)

_NORMALS = [_face_normal(idxs) for idxs, _ in _FACES]

def draw_board(roll_deg, pitch_deg):
    glPushMatrix()
    glRotatef(pitch_deg, 0, 1, 0)
    glRotatef(roll_deg,  1, 0, 0)

    # PCB body
    for (idxs, col), norm in zip(_FACES, _NORMALS):
        glColor3f(*col)
        glNormal3f(*norm)
        glBegin(GL_QUADS)
        for i in idxs:
            glVertex3f(*_V[i])
        glEnd()

    # Edge outline
    glColor3f(0.12, 0.45, 0.18)
    glLineWidth(1.2)
    for idxs, _ in _FACES:
        glBegin(GL_LINE_LOOP)
        for i in idxs:
            glVertex3f(*_V[i])
        glEnd()

    glPopMatrix()

def draw_arrow(tip, color, width=2.0):
    """Draw a line from origin to tip with a small cone head."""
    tx, ty, tz = tip
    glColor3f(*color)
    glLineWidth(width)
    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)
    glVertex3f(tx, ty, tz)
    glEnd()

def draw_axis_grid():
    """World axes + faint grid on the XY plane."""
    glLineWidth(1.0)
    axes = [((1,0,0),(0.4,0.1,0.1)),
            ((0,1,0),(0.1,0.4,0.1)),
            ((0,0,1),(0.1,0.1,0.4))]
    for (dx,dy,dz), col in axes:
        glColor3f(*col)
        glBegin(GL_LINES)
        glVertex3f(0,0,0); glVertex3f(dx*1.1,dy*1.1,dz*1.1)
        glEnd()

    glColor3f(0.10, 0.10, 0.10)
    glLineWidth(0.5)
    for i in range(-5, 6):
        x = i * 0.22
        glBegin(GL_LINES)
        glVertex3f(x, -1.1, -1.0); glVertex3f(x, 1.1, -1.0)
        glEnd()
        glBegin(GL_LINES)
        glVertex3f(-1.1, x, -1.0); glVertex3f(1.1, x, -1.0)
        glEnd()

# ─── 2D graph rendering (pygame.draw) ────────────────────────────────────────
# Colors per channel
CH_COL = {
    "ax":(255, 68, 85), "ay":(51,255,170), "az":(68,153,255),
    "gx":(255, 68, 85), "gy":(51,255,170), "gz":(68,153,255),
    "roll":(255,170, 34),"pitch":(204, 85,255),
}
BG_COL   = (10, 10, 10)
PANEL_COL= (16, 16, 16)
DIM_COL  = (30, 30, 30)
TEXT_COL = (80, 80, 80)

def _draw_graph(surf, rect, channels, data_dict, y_pad=0.15, title=""):
    x0, y0, gw, gh = rect
    pygame.draw.rect(surf, PANEL_COL, rect)
    pygame.draw.rect(surf, DIM_COL,   rect, 1)

    # collect all values for y-range
    all_vals = []
    for ch in channels:
        d = list(data_dict[ch])
        if d: all_vals.extend(d)
    if not all_vals:
        return
    mn, mx = min(all_vals), max(all_vals)
    span = max(mx - mn, 0.01)
    mn -= span * y_pad; mx += span * y_pad

    # zero line
    if mn < 0 < mx:
        zy = y0 + gh - int((0 - mn) / (mx - mn) * gh)
        pygame.draw.line(surf, (30,30,30), (x0, zy), (x0+gw, zy), 1)

    for ch in channels:
        d = list(data_dict[ch])
        if len(d) < 2: continue
        n = len(d)
        pts = []
        for i, v in enumerate(d):
            px = x0 + int(i / (HISTORY_LEN - 1) * gw)
            py = y0 + gh - int((v - mn) / (mx - mn) * gh)
            py = max(y0, min(y0+gh, py))
            pts.append((px, py))
        pygame.draw.lines(surf, CH_COL[ch], False, pts, 1)

    if title:
        label = _font_sm.render(title, True, TEXT_COL)
        surf.blit(label, (x0 + 6, y0 + 4))

def _draw_text(surf, text, pos, color, font=None):
    f = font or _font_sm
    surf.blit(f.render(text, True, color), pos)

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    global _font_sm, _font_md, _font_lg

    # ── start data thread ──
    port = None
    if not FAKE_MODE:
        for p in serial.tools.list_ports.comports():
            if any(k in p.description for k in
                   ["Arduino","CH340","USB Serial","ttyUSB","ttyACM"]):
                port = p.device; break
    src = (threading.Thread(target=serial_thread, args=(port,), daemon=True)
           if port else
           threading.Thread(target=fake_thread, daemon=True))
    if not port:
        print("[main] no Arduino → fake/demo mode")
    src.start()
    time.sleep(0.25)

    # ── pygame + OpenGL init ──
    pygame.init()
    pygame.display.set_caption("MPU-6050  ·  GL Visualizer")
    screen = pygame.display.set_mode(
        (WIN_W, WIN_H), DOUBLEBUF | OPENGL | RESIZABLE)
    clock = pygame.time.Clock()

    _font_sm = pygame.font.SysFont("monospace", 12)
    _font_md = pygame.font.SysFont("monospace", 14, bold=True)
    _font_lg = pygame.font.SysFont("monospace", 18, bold=True)

    # 2D overlay surface (blitted on top each frame)
    overlay = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)

    # ── OpenGL viewport: left half only ──
    VP_W = GRAPH_X   # 3D lives in [0 .. GRAPH_X]

    def setup_3d_viewport():
        glViewport(0, 0, VP_W, WIN_H)
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        gluPerspective(45, VP_W / WIN_H, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW);  glLoadIdentity()
        gluLookAt(0, -3.2, 1.6,   0, 0, 0,   0, 0, 1)

    setup_3d_viewport()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glShadeModel(GL_SMOOTH)
    glClearColor(BG_COL[0]/255, BG_COL[1]/255, BG_COL[2]/255, 1.0)

    s_roll = s_pitch = 0.0

    while True:
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit(); sys.exit()
            if ev.type == KEYDOWN and ev.key == K_ESCAPE:
                pygame.quit(); sys.exit()

        # ── grab latest data ──
        with lock:
            row   = latest.copy()
            buf_snap = {k: list(buf[k]) for k in buf}

        # ── linear interpolation/extrapolation to right now ──
        iv      = get_display()
        s_roll  = iv["roll"]
        s_pitch = iv["pitch"]
        sv      = iv

        # ════════════════════════════════════════════
        # 1) OpenGL: clear & draw 3D left panel
        # ════════════════════════════════════════════
        glViewport(0, 0, VP_W, WIN_H)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW); glLoadIdentity()
        gluLookAt(0, -3.2, 1.6,   0, 0, 0,   0, 0, 1)

        draw_axis_grid()
        draw_board(s_roll, s_pitch)

        # accel vector
        draw_arrow((sv["ax"], sv["ay"], sv["az"]), (1.0, 0.27, 0.33), width=2.5)

        # ════════════════════════════════════════════
        # 2) pygame 2D: graphs + info on right panel
        # ════════════════════════════════════════════
        # Switch to 2D — blit overlay onto a temp surface then use
        # glDrawPixels to composite it over the OpenGL frame.
        # Simpler: use pygame.display with OPENGL flag means we can't
        # blit directly. Instead we render the 2D part into a Surface
        # then upload as texture to a full-screen quad on the right half.

        overlay.fill((0, 0, 0, 0))

        # background for right panel
        pygame.draw.rect(overlay, (*BG_COL, 255),
                         (GRAPH_X, 0, WIN_W - GRAPH_X, WIN_H))

        GW = WIN_W - GRAPH_X - GRAPH_PAD * 2
        gh = (WIN_H - GRAPH_PAD * 5) // 3

        # ── 3 graphs stacked ──
        _draw_graph(overlay,
                    (GRAPH_X + GRAPH_PAD, GRAPH_PAD, GW, gh),
                    ["ax","ay","az"], buf_snap, title="accelerometer  (g)")

        _draw_graph(overlay,
                    (GRAPH_X + GRAPH_PAD, GRAPH_PAD*2 + gh, GW, gh),
                    ["gx","gy","gz"], buf_snap, title="gyroscope  (°/s)")

        _draw_graph(overlay,
                    (GRAPH_X + GRAPH_PAD, GRAPH_PAD*3 + gh*2, GW, gh),
                    ["roll","pitch"], buf_snap,
                    y_pad=0.25, title="angles  (°)")

        # ── legend dots ──
        legend_y = WIN_H - 20
        for i, (label, col) in enumerate([
                ("AX/GX/Roll","#ff4455"),("AY/GY/Pitch","#33ffaa"),("AZ/GZ","#4499ff")]):
            x = GRAPH_X + GRAPH_PAD + i * 140
            pygame.draw.circle(overlay, CH_COL["ax" if i==0 else "ay" if i==1 else "az"],
                               (x, legend_y), 4)
            _draw_text(overlay, label, (x+10, legend_y-7), (60,60,60))

        # ── info panel (right of last graph, or below — squeeze into bottom) ──
        IX = GRAPH_X + GRAPH_PAD
        IY = GRAPH_PAD*3 + gh*2 + gh + GRAPH_PAD*2
        if IY + 160 < WIN_H:
            info_items = [
                (f"AX {sv['ax']:+.3f} g",  CH_COL["ax"]),
                (f"AY {sv['ay']:+.3f} g",  CH_COL["ay"]),
                (f"AZ {sv['az']:+.3f} g",  CH_COL["az"]),
                (f"GX {sv['gx']:+6.1f} °/s", CH_COL["gx"]),
                (f"GY {sv['gy']:+6.1f} °/s", CH_COL["gy"]),
                (f"GZ {sv['gz']:+6.1f} °/s", CH_COL["gz"]),
                (f"T  {sv['temp']:.1f} °C",  (136,204,255)),
            ]
            for i, (txt, col) in enumerate(info_items):
                _draw_text(overlay, txt, (IX + i//4*200, IY + (i%4)*18), col)

        # posture indicator
        ok = abs(s_pitch) < 30
        p_col = (51,255,170) if ok else (255,68,85)
        p_txt = "POSTURE OK" if ok else "BENT FORWARD"
        _draw_text(overlay, p_txt,
                   (GRAPH_X + GRAPH_PAD, WIN_H - 38), p_col, _font_md)

        # roll/pitch readout top of 3D panel
        rp_txt = f"roll {s_roll:+.1f}°   pitch {s_pitch:+.1f}°"
        _draw_text(overlay, rp_txt, (10, 10), (50,50,50), _font_md)

        # fps
        fps_txt = f"{clock.get_fps():.0f} fps"
        _draw_text(overlay, fps_txt, (VP_W - 60, 10), (35,35,35))

        # ── upload overlay as OpenGL texture & draw full-screen quad ──
        # Convert surface to raw bytes
        raw = pygame.image.tostring(overlay, "RGBA", True)
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, WIN_W, WIN_H, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, raw)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # 2D textured quad over full screen
        glViewport(0, 0, WIN_W, WIN_H)
        glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
        glOrtho(0, WIN_W, 0, WIN_H, -1, 1)
        glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()

        glEnable(GL_TEXTURE_2D)
        glDisable(GL_DEPTH_TEST)
        glColor4f(1,1,1,1)
        glBegin(GL_QUADS)
        glTexCoord2f(0,0); glVertex2f(0,    0)
        glTexCoord2f(1,0); glVertex2f(WIN_W,0)
        glTexCoord2f(1,1); glVertex2f(WIN_W,WIN_H)
        glTexCoord2f(0,1); glVertex2f(0,    WIN_H)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION); glPopMatrix()
        glMatrixMode(GL_MODELVIEW);  glPopMatrix()
        glDeleteTextures([tex_id])

        pygame.display.flip()
        clock.tick(TARGET_FPS)

if __name__ == "__main__":
    main()