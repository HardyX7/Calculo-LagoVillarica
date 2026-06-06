# Calculo Lago Villarrica

Aplicacion de escritorio en Python/Tkinter para modelar el Lago Villarrica con herramientas de calculo diferencial e integral. La app muestra una imagen satelital calibrada, dibuja el contorno del lago, una cuadricula cartesiana, curvas cubicas por tramos, lineas de Riemann, area aproximada, area por integral, volumen idealizado y centroide usado como referencia de abastecimiento.

## Como ejecutar

Desde la carpeta del proyecto:

```bash
python -B main.py
```

El parametro `-B` evita que Python genere carpetas `__pycache__`. El archivo `main.py` tambien activa `sys.dont_write_bytecode` antes de abrir la interfaz.

## Flujo de la app

1. `main.py` crea la ventana principal desde `VistaPrincipal`.
2. `vista.py` arma la pantalla: panel de controles, tarjetas de resultados y panel del mapa.
3. El usuario elige `n` para la suma de Riemann y la cantidad de curvas cubicas.
4. Al presionar `Calcular`, `CalculosDIRECTOS.calcular_modelo()` obtiene area por Riemann, area por integral, volumen y centroide.
5. `cambios_visuales_mapa.py` redibuja el mapa usando el resultado: contorno, area, lineas de Riemann, puntos de control y centroide / abastecimiento.
6. Los botones `Profundizar` explican el metodo usado para curvas, Riemann, integral y datos/limitaciones.

## Archivos principales

- `main.py`: punto de entrada de la aplicacion.
- `vista.py`: construye la interfaz, maneja botones y muestra explicaciones.
- `calculos.py`: contiene dos clases:
  - `CalculosDIRECTOS`: calculos ligados directamente a la materia, como interpolacion cubica, evaluacion de polinomios, suma de Riemann, integrales, centroide, volumen y resultado final.
  - `CalculosIndirectos`: apoyo geometrico y visual, como validaciones, contorno base, conversion de kilometros a coordenadas, grilla, puntos de control y lineas visuales sobre el contorno.
- `cambios_visuales_mapa.py`: dibuja los elementos del modelo sobre la imagen satelital.
- `estilizacion/moldes_widgets.py`: widgets reutilizables, colores, fuentes y canvas de imagen/mapa.
- `estilizacion/constantes.py`: fuentes, coordenadas, parametros de escala y puntos del contorno del lago.
- `estilizacion/MoldeFondo.png`: imagen de fondo de la ventana.
- `estilizacion/LagoVillarricaSatelitalCalibrado.png`: imagen satelital calibrada usada como base del mapa.

## Datos y fuentes

- Area oficial usada para comparar: 175,9 km2.
- Fuente del area oficial: MMA, D.S. N. 19/2013.
- Fuente del contorno: OpenStreetMap, relacion 1922935, Lago Villarrica.
- Fuente de imagen satelital: Esri World Imagery, calibrada al encuadre geografico del modelo.

## Consideraciones del modelo

El contorno real del lago es irregular, por lo que el modelo aproxima sus bordes mediante curvas cubicas por tramos. La suma de Riemann aproxima el area mediante divisiones verticales, mientras que la integral calcula el area entre las curvas superior e inferior. El volumen es idealizado con secciones semicirculares y no representa una medicion batimetrica real.

El centroide se usa como punto de referencia para abastecimiento, pero no garantiza seguridad, profundidad, permisos ambientales ni condiciones practicas de navegacion.
