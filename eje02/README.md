# Ejercicio 02: Singleton con Recursos Compartidos (Logger)

## Descripción
Este módulo implementa un sistema de registro (`Logger`) que escribe eventos en un archivo de texto llamado `bitacora.log`. Se utiliza el patrón **Singleton** para garantizar que existe un único punto de acceso al archivo de registro, centralizando la gestión de logs.

## Detalles de Implementación
- **Clase:** `Logger` (usa `SingletonMeta`).
- **Persistencia:** Archivo local `bitacora.log`.
- **Formato:** Los mensajes incluyen una marca de tiempo automática (`datetime`).

## Pruebas
Al ejecutar el script, se simulan eventos desde diferentes variables, confirmando que todas escriben en el mismo archivo físico y a través de la misma instancia en memoria.