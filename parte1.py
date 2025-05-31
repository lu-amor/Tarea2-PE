import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import poisson
from collections import Counter

# Parte 1
contadorRows = 0
valores = []

# Lectura de todos los valores
valores = []
contadorRows = 0

with open('cancelaciones.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader)  # Saltar encabezado
    for row in spamreader:
        try:
            valor = int(row[1])
            if valor >= 0:
                valores.append(valor)
                contadorRows += 1
        except ValueError:
            continue

# Contar ocurrencias de cada cantidad de cancelaciones
cancelaciones_por_valor = Counter(valores)
valores_ordenados = sorted(cancelaciones_por_valor.keys())

acumulado = 0.0
with open('probabilidades.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='|')
    spamwriter.writerow(['valor', 'cant. cancelaciones', 'probabilidad', 'dist. acumulada'])
    
    for valor in valores_ordenados:
        cantidad = cancelaciones_por_valor[valor]
        probabilidad = cantidad / contadorRows
        acumulado += probabilidad
        spamwriter.writerow([valor, cantidad, round(probabilidad, 4), round(acumulado, 4)])

# Parte 2
# Cálculo de esperanza
max_valor = max(cancelaciones_por_valor) if cancelaciones_por_valor else 0
esperanza = sum(i * cancelaciones_por_valor[i] for i in range(max_valor + 1)) / contadorRows if contadorRows > 0 else 0
print(f'Esperanza: {round(esperanza, 4)}')

# Cálculo de varianza
varianza = sum((i - esperanza) ** 2 * cancelaciones_por_valor[i] for i in range(max_valor + 1)) / contadorRows if contadorRows > 0 else 0
print(f'Varianza: {round(varianza, 4)}')

# Parte 3
if not valores:
    print("No hay datos para graficar.")
else:
    mediana = np.median(valores)

    q1 = np.percentile(valores, 25)
    q3 = np.percentile(valores, 75)
    ri = q3 - q1
    print(f'Mediana: {round(mediana, 4)}')
    print(f'Q1: {round(q1, 4)}')
    print(f'Q3: {round(q3, 4)}')
    print(f'RI: {round(ri, 4)}')

    # Diagrama de caja
    plt.boxplot(valores, medianprops=dict(color='#b9375e', linewidth = 1.5), boxprops=dict(color='#ff7aa2', linewidth = 1.5))
    plt.title('Diagrama de caja de cancelaciones')
    plt.xlabel('Cantidad de cancelaciones')
    plt.grid()
    plt.show()

# Parte 4
# Crea bins para que el formato del histograma quede mejor
min_valor = min(valores)
max_valor = max(valores)
bins = np.arange(min_valor - 0.5, max_valor + 1.5, 1) 

plt.hist(valores, bins=bins, color='#ffc2d4', edgecolor='black')
plt.title('Histograma de cancelaciones')
plt.xlabel('Cantidad de cancelaciones')
plt.ylabel('Frecuencia')
plt.xticks(range(min_valor, max_valor + 1))
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()

# Parte 5 - Poisson
x_vals_poisson = np.arange(min_valor, max_valor + 1)
pmf_poisson = poisson.pmf(x_vals_poisson, mu=round(esperanza, 4)) * contadorRows  # Escalar para que coincida con frecuencias

# Histograma con superposición de Poisson
plt.hist(valores, bins=bins, color='#ffc2d4', edgecolor='black', label='Datos reales')
plt.plot(x_vals_poisson, pmf_poisson, 'o-', color='#c9184a', label=f'Poisson λ={round(esperanza, 4)}')
plt.title('Cancelaciones diarias vs Distribución de Poisson')
plt.xlabel('Cantidad de cancelaciones')
plt.ylabel('Frecuencia')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()

# Parte 6 - Probabilidades bajo Poisson
prob_menor_5 = poisson.cdf(4, mu=round(esperanza, 4))
prob_mayor_15 = 1 - poisson.cdf(15, mu=round(esperanza, 4))

print(f"P(X < 5): {round(prob_menor_5, 4)}")
print(f"P(X > 15): {round(prob_mayor_15, 4)}")
