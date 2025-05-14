import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import cm 

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z**2 +c 
        n += 1
    return n

def generate_fractal(xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    fractal = np.zeros((height, width))

    for i in range(height):
        for j in range(width):
            fractal[i, j] = mandelbrot(x[j] + 1j*y[i], max_iter)
    
    return fractal

xmin, xmax = -2, 1
ymin, ymax = -1.5, 1.5
width, height = 800, 600
max_iter = 50


fractal = generate_fractal(xmin, xmax, ymin, ymax, width, height, max_iter)

plt.figure(figsize=(10,8))
plt.imshow(fractal, cmap=cm.magma, extent=(xmin, xmax, ymin, ymax))
plt.colorbar(label= "Iteraciones")
plt.show()