# Ejercicio 03: Conexión Simulada a Base de Datos (Aplicado)

## Descripción
Simulación de un controlador de base de datos (`ConexionBD`). Este ejercicio demuestra cómo el patrón **Singleton** protege un recurso crítico (la conexión a la BD) evitando que múltiples partes del código abran conexiones redundantes.

## Funcionalidad
- **Unicidad:** Solo puede existir una instancia del gestor de conexión.
- **Gestión de Estado:** Métodos `conectar()` y `desconectar()` que verifican el estado actual (`_conectado`) antes de actuar.
- **Protección:** Si se llama a `conectar()` cuando ya existe una sesión, el sistema reutiliza la existente en lugar de crear una nueva o lanzar un error.

## Ejecución
```bash
python main.py