m = 80   # kg
k = 0.25 # kg/m
v0 = 15  # m/s

def a(t, s, v):
    return -k/m*v**2

tg = 0
vg = v0
sg = 0
#T = 10 bruke denn hvis du har for løkke
dt = 0.01 # s
#N = int (T/dt) bruke denne hvis du har for løkke


while vg > 2:
    ag = a(tg, sg, vg) # regne ut akselerasjonen i forrige steg
    vn = vg + ag*dt # oppdater hastigheten
    sn = sg + vg*dt # oppdater posisjonen
    tn = tg + dt # oppdater tiden
    
    tg = tn
    sg = sn
    vg = vn

print("Stoppet etter", round(sn, 1), "meter")