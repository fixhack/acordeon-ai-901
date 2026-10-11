# Tema 2: Imágenes y procesamiento de imágenes

### Descripción
Antes de hablar de redes neuronales, hay que entender cómo "ve" la computadora. Una imagen es una **matriz de números** y "procesarla" significa hacer operaciones matemáticas sobre esa matriz. La operación estrella es la **convolución con filtros**, que es exactamente lo que después aprenden a hacer las CNN.

Lectura oficial: [Imágenes y procesamiento de imágenes – Microsoft Learn](https://learn.microsoft.com/es-es/training/modules/introduction-computer-vision/3-understand-image-processing?pivots=text)

Analogía: un filtro es como una **lupa con una regla especial** que pasas por toda la foto, cuadrito por cuadrito. En cada posición hace una cuenta con los píxeles que ve y anota el resultado en una hoja nueva.

### Aspectos Clave

1. **Píxeles y resolución:**
   - Cada píxel vale de **0 (negro) a 255 (blanco)**; los valores intermedios son tonos de gris.
   - El número de filas y columnas es la **resolución**. Ejemplo: imagen de 7×7 con un cuadro blanco al centro:
     ```
     0   0   0   0   0   0   0
     0   0   0   0   0   0   0
     0   0  255 255 255  0   0
     0   0  255 255 255  0   0
     0   0  255 255 255  0   0
     0   0   0   0   0   0   0
     0   0   0   0   0   0   0
     ```

2. **Canales de color (RGB):**
   - Una imagen a color tiene **3 capas**: Rojo, Verde y Azul.
   - Fondo morado = (R 150, G 0, B 255); cuadro amarillo = (R 255, G 255, B 0).
   - Una foto de 1920×1080 a color tiene 1920 × 1080 × 3 = **6,220,800 números**.

3. **Filtros y kernels:**
   - Un **kernel** es una matriz pequeña de pesos. El de Microsoft Learn (filtro Laplace) es:
     ```
     -1 -1 -1
     -1  8 -1
     -1 -1 -1
     ```
   - **Convolución:** el kernel se coloca sobre un parche de 3×3, se multiplica cada píxel por su peso, se suman los resultados y el valor se guarda en una imagen nueva. Luego se desplaza un píxel y se repite.
   - **Ejemplo paso 1:** la esquina superior izquierda solo tiene un 255 en la posición inferior derecha → `255 × -1 = -255`.
   - **Ejemplo paso 2:** al moverse a la derecha hay dos 255 en la fila inferior → `-510`.
   - Los valores fuera de 0–255 se **ajustan (clip)** y el borde exterior se rellena con **padding** (normalmente 0).

4. **Efectos de distintos kernels:**

   | Filtro | Kernel | Efecto |
   |---|---|---|
   | Laplace | `[[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]` | Resalta **bordes** |
   | Desenfoque (blur) | Todos `1/9` | Suaviza / reduce ruido |
   | Enfoque (sharpen) | `[[0,-1,0],[-1,5,-1],[0,-1,0]]` | Aumenta nitidez |
   | Sobel horizontal | `[[-1,0,1],[-2,0,2],[-1,0,1]]` | Bordes **verticales** |

### Práctica en Python: convolución desde cero
```python
import numpy as np

imagen = np.zeros((7, 7))
imagen[2:5, 2:5] = 255                      # cuadro blanco al centro

kernel = np.array([[-1, -1, -1],
                   [-1,  8, -1],
                   [-1, -1, -1]])

# Padding de 1 píxel con ceros para conservar el tamaño 7x7
con_padding = np.pad(imagen, 1, constant_values=0)
salida = np.zeros_like(imagen)

for fila in range(imagen.shape[0]):
    for col in range(imagen.shape[1]):
        parche = con_padding[fila:fila + 3, col:col + 3]
        salida[fila, col] = np.sum(parche * kernel)    # multiplicar y sumar

print(salida.astype(int))                   # valores crudos (con negativos)
print(np.clip(salida, 0, 255).astype(int))  # ajustados al rango 0-255
```
- **Explicación:**
  - El doble `for` desliza el kernel por toda la imagen.
  - En las zonas planas (todo 0 o todo 255) el resultado es 0: no hay cambio, no hay borde.
  - En las orillas del cuadro aparecen valores grandes: **ahí están los bordes**.
  - Nota: como aquí agregamos padding, la esquina `(1,1)` corresponde al primer parche completo del ejemplo de Microsoft Learn y da `-255`; la `(1,2)` da `-510`.

### Práctica con una foto real
```python
# pip install opencv-python matplotlib
import cv2
import matplotlib.pyplot as plt

foto = cv2.imread("perro.jpg", cv2.IMREAD_GRAYSCALE)        # cualquier imagen tuya
bordes = cv2.filter2D(foto, ddepth=-1, kernel=kernel)        # mismo kernel Laplace
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].imshow(foto, cmap="gray"); ax[0].set_title("Original")
ax[1].imshow(bordes, cmap="gray"); ax[1].set_title("Filtro Laplace (bordes)")
plt.show()
```
- **Explicación:** `filter2D` hace la misma convolución, optimizada. Se llama **filtrado convolucional** y es la base de las CNN del siguiente tema.

### Recursos
- [Image Kernels explained visually – Setosa](https://setosa.io/ev/image-kernels/)
