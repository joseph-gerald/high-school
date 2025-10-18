
def f(x):
    try:
        return (x**3 + 2 * x ** 2) / (3 * x - 6)
        return x**3 + 2 * x**2
        return 3*x + 6
    except ZeroDivisionError:
        return float('inf')

def main():
    a = float(input("a: "))

    exponent = 0
    precision = 16

    while exponent <= precision:
        offset = 10 ** (-exponent)
        
        print(f"{a} ± {offset}: {f(a - offset)} to {f(a + offset)}")
        
        exponent += 1

while True:
    main()