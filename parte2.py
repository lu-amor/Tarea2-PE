import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde, cauchy

def lcg(semilla, a, c, m):
    x = (a * semilla + c) % m
    return x, x / m

def distribuciónUniforme(n, semilla=None, a=1664525, c=1013904223, m=2**32):
    numeros = []
    if semilla is None:
        semilla = int(time.time() * 1000)
        print (time.time())
    x = semilla
    for _ in range(n):
        x, xsm = lcg(x, a, c, m) # xsm significa: x sobre m
        print(xsm)
        numeros.append(xsm)
    return numeros

def graficarUniforme(numeros):
    plt.figure()
    plt.hist(numeros, bins=10, density=True, alpha=0.6, color='#ffc2d4', edgecolor='#b9375e', label='Histograma')

    # Calcular curva de densidad de núcleos
    kde = gaussian_kde(numeros)
    x_vals = np.linspace(0, 1, 500)
    kde_vals = kde(x_vals)
    plt.plot(x_vals, kde_vals, color='#800f2f', label='Curva KDE')


    plt.xticks(np.arange(0, 1.01, 0.1))
    plt.title('Variable aleatoria uniforme + Curva de densidad')
    plt.xlabel('Valor')
    plt.ylabel('Densidad de probabilidad')
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()

def distribuciónCauchy(u):
    return np.tan(np.pi * (u - 0.5))

def graficarCauchy(numeros):
    numeros_filtrados = [x for x in numeros if -10 < x < 10]  # Filtra valores extremos

    plt.figure()
    plt.hist(numeros_filtrados, bins=100, density=True, alpha=0.6, color='#ffc2d4', edgecolor='#ff8fa3', label='Histograma') # no se que poner en la label pero hay que cambiar esto

    kde = gaussian_kde(numeros_filtrados)
    x_vals = np.linspace(-10, 10, 1000)
    kde_vals = kde(x_vals)

    plt.plot(x_vals, kde_vals, color='#c9184a', label='Curva KDE')
    plt.plot(x_vals, cauchy.pdf(x_vals), color='#026c7c', linestyle='--', linewidth='2', label='Densidad Cauchy teórica')

    plt.xlim(-10, 10)
    plt.xticks(np.arange(-10, 11, 2))
    plt.title('Distribución Cauchy Estándar')
    plt.xlabel('Valor')
    plt.ylabel('Densidad de Probabilidad')
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()


numeros = distribuciónUniforme(n=100)
graficarUniforme(numeros)
graficarCauchy(distribuciónCauchy(np.array(numeros)))