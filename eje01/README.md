# Ejercicio 01: Singleton Básico (Configuración)

## Descripción
Este ejercicio implementa una clase `Configuracion` utilizando el patrón **Singleton**. El objetivo es garantizar que las configuraciones globales del sistema (como idioma y zona horaria) sean consistentes en toda la aplicación, evitando duplicidad de datos o desincronización.

## Implementación Técnica
- Se utiliza una **Metaclase (`SingletonMeta`)** definida en `patrones.py` para abstraer la lógica de creación única.
- La clase `Configuracion` define atributos de instancia que persisten durante todo el ciclo de vida del programa.
- Se verifica la unicidad comparando las direcciones de memoria de dos variables instanciadas por separado (`is`).

## Ejecución
Para probar el ejercicio:
```bash
python main.py