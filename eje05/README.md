# Ejercicio 05: Singleton Thread-Safe (Validación y Calidad)

## Descripción
Este ejercicio demuestra la **seguridad en subprocesos (thread-safety)** del patrón Singleton implementado en `patrones.py`. La metaclase `SingletonMeta` usa **Double-Checked Locking** para garantizar que solo una instancia existe incluso cuando múltiples hilos intentan crearla simultáneamente.

## Objetivo
Validar y demostrar que:
1. El Singleton es **thread-safe** (seguro en entornos concurrentes)
2. No hay **condiciones de carrera (race conditions)** al acceder a la instancia compartida
3. Los datos se modifican de forma atómica sin corrupción

## Metodología de Prueba

### Prueba 1: Unicidad
Verifica que todas las referencias a `ContadorCompartido()` apunten a la misma instancia en memoria.

### Prueba 2: Concurrencia Básica
- **5 hilos** ejecutan **100 incrementos cada uno** = **500 total esperado**
- Sin sincronización adecuada, habría condiciones de carrera
- Valida que el contador final sea exacto

### Prueba 3: Estrés
- **20 hilos** ejecutan **500 incrementos cada uno** = **10,000 total esperado**
- Prueba el comportamiento bajo carga alta
- Mide tiempo de ejecución

### Prueba 4: Integridad del Historial
- Registra cada incremento con timestamp y nombre de hilo
- Verifica que no se pierdan ni dupliquen registros
- Demuestra orden correcto de operaciones

## Resultados Esperados

Si el Singleton es thread-safe, verás:
```
✓ Todas las referencias son idénticas: True
✓ Concurrencia Básica: contador final = 500
✓ Estrés: contador final = 10,000
✓ Historial: 10,000 registros sin pérdida
✓ TODAS LAS PRUEBAS EXITOSAS
```

## Ejecución
```bash
cd eje05
python main.py
```

## Puntos Clave Validados

- ✓ **Double-Checked Locking:** Previene creación múltiple de instancias
- ✓ **Lock Interno:** Protege acceso al contador compartido
- ✓ **Atomicidad:** Las operaciones no se entrecruzan
- ✓ **Escalabilidad:** Funciona bajo carga alta sin degradación
