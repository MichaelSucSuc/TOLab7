# Laboratorio 7: Patrón Singleton

**ASIGNATURA:** Tecnología de Objetos

**TÍTULO DE LA PRÁCTICA:** Ejercicios - Singleton

**NÚMERO DE PRÁCTICA:** 9

**AÑO LECTIVO:** 2025

**SEMESTRE:** 6

**FECHA DE PRESENTACIÓN:** 08/12/2025

**DOCENTE:** CARLO JOSE LUIS CORRALES DELGADO

**INTEGRANTES:**
- MICHAEL BENJAMIN SUCLLE SUCA
- JHASTYN JEFFERSON PAYEHUANCA RIQUELME

---

## Resumen de la Práctica

Este laboratorio implementa y valida el patrón de diseño **Singleton** en Python, demostrando sus aplicaciones prácticas desde casos básicos hasta validación de thread-safety en entornos concurrentes. El trabajo comprende cinco ejercicios progresivos que cubren diferentes aspectos del patrón.

## Estructura del Proyecto

**patrones.py** contiene la metaclase `SingletonMeta` que implementa el patrón Singleton usando Double-Checked Locking, garantizando que solo existe una instancia de cada clase y proporcionando thread-safety automática para la creación de instancias.

**eje01/** implementa un Singleton básico de Configuración que demuestra cómo centralizar configuraciones globales del sistema (idioma, zona horaria) evitando duplicidad de datos. Usa la metaclase `SingletonMeta` heredada desde patrones.py.

**eje02/** crea un Logger Singleton que escribe eventos en un archivo bitacora.log, garantizando un único punto de acceso al recurso de archivo. Demuestra la aplicación del patrón para proteger recursos compartidos.

**eje03/** simula una Conexión a Base de Datos (ConexionBD) que ejemplifica cómo el Singleton protege un recurso crítico evitando múltiples conexiones redundantes. Implementa métodos conectar() y desconectar() que verifican estado antes de actuar.

**eje04/** es un juego gráfico "Atrapa el Bloque" que demuestra el Singleton en un contexto interactivo. Usa `ControlJuego` como Singleton para centralizar el estado global (puntaje, vidas, posiciones), separando la lógica de juego de la interfaz gráfica con Pygame. El jugador controla una barra azul con flechas, atrapa bloques naranjas para sumar puntos, y pierde vidas cuando los bloques caen. La dificultad aumenta progresivamente. Incluye demostración de unicidad al inicio.

**eje05/** es una suite completa de pruebas de concurrencia que valida la thread-safety del Singleton. Implementa cuatro pruebas progresivas: Unicidad verifica que todas las referencias apunten a la misma instancia en memoria (test `a is b is c`). Concurrencia Básica crea 5 hilos que incrementan un contador 100 veces cada uno (500 total esperado) para detectar race conditions. Estrés escala a 20 hilos con 500 iteraciones cada uno (10,000 total) para validar comportamiento bajo carga extrema. Historial verifica que cada una de 150 operaciones (3 hilos × 50 iteraciones) se registre sin pérdida, garantizando atomicidad. Si todas pasan, el Singleton es 100% thread-safe porque el `threading.Lock()` interno previene race conditions.

## Metodología de Prueba (eje05)

La metodología valida que el Singleton es thread-safe mediante cuatro pruebas progresivas. La Prueba 1 de Unicidad verifica que todas las referencias apunten a la misma instancia en memoria. La Prueba 2 de Concurrencia Básica crea 5 hilos que incrementan un contador 100 veces cada uno (500 total esperado) para detectar race conditions. La Prueba 3 de Estrés escala a 20 hilos con 500 iteraciones cada uno (10,000 total) para validar comportamiento bajo carga extrema. La Prueba 4 de Historial verifica que cada una de las 150 operaciones (3 hilos × 50 iteraciones) se registre sin pérdida, garantizando atomicidad.

Si todas las pruebas pasan, el contador es exacto en cada caso (500, 10,000, 150) y el Singleton es 100% thread-safe porque el `threading.Lock()` interno previene race conditions y garantiza que solo un hilo modifica los datos a la vez.

## Requisitos Cumplidos

Patrón Singleton correctamente implementado con metaclase que usa Double-Checked Locking para garantizar instancia única incluso bajo concurrencia. Código limpio y bien comentado con docstrings en todas las clases y métodos. Aplicaciones prácticas demostrando gestión de recursos compartidos (Logger, Base de Datos, Estado de Juego). Interfaz gráfica interactiva con Pygame en eje04 que muestra el patrón en contexto visual. Suite completa de pruebas de thread-safety con validación automática de cuatro aspectos críticos. Manejo correcto de imports y rutas relativas para resolver patrones.py desde cualquier ejercicio.

## Conclusiones

El patrón Singleton proporciona un mecanismo robusto para garantizar la existencia de una única instancia y centralizar acceso a recursos compartidos. La implementación con metaclase proporciona elegancia y automatización. El Double-Checked Locking asegura thread-safety sin sacrificar rendimiento significativamente. El patrón es especialmente útil para gestionar configuraciones globales, acceso a bases de datos, logging y estado de aplicaciones. Las pruebas demuestran que incluso bajo estrés extremo (10,000 operaciones concurrentes), el patrón mantiene integridad de datos perfecta.