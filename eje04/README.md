# Ejercicio 04: Juego Interactivo con Singleton

## Descripción

Este ejercicio implementa un juego gráfico llamado "Atrapa el Bloque" utilizando el patrón Singleton para gestionar el estado global de la aplicación. El juego demuestra cómo centralizar la lógica y estado del programa en una única instancia compartida, separando claramente la interfaz gráfica de la lógica de negocio.

## Objetivo

Aplicar el patrón Singleton en un contexto práctico e interactivo, mostrando cómo el patrón facilita la gestión de estado global en aplicaciones con interfaz gráfica. El juego valida que las decisiones de diseño basadas en Singleton mejoran la mantenibilidad y escalabilidad del código.

## Cómo Jugar

El jugador controla una barra azul en la parte inferior de la pantalla usando las flechas izquierda y derecha. El objetivo es atrapar bloques naranjas que caen desde la parte superior. Cada bloque atrapado suma 10 puntos y aumenta la dificultad (velocidad). El jugador comienza con 3 vidas y pierde una cada vez que un bloque cae sin ser atrapado. El juego termina cuando se agotan las vidas. Presionando R se reinicia una nueva partida y ESC cierra el juego.

## Cumplimiento de Requisitos

El ejercicio cumple con los requisitos académicos del laboratorio de la siguiente manera:

**Patrón Singleton Implementado Correctamente:** La clase `ControlJuego` usa la metaclase `SingletonMeta` importada desde patrones.py, garantizando que solo existe una instancia del controlador durante toda la ejecución. El código verifica la unicidad con `if getattr(self, "_inicializado", False): return` en el `__init__`, evitando reinicializaciones múltiples.

**Separación de Responsabilidades:** La lógica del juego reside en `ControlJuego` (estado, reglas, colisiones) mientras que `InterfazJuego` maneja únicamente renderización y eventos. Esto demuestra que el Singleton centraliza correctamente el estado sin entrelazarlo con detalles de presentación.

**Thread-Safe por Herencia:** Al usar `SingletonMeta` de patrones.py, que implementa Double-Checked Locking, el `ControlJuego` es automáticamente thread-safe. Aunque este ejercicio no usa múltiples hilos, hereda la seguridad del patrón base.

**Interfaz Gráfica con Pygame:** El juego implementa un canvas interactivo con renderizado suave a 60 FPS. La barra del jugador se dibuja en azul, los bloques en naranja, y hay overlays semitransparentes para GAME OVER y estado. Esto demuestra aplicación práctica del Singleton en contextos visuales complejos.

**Dinámica Progresiva:** La dificultad aumenta conforme crece la serpiente (en este caso, conforme aumenta el puntaje), haciendo el juego más desafiante. La velocidad se calcula dinámicamente según el puntaje, demostrando que el Singleton puede manejar lógica de estado compleja.

**Demostración de Unicidad:** Antes de iniciar el juego, se ejecuta `demostrar_singleton()` que crea dos referencias `a` y `b` a `ControlJuego()`, verifica que `a is b` es `True`, cambia el puntaje en `a` y confirma que se refleja en `b`. Esto prueba visualmente que ambas referencias apuntan a la misma instancia.

**Código Bien Comentado:** Todas las clases y métodos tienen docstrings descriptivos. Las secciones están claramente delimitadas con comentarios de encabezado. Los parámetros y tipos de retorno están anotados con type hints de Python.

**Manejo de Importes Correcto:** El código dinámicamente agrega la carpeta raíz al `sys.path` para resolver patrones.py, permitiendo ejecutar desde cualquier ubicación sin cambiar variables de entorno.

## Ejecución

Para jugar, navega a la carpeta eje04 y ejecuta:

```bash
python main.py
```

El juego mostrará primero la demostración de Singleton en consola, luego abrirá la ventana gráfica.

## Tecnologías Utilizadas

Python 3.11 con Pygame 2.6.1 para renderización gráfica y eventos. La aplicación usa `dataclass` para configuración inmutable y `typing` para anotaciones de tipo.

## Conclusión

El ejercicio demuestra que el patrón Singleton es efectivo no solo para casos simples (configuración, logging) sino también en aplicaciones complejas e interactivas. La centralización de estado en `ControlJuego` facilita agregar nuevas funcionalidades (power-ups, niveles, guardado de progreso) sin afectar la interfaz gráfica. El patrón proporciona un punto de acceso único y previsible al estado del juego desde cualquier parte del código.
