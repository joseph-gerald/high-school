from matplotlib import pyplot as plt
import numpy as np

data = np.loadtxt("co2_norway.txt", delimiter=",")

x_original = data[:, 0]
y_original = data[:, 1]

x_extended = np.arange(1940, 2101)

linear_fit = np.polyfit(x_original, y_original, 1)
polynomial_fit = np.polyfit(x_original, y_original, 2)

def polynomial_function(x, fit):
    return fit[0] * x**2 + fit[1] * x + fit[2]

def linear_function(x, fit):
    return fit[0] * x + fit[1]

y_linear_extended = linear_function(x_extended, linear_fit)
y_polynomial_extended = polynomial_function(x_extended, polynomial_fit)

def plot_data(x_data, y_data, x_fit, y_linear_fit, y_polynomial_fit):
    plt.figure(figsize=(12, 6))
    plt.scatter(x_data, y_data, c="black", s=10, label="Original Data")
    plt.plot(x_fit, y_linear_fit, color="red", linestyle="-", label="Linear Fit")
    plt.plot(x_fit, y_polynomial_fit, color="blue", linestyle="--", label="Polynomial Fit")

    plt.xlabel("Time (Year)")
    plt.ylabel("MtCO2")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

plot_data(x_original, y_original, x_extended, y_linear_extended, y_polynomial_extended)