
def deriver(fn, x, a=6):
    d = 10**-a
    
    derivert = (fn(x+d) - fn(x)) / d
    
    return derivert

x_0 = -4
x = x_0

a = 6
d = 10**-a

fn = lambda x: x**2
diff = 10E+8

while True:
    lastDiff = diff
    x += d
    
    diff = abs(deriver(fn, x))
    
    if (diff > lastDiff):
        break

print(x, deriver(fn, x))
