# -*- coding: utf-8 -*-
"""IABD_MP3_T03_01.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zWD43Pexh6PN5u7mh3VGXoLWw58BWB6c

(https://www.tensorflow.org/datasets/catalog/mnist)
Objetivo: Clasificar imágenes de dígitos del 0 al 9.
Ejercicio 1: Scikit-learn (Perceptrón Multicapa)
•	Tarea: Construye un modelo de Perceptrón Multicapa (MLP) utilizando la clase MLPClassifier de Scikit-learn para clasificar las imágenes del dataset MNIST.
•	Requisitos:
o	Preprocesa los datos: Normaliza los valores de los píxeles de las imágenes (dividiendo por 255).
o	Divide el dataset en conjuntos de entrenamiento y prueba (por ejemplo, 80% entrenamiento, 20% prueba).
o	Entrena el modelo con diferentes configuraciones de hiperparámetros (número de capas ocultas, neuronas por capa, función de activación, optimizador, etc.)
o	Evalúa el rendimiento del modelo usando métricas como la precisión (accuracy) y la matriz de confusión.

Comenzamos por importar las bibliotecas necesarias. Hará falta scikit-learn, tensorflow_datasets  para leer el dataset, numpy para cálculos, seaborn y matplotlib para las gráficas y pandas para hacer datasets
"""

!pip install tensorflow-datasets
!pip install seaborn matplotlib

import time
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import tensorflow_datasets as tfds

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd

"""Después cargamos el dataset desde la url."""

# Carga el dataset MNIST
(ds_train, ds_test), ds_info = tfds.load(
    'mnist',
    split=['train', 'test'],
    shuffle_files=True,
    as_supervised=True,
    with_info=True,
)

"""La biblioteca MLPClassifier espera que los datos de entrada sean arrays de NumPy, así que el siguiente paso será convertir el datasey a NumPy arrays, y normalizarlos dividiendo entre 255.
Además, el datasey MNIST de tensorlow son arrays de tres dimensiones con (número de imágenes, alto, ancho). MPClassifier necesita convertir esas matrices en vectores unidimensionales, así que hay que aplanar las matrices. El -1 indica que debe calcular el número de filas, y el 784 las columnas (28x28 pixeles)
"""

# Convierte el dataset a NumPy arrays
X_train = np.array([example[0].numpy() for example in ds_train])
y_train = np.array([example[1].numpy() for example in ds_train])
X_test = np.array([example[0].numpy() for example in ds_test])
y_test = np.array([example[1].numpy() for example in ds_test])

# Normaliza los valores de los píxeles
X_train = X_train / 255.0
X_test = X_test / 255.0

# Ajusta la forma de los arrays de imágenes
X_train = X_train.reshape(-1, 784)
X_test = X_test.reshape(-1, 784)

"""Con los datos preparados, hay que dividirlos en datos de entrenamiento y de prueba. Usaremos una proporción de 80-20"""

# Divide los datos en conjuntos de entrenamiento y prueba
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

"""Ya que el objetivo es hacer varios entrenamientos y poder compararlos, vamos a crear una lista de diccionarios, donde cada diccionarios tiene una configuración diferente. Después entrenaremos al MLPClassifier con cada configuración, iterando sobre la lista, y lo evaluaremos.
Para poder comparar realmente cuál sería la mejor configuración de una forma seria habría que hacer más configuraciones y cambiar menos parámetros en cada una de ellas, para poder observar qué cambio está produciendo la mejora en el modelo. Aquí hemos puesto algunos para jugar con el programa, pero habría que ir adaptándalo.
"""

configuraciones = [
    {'hidden_layer_sizes': (100,), 'activation': 'relu', 'solver': 'adam'},
    {'hidden_layer_sizes': (50, 50), 'activation': 'tanh', 'solver': 'sgd'},
    {'hidden_layer_sizes': (100, 50, 25), 'activation': 'relu', 'solver': 'adam', 'alpha': 0.01},
    # ... más configuraciones
]

"""Aquí hay que definir qué se quiere evaluar. Además de la precisión global y la matriz de confusión, nos ha parecido interesante evaluar el tiempo que tarda en entrenarse el modelo y el de inferencia, el tiempo que tarda en resolver el test, que puede dar una idea de cuál podría ser más rápido a la hora de resolver problemas reales.
Para poder evaluar los modelos por clases, para saber si alguna clase le cuesta más que otra, además de los números de la matriz de confusión incluimos el classification_report de scikit, que permite ver la precisión, el recall y el F1-score por cada clase.  
"""

resultados = []

for i, config in enumerate(configuraciones):
    print(f"Entrenando configuración {i + 1}...")

    # Entrenamiento
    inicio_entrenamiento = time.time()
    modelo = MLPClassifier(**config, random_state=42)
    modelo.fit(X_train, y_train)
    fin_entrenamiento = time.time()
    tiempo_entrenamiento = fin_entrenamiento - inicio_entrenamiento

    # Inferencia
    inicio_inferencia = time.time()
    y_pred = modelo.predict(X_test)
    fin_inferencia = time.time()
    tiempo_inferencia = fin_inferencia - inicio_inferencia

    # Métricas
    precision = accuracy_score(y_test, y_pred)
    matriz_confusion = confusion_matrix(y_test, y_pred)
    reporte_clasificacion = classification_report(y_test, y_pred)

    resultados.append({
        'configuración': i + 1,
        'config': config,
        'precision': precision,
        'matriz_confusion': matriz_confusion,
        'tiempo_entrenamiento': tiempo_entrenamiento,
        'tiempo_inferencia': tiempo_inferencia,
        'reporte_clasificacion': reporte_clasificacion
    })

for i, resultado in enumerate(resultados):
    print(f"Configuración: {resultado['configuración']}")  # Mostrar el nombre de la configuración
    print(f"Precisión: {resultado['precision']}")
    print(f"Tiempo de entrenamiento: {resultado['tiempo_entrenamiento']} segundos")
    print(f"Tiempo de inferencia: {resultado['tiempo_inferencia']} segundos")
    print(f"Reporte de clasificación:\n{resultado['reporte_clasificacion']}")

    # Mostrar la matriz de confusión con seaborn
    paleta_colores = ["Blues", "Reds", "Greens"]  # Azul para 1, rojo para 2, verde para 3

    plt.figure(figsize=(8, 6))
    sns.heatmap(resultado['matriz_confusion'], annot=True, fmt='d', cmap=paleta_colores[i % len(paleta_colores)])  # Usar la paleta de colores
    plt.title('Matriz de Confusión')
    plt.xlabel('Predicción')
    plt.ylabel('Valor Real')
    plt.show()

"""Por último, comparamos los distintos resultados.


"""

#Grafico de barras para comparar la precisión, empezando en 0.9 para que se aprecie
precisiones = [resultado['precision'] for resultado in resultados]
nombres_configuraciones  = [f"Configuración {i+1}" for i in range(len(resultados))]

paleta_colores = ["skyblue", "tomato", "limegreen"]
plt.figure(figsize=(10, 6))
sns.barplot(x=nombres_configuraciones , y=precisiones , hue=nombres_configuraciones , palette=paleta_colores)
plt.title('Comparación de Precisión')
plt.xlabel('Configuración')
plt.ylabel('Precisión')
plt.ylim(0.9, 1.0)  # Ajustar el límite del eje Y
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

#Graficos para comparar los tiempos

# Extraer los tiempos de entrenamiento y de inferencia
tiempos_entrenamiento = [resultado['tiempo_entrenamiento'] for resultado in resultados]
tiempos_inferencia = [resultado['tiempo_inferencia'] for resultado in resultados]

# Crear una figura con dos subplots
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

# Gráfico de tiempos de entrenamiento
sns.barplot(x=nombres_configuraciones, y=tiempos_entrenamiento, ax=axes[0], hue=nombres_configuraciones , palette=paleta_colores)
axes[0].set_title('Comparación de Tiempos de Entrenamiento')
axes[0].set_xlabel('Configuración')
axes[0].set_ylabel('Tiempo (segundos)')
# Rotar las etiquetas del eje x y ajustar la alineación horizontal después de dibujar el gráfico
axes[0].tick_params(axis='x', rotation=45, labelbottom=True, labeltop=False)

# Gráfico de tiempos de inferencia
sns.barplot(x=nombres_configuraciones, y=tiempos_inferencia, ax=axes[1], hue=nombres_configuraciones , palette=paleta_colores)
axes[1].set_title('Comparación de Tiempos de Inferencia')
axes[1].set_xlabel('Configuración')
axes[1].set_ylabel('Tiempo (segundos)')
# Rotar las etiquetas del eje x y ajustar la alineación horizontal después de dibujar el gráfico
axes[1].tick_params(axis='x', rotation=45, labelbottom=True, labeltop=False)

# Ajustar el diseño
plt.tight_layout()
plt.show()

"""Incluimos también gráficos de barras para comprar la precisión, el recall y el f1-score por clase"""

# Extraer la precision para cada clase de cada configuración
precision_scores = []
for resultado in resultados:
    reporte = resultado['reporte_clasificacion']
    for linea in reporte.split('\n'):
        if linea.startswith(' ') and linea.split()[0].isdigit():  # Filtrar las líneas con información de las clases y asegurarse de que la primera columna sea un número (clase)
            clase = linea.split()[0]
            precision = float(linea.split()[1])  # Extraer la precision
            precision_scores.append([resultado['configuración'], clase, precision])

# Crear un DataFrame con los recall
df_recall = pd.DataFrame(precision_scores, columns=['Configuración', 'Clase', 'Precision'])

# Crear un gráfico de barras para comparar el recall para cada clase
plt.figure(figsize=(12, 6))
sns.barplot(x='Clase', y='Precision', hue='Configuración', data=df_recall, palette=paleta_colores)
plt.title('Comparación de la precision para cada clase')
plt.xlabel('Clase')
plt.ylabel('Precision')
plt.xticks(rotation=45, ha='right')
plt.ylim(0.9, 1.0)  # Ajustar el límite del eje Y
plt.tight_layout()
plt.show()

# Extraer el recall para cada clase de cada configuración
recall_scores = []
for resultado in resultados:
    reporte = resultado['reporte_clasificacion']
    for linea in reporte.split('\n'):
        if linea.startswith(' ') and linea.split()[0].isdigit():  # Filtrar las líneas con información de las clases y asegurarse de que la primera columna sea un número (clase)
            clase = linea.split()[0]
            recall = float(linea.split()[2])  # Extraer el recall
            recall_scores.append([resultado['configuración'], clase, recall])

# Crear un DataFrame con los recall
df_recall = pd.DataFrame(recall_scores, columns=['Configuración', 'Clase', 'Recall'])

# Crear un gráfico de barras para comparar el recall para cada clase
plt.figure(figsize=(12, 6))
sns.barplot(x='Clase', y='Recall', hue='Configuración', data=df_recall, palette=paleta_colores)
plt.title('Comparación del Recall para cada clase')
plt.xlabel('Clase')
plt.ylabel('Recall')
plt.xticks(rotation=45, ha='right')
plt.ylim(0.9, 1.0)  # Ajustar el límite del eje Y
plt.tight_layout()
plt.show()

# Extraer el F1-score para cada clase de cada configuración
f1_scores = []
for resultado in resultados:
    reporte = resultado['reporte_clasificacion']
    for linea in reporte.split('\n'):
        if linea.startswith(' ') and linea.split()[0].isdigit():  # Filtrar las líneas con información de las clases y asegurarse de que la primera columna sea un número (clase)
            clase = linea.split()[0]
            f1 = float(linea.split()[-2])  # Extraer el F1-score
            f1_scores.append([resultado['configuración'], clase, f1])

# Crear un DataFrame con los F1-scores
df_f1 = pd.DataFrame(f1_scores, columns=['Configuración', 'Clase', 'F1-score'])

# Crear un gráfico de barras para comparar el F1-score para cada clase
plt.figure(figsize=(12, 6))
sns.barplot(x='Clase', y='F1-score', hue='Configuración', data=df_f1, palette=paleta_colores)
plt.title('Comparación del F1-score para cada clase')
plt.xlabel('Clase')
plt.ylabel('F1-score')
plt.xticks(rotation=45, ha='right')
plt.ylim(0.9, 1.0)  # Ajustar el límite del eje Y
plt.tight_layout()
plt.show()

"""Por último, comparamos las matrices de confusión de las tres configuraciones


"""

# Comparaciones de matrices de confusión
comparaciones = [(0, 1), (0, 2), (1, 2)]  # Índices de las configuraciones a comparar

# Crear una figura con tres subplots
fig, axes = plt.subplots(nrows=1, ncols=len(comparaciones), figsize=(18, 6))

for i, (config1_idx, config2_idx) in enumerate(comparaciones):
    config1 = resultados[config1_idx]['matriz_confusion']
    config2 = resultados[config2_idx]['matriz_confusion']
    diferencia = config2 - config1

    # Visualizar la diferencia con un heatmap en el subplot correspondiente
    sns.heatmap(diferencia, annot=True, fmt='d', cmap='RdBu_r', ax=axes[i])
    axes[i].set_title(f'Diferencia entre la configuración {config2_idx + 1} y la configuración {config1_idx + 1}')
    axes[i].set_xlabel('Predicción')
    axes[i].set_ylabel('Valor Real')

# Ajustar el diseño
plt.tight_layout()
plt.show()