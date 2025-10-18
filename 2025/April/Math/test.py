from matplotlib import pyplot as plt
import numpy as np

data = np.loadtxt("co2_norway.txt", delimiter=",")

x = data[:, 0]
y = data[:, 1]

linear_fit = np.polyfit(x, y, 1)
polynomial_fit = np.polyfit(x, y, 2)

def polynomial_function(x):
    return polynomial_fit[0] * x**2 + polynomial_fit[1] * x + polynomial_fit[2]

def linear_function(x):
    return linear_fit[0] * x + linear_fit[1]

def plot_data():    
    plt.scatter(x, y, c="black", s=10)

    plt.xlabel("Time (Year)")
    plt.ylabel("MtCO2")
    plt.legend()

    plt.show()

plt.plot(x, linear_function(x), color="red", label="Linear Fit")
plot_data()

plt.plot(x, polynomial_function(x), color="red", label="Polynom Fit")
plot_data()

# print the derivative of the polynomial function

derivative = np.polyder(polynomial_fit)
print(derivative)

# print the extremum of the polynomial function

extremum = np.roots(derivative)
print(extremum)

# find the gradient in the year 1970, 1990 and 2010

gradient_1970 = np.polyval(derivative, 1970)
gradient_1990 = np.polyval(derivative, 1990)
gradient_2010 = np.polyval(derivative, 2010)

print("Gradient in 1970: ", gradient_1970)
print("Gradient in 1990: ", gradient_1990)
print("Gradient in 2010: ", gradient_2010)

# find the linear function for the range 1960-1970 and 2010-2017

linear_fit_1960_1970 = np.polyfit(x[(x >= 1960) & (x <= 1970)], y[(x >= 1960) & (x <= 1970)], 1)
linear_fit_2010_2017 = np.polyfit(x[(x >= 2010) & (x <= 2017)], y[(x >= 2010) & (x <= 2017)], 1)
print("Linear fit for 1960-1970: ", linear_fit_1960_1970)
print("Linear fit for 2010-2017: ", linear_fit_2010_2017)

# find the linear function for the range 1960-1970 and 2010-2017

linear_fit_1960_1970 = np.polyfit(x[(x >= 1960) & (x <= 1970)], y[(x >= 1960) & (x <= 1970)], 1)
linear_fit_2010_2017 = np.polyfit(x[(x >= 2010) & (x <= 2017)], y[(x >= 2010) & (x <= 2017)], 1)

print("Linear fit for 1960-1970: ", linear_fit_1960_1970)
print("Linear fit for 2010-2017: ", linear_fit_2010_2017)

# find when the polynomial function is equal to 0

roots = np.roots(polynomial_fit)
print("Roots of the polynomial function: ", roots)