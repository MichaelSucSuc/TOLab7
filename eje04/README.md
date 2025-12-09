# Ejercicio 04: Juego Interactivo con Singleton

## Descripción

Este ejercicio implementa un juego gráfico llamado "Atrapa Bloques Evita Enemigos" utilizando el patrón Singleton para gestionar el estado global. El juego demuestra cómo centralizar la lógica y estado del programa en una única instancia compartida, separando claramente la interfaz gráfica de la lógica de negocio mediante una arquitectura modular en tres archivos independientes.

## Cómo Jugar

El jugador controla una barra azul en la parte inferior de la pantalla usando las flechas izquierda y derecha. Dos tipos de objetos caen desde la parte superior: bloques naranjas circulares y enemigos rojos triangulares con ojos amenazantes. El objetivo es atrapar bloques (ganan +10 puntos) y evitar enemigos. Los enemigos que caen sin ser tocados dan +5 puntos bonus. El jugador comienza con 3 vidas y pierde una cada vez que toca un enemigo o un bloque cae sin ser atrapado. La dificultad aumenta progresivamente conforme crece el puntaje.

## Arquitectura del Proyecto

**estado.py** contiene toda la lógica del juego con `ControlJuego` como Singleton, clases `Objeto` y `TipoObjeto` para gestionar bloques y enemigos, y la clase `Ajustes` con configuración inmutable.

**interfaz.py** maneja presentación visual y eventos de entrada, renderizando bloques como círculos naranjas y enemigos como triángulos rojos con ojos, a 60 FPS.

**main.py** es el punto de entrada que demuestra el Singleton (verificando unicidad a is b) antes de iniciar el juego.

## Cumplimiento de Requisitos

Patrón Singleton correctamente implementado con metaclase `SingletonMeta` garantizando una única instancia. Separación clara de responsabilidades: lógica en estado.py, presentación en interfaz.py, orquestación en main.py. Thread-safety automática heredada del patrón base. Interfaz gráfica interactiva a 60 FPS con renderización detallada. Dinámica progresiva con velocidades incrementales. Mecánicas variadas: bloques +10 pts, enemigos evitados +5 pts, enemigos tocados -1 vida. Demostración de unicidad ejecutada antes del juego.

## Ejecución

```bash
cd eje04
python main.py
```

## Conclusión

Demuestra la efectividad del Singleton en aplicaciones complejas e interactivas. La arquitectura modular permite escalar fácilmente sin contaminar la lógica con detalles de presentación.
