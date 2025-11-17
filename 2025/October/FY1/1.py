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
    vg = vg + ag*dt  # regne ut ny fart
    sg = sg + vg*dt  # regne ut ny posisjon
    tg = tg + dt     # oppdatere tid

sn = sg

print("Stoppet etter", round(sn, 1), "meter")