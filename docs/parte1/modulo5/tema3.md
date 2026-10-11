# Tema 3: Redes neuronales convolucionales (CNN) — Fundamentos técnicos

### Descripción
En el tema anterior **nosotros** elegimos el kernel (Laplace) para detectar bordes. Una **CNN** hace lo mismo, pero **aprende sola** cuáles son los mejores kernels para la tarea. Usa filtros para extraer mapas de características numéricos de las imágenes y luego alimenta esos valores a un modelo de deep learning que predice una etiqueta.

Analogía: un detective novato al principio solo nota cosas simples (líneas, colores). Con experiencia combina esas pistas en patrones (orejas, bigotes) y al final concluye "es un gato". Las primeras capas de una CNN detectan bordes, las intermedias formas y las últimas conceptos completos.

### Aspectos Clave

1. **Arquitectura paso a paso:**
   ```
   Imagen → [Convolución + activación] → [Pooling] → ... → [Flatten] → [Capas densas] → [Softmax] → [0.2, 0.5, 0.3]
   ```
   1. **Capas de convolución (filtros):** kernels con pesos que empiezan **aleatorios** y producen **mapas de características (feature maps)**.
   2. **Función de activación (ReLU):** convierte los valores negativos en 0 (`max(0, x)`). Permite aprender relaciones no lineales.
   3. **Pooling:** reduce el tamaño del mapa quedándose con lo más importante. *Max pooling* 2×2 toma el valor máximo de cada bloque y reduce el tamaño a la mitad.
   4. **Flatten (aplanar):** convierte los mapas 2D en un vector 1D.
   5. **Red totalmente conectada (fully connected):** combina las características para decidir.
   6. **Softmax:** convierte la salida en probabilidades que suman 1, por ejemplo `[0.2, 0.5, 0.3]` para [manzana, plátano, naranja].

2. **Entrenamiento:**
   - Se alimentan imágenes con etiquetas conocidas (0: manzana, 1: plátano, 2: naranja).
   - Para un plátano, la salida ideal es `[0.0, 1.0, 0.0]`.
   - La diferencia entre la predicción y lo esperado es la **pérdida (loss)**.
   - **Backpropagation** ajusta los pesos de la red densa **y de los kernels** para reducir la pérdida.
   - Se repite durante varias **épocas** hasta encontrar los mejores pesos, que luego se guardan para predecir imágenes nuevas.

3. **Por qué funcionan tan bien con imágenes:**
   - **Pesos compartidos:** el mismo kernel recorre toda la imagen, así que detecta un borde esté donde esté. Muchos menos parámetros que una red densa.
   - **Jerarquía de características:** bordes → texturas → partes → objetos.
   - **Invarianza a la traslación:** un gato en la esquina sigue siendo gato.

4. **Arquitecturas famosas:** LeNet (1998, dígitos), AlexNet (2012, detonó el boom del deep learning), VGG, ResNet (conexiones residuales, cientos de capas), EfficientNet. Para detección: R-CNN, YOLO.

### Práctica: una CNN mínima con PyTorch
```python
# pip install torch torchvision
import torch
import torch.nn as nn

class MiniCNN(nn.Module):
    def __init__(self, num_clases=3):
        super().__init__()
        self.extractor = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),  # 16 filtros 3x3 sobre RGB
            nn.ReLU(),
            nn.MaxPool2d(2),                             # 64x64 -> 32x32
            nn.Conv2d(16, 32, kernel_size=3, padding=1), # 32 filtros
            nn.ReLU(),
            nn.MaxPool2d(2),                             # 32x32 -> 16x16
        )
        self.clasificador = nn.Sequential(
            nn.Flatten(),                                # 32 * 16 * 16 = 8192 valores
            nn.Linear(32 * 16 * 16, 64),
            nn.ReLU(),
            nn.Linear(64, num_clases),
        )

    def forward(self, x):
        return self.clasificador(self.extractor(x))

modelo = MiniCNN()
imagen_falsa = torch.rand(1, 3, 64, 64)                 # 1 imagen RGB de 64x64
probabilidades = torch.softmax(modelo(imagen_falsa), dim=1)
print(probabilidades)   # ej. tensor([[0.33, 0.35, 0.32]]) -> sin entrenar, casi al azar
```
- **Explicación:**
  - `Conv2d(3, 16, 3)`: 16 kernels de 3×3 que reciben 3 canales (RGB). Sus pesos son aleatorios al inicio.
  - `MaxPool2d(2)`: reduce a la mitad el ancho y alto.
  - `Flatten` + `Linear`: la red densa que decide.
  - Sin entrenar, las probabilidades son casi iguales. Al entrenar con fotos de frutas, los kernels aprenden a detectar formas y colores útiles.

### Limitación que motivó a los Transformers
Una CNN ve **localmente** (kernels de 3×3); relacionar dos zonas lejanas de la imagen requiere muchas capas. Los **Vision Transformers** usan atención para relacionar cualquier parte con cualquier otra desde la primera capa (siguiente tema).

### Recursos
- [CNN Explainer (visualización interactiva)](https://poloclub.github.io/cnn-explainer/)
- [Funciones de activación ReLU y sigmoide (acordeón AI-900)](https://github.com/josejesusguzman/acordeon-ia-900/blob/main/docs/intro_deep_learning.md)
