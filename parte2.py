import time
import matplotlib.pyplot as plt
import numpy as np

def lcg(semilla, a, c, m):
    x = (a * semilla + c) % m
    return x, x / m

def generar_numeros_aleatorios(n, semilla=None, a=1664525, c=1013904223, m=2**32):
    numeros = []
    if semilla is None:
        semilla = int(time.time() * 1000)
    x = semilla
    for _ in range(n):
        x, rnd = lcg(x, a, c, m)
        print(f'{rnd}')
        numeros.append(rnd)
    return numeros

generar_numeros_aleatorios(n=100)

# histograma de frecuencias
def graficar_histograma(numeros):
    plt.hist(numeros, bins=10, density=True, alpha=0.7, color='#ffc2d4')
    plt.title('Histograma de Números Aleatorios')
    plt.xlabel('Valor')
    plt.ylabel('Densidad de Probabilidad')
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.show()
graficar_histograma(generar_numeros_aleatorios(n=100))