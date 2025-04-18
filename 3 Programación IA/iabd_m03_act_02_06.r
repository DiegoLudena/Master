# -*- coding: utf-8 -*-
"""iabd_m03_act_02_06.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1M_Xi9Tn1--88mILZ34DMnIKtShbQUwJz

Crea un DataFrame sencillo en R con datos de productos, incluyendo su Nombre, Categoría, y Precio. Luego, realiza algunas manipulaciones de datos, como filtrar productos por categoría y calcular el precio promedio de los productos.
Instrucciones:

Comienzo por instalar la biblioteca data.table para crear la tabla
"""

install.packages("data.table")

"""He intentado crear datos aleatorios, pero las bibliotecas que he probado, o no son compatibles
con la versión de R de GoogleColab (faker, mockaroo), o sirven para generar
nombres propios, no categorías.

He optado por por pedir a ChatGPT la lista de los productos para el código y generar solo los precios.
"""

# Crear un conjunto de productos y categorías
productos <- c("Laptop", "Smartphone", "Tablet", "Auriculares", "Teclado",
               "Monitor", "Ratón", "Cámara", "Impresora", "Altavoz",
               "Smartwatch", "Televisor", "Consola de videojuegos", "Disco duro externo",
               "Router", "Microondas", "Frigorífico", "Lavadora", "Cafetera", "Aspiradora")

categorias <- c("Electrónica", "Electrónica", "Electrónica", "Audio", "Periféricos",
                "Electrónica", "Periféricos", "Fotografía", "Oficina", "Audio",
                "Electrónica", "Electrónica", "Electrónica", "Almacenamiento",
                "Redes", "Electrodomésticos", "Electrodomésticos", "Electrodomésticos", "Electrodomésticos", "Electrodomésticos")

# Establecer número de productos
n <- length(productos)

# Asignar rangos de precios según la categoría
for (i in 1:n) {
  if (categorias[i] == "Electrónica") {
    precios[i] <- round(runif(1, min = 200, max = 1500), 2)
  } else if (categorias[i] == "Periféricos") {
    precios[i] <- round(runif(1, min = 50, max = 300), 2)
  } else if (categorias[i] == "Audio") {
    precios[i] <- round(runif(1, min = 100, max = 500), 2)
  } else if (categorias[i] == "Fotografía") {
    precios[i] <- round(runif(1, min = 300, max = 2000), 2)
  } else if (categorias[i] == "Oficina") {
    precios[i] <- round(runif(1, min = 100, max = 600), 2)
  } else if (categorias[i] == "Almacenamiento") {
    precios[i] <- round(runif(1, min = 50, max = 400), 2)
  } else if (categorias[i] == "Redes") {
    precios[i] <- round(runif(1, min = 50, max = 250), 2)
  } else if (categorias[i] == "Electrodomésticos") {
    precios[i] <- round(runif(1, min = 100, max = 800), 2)
  }
}

# Crear DataFrame
df_productos <- data.frame(Nombre = productos, Categoría = categorias, Precio = precios)

# Mostrar el DataFrame
print(df_productos)

"""-	Filtra los productos que pertenecen a una categoría específica (por ejemplo, "Electrónica")."""

# Filtrar productos que pertenecen a la categoría "Electrónica"
df_electronica <- subset(df_productos, Categoría == "Electrónica")

# Mostrar los productos filtrados
print(df_electronica)

-	Calcula y muestra el precio promedio de los productos de esa categoría.

# Calcular el precio medio de los productos en la categoría "Electrónica"
precio_medio_electronica <- mean(df_electronica$Precio)

# Mostrar el precio medio
print(paste("El precio medio de Electrónica es:", round(precio_medio_electronica, 2), "€"))

"""Para utilizar alguna función más, voy a mostrar el producto más caro y el más barato."""

# Producto más caro
producto_mas_caro <- df_productos[which.max(df_productos$Precio), ]

# Producto más barato
producto_mas_barato <- df_productos[which.min(df_productos$Precio), ]

# Mostrar resultados
print("Producto más caro:")
print(producto_mas_caro)

print("Producto más barato:")
print(producto_mas_barato)

Y voy a añadir una columna "Rango de precio"
que clasifique los productos en "Barato", "Caro" o "En la media" según el precio
 promedio de su categoría.

# Crear una nueva columna en el DataFrame
df_productos$Rango <- NA

# Calcular el precio medio por cada categoría y asignar "Barato", "Caro" o "En la media"
for (categoria in unique(df_productos$Categoría)) {
  # Filtrar productos de la categoría actual
  productos_categoria <- subset(df_productos, Categoría == categoria)

  # Calcular el precio medio de la categoría
  precio_medio_categoria <- mean(productos_categoria$Precio)

  # Clasificar cada producto en la categoría
  for (i in 1:nrow(df_productos)) {
    if (df_productos$Categoría[i] == categoria) {
      if (df_productos$Precio[i] < precio_medio_categoria) {
        df_productos$Rango[i] <- "Barato"
      } else if (df_productos$Precio[i] > precio_medio_categoria) {
        df_productos$Rango[i] <- "Caro"
      } else {
        df_productos$Rango[i] <- "En la media"
      }
    }
  }
}

# Mostrar el DataFrame con la nueva columna "Rango"
print(df_productos)