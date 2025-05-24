import csv
import matplotlib.pyplot as plt
import numpy as np

# Parte 1
contadorRows = 0
valores = []

# Lectura de todos los valores
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

# Valor máximo de cancelaciones
max_valor = max(valores) if valores else 0

# Crea un array para contar la cantidad de ocurrencias de cada cantidad de cancelaciones
cancelaciones_por_valor = [0] * (max_valor + 1)

# Recorre los valores y cuenta las ocurrencias
for valor in valores:
    cancelaciones_por_valor[valor] += 1

# Calcula la distribución acumulada
acumulado = 0
distribucion_acumulada = []
for i in range(max_valor + 1):
    probabilidad = cancelaciones_por_valor[i] / contadorRows if contadorRows > 0 else 0
    acumulado += probabilidad
    distribucion_acumulada.append((round(acumulado, 4)))

# Escribe probabilidades y distribución acumulada en el archivo de salida
with open('probabilidades.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='|')
    spamwriter.writerow(['valor', 'cant. cancelaciones', 'probabilidad', 'dist. acumulada'])
    for i in range(max_valor + 1):
        if cancelaciones_por_valor[i] == 0:
            continue
        probabilidad = cancelaciones_por_valor[i] / contadorRows if contadorRows > 0 else 0
        spamwriter.writerow([i, cancelaciones_por_valor[i], round(probabilidad, 4), distribucion_acumulada[i]])

# Parte 2
# Cálculo de esperanza
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
# Histograma
min_valor = min(valores)
max_valor = max(valores)
bins = np.arange(min_valor - 0.5, max_valor + 1.5, 1) 

# Graficar histograma alineado
plt.hist(valores, bins=bins, color='#ffc2d4', edgecolor='black')
plt.title('Histograma de cancelaciones')
plt.xlabel('Cantidad de cancelaciones')
plt.ylabel('Frecuencia')
plt.xticks(range(min_valor, max_valor + 1))
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()