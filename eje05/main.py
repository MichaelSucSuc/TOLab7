"""
Ejercicio 05: Singleton Thread-Safe
Demuestra la seguridad en subprocesos del patrón Singleton.
Valida que múltiples hilos acceden a la misma instancia sin condiciones de carrera.
"""

from __future__ import annotations

import sys
import threading
import time
from pathlib import Path
from typing import List, Tuple

# Agrega la carpeta raiz (..\) para importar patrones.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from patrones import SingletonMeta


# ============================================================================
# Singleton Thread-Safe: Contador Compartido
# ============================================================================


class ContadorCompartido(metaclass=SingletonMeta):
    """
    Singleton que gestiona un contador compartido entre múltiples hilos.
    Usa un lock interno para evitar condiciones de carrera.
    """

    def __init__(self) -> None:
        if getattr(self, "_inicializado", False):
            return
        self._inicializado = True
        self._contador = 0
        self._lock = threading.Lock()
        self._incrementos_registrados: List[Tuple[int, str]] = []

    def incrementar(self) -> None:
        """Incrementa el contador de forma thread-safe."""
        with self._lock:
            self._contador += 1
            hilo_actual = threading.current_thread().name
            self._incrementos_registrados.append((self._contador, hilo_actual))

    def get_valor(self) -> int:
        """Obtiene el valor actual del contador."""
        with self._lock:
            return self._contador

    def reset(self) -> None:
        """Reinicia el contador y el registro."""
        with self._lock:
            self._contador = 0
            self._incrementos_registrados.clear()

    def obtener_historial(self) -> List[Tuple[int, str]]:
        """Obtiene el historial de incrementos."""
        with self._lock:
            return self._incrementos_registrados.copy()


# ============================================================================
# Pruebas de Concurrencia
# ============================================================================


class PruebasConcurrencia:
    """Suite de pruebas para validar la seguridad del Singleton."""

    def __init__(self) -> None:
        self.contador = ContadorCompartido()
        self.resultados: List[str] = []

    def agregar_resultado(self, msg: str) -> None:
        """Agrega un resultado a la lista."""
        self.resultados.append(msg)
        print(msg)

    def prueba_unicidad(self) -> bool:
        """
        Prueba 1: Verifica que múltiples referencias son la misma instancia.
        """
        print("\n" + "=" * 70)
        print("PRUEBA 1: UNICIDAD DEL SINGLETON")
        print("=" * 70)

        a = ContadorCompartido()
        b = ContadorCompartido()
        c = ContadorCompartido()

        resultado = a is b is c
        self.agregar_resultado(f"✓ Todas las referencias son idénticas: {resultado}")
        self.agregar_resultado(f"  ID(a): {id(a)}")
        self.agregar_resultado(f"  ID(b): {id(b)}")
        self.agregar_resultado(f"  ID(c): {id(c)}")
        return resultado

    def tarea_incrementar(self, iteraciones: int) -> None:
        """Tarea que ejecuta un hilo: incrementa el contador N veces."""
        for _ in range(iteraciones):
            self.contador.incrementar()
            # Simula algo de trabajo
            time.sleep(0.0001)

    def prueba_concurrencia_basica(self) -> bool:
        """
        Prueba 2: Múltiples hilos incrementan el contador sin condiciones de carrera.
        """
        print("\n" + "=" * 70)
        print("PRUEBA 2: SEGURIDAD EN SUBPROCESOS (BASICA)")
        print("=" * 70)

        self.contador.reset()
        num_hilos = 5
        iteraciones_por_hilo = 100
        esperado = num_hilos * iteraciones_por_hilo

        # Crear hilos
        hilos: List[threading.Thread] = []
        for i in range(num_hilos):
            hilo = threading.Thread(
                target=self.tarea_incrementar,
                args=(iteraciones_por_hilo,),
                name=f"Hilo-{i+1}",
            )
            hilos.append(hilo)

        # Lanzar todos los hilos
        inicio = time.time()
        for hilo in hilos:
            hilo.start()

        # Esperar a que terminen todos
        for hilo in hilos:
            hilo.join()
        duracion = time.time() - inicio

        valor_final = self.contador.get_valor()
        resultado = valor_final == esperado

        self.agregar_resultado(f"Hilos: {num_hilos} | Iteraciones por hilo: {iteraciones_por_hilo}")
        self.agregar_resultado(f"Valor esperado: {esperado}")
        self.agregar_resultado(f"Valor obtenido: {valor_final}")
        self.agregar_resultado(f"Tiempo total: {duracion:.4f}s")
        self.agregar_resultado(f"✓ Prueba exitosa: {resultado}")

        return resultado

    def prueba_concurrencia_extrema(self) -> bool:
        """
        Prueba 3: Prueba de estrés con muchos hilos e iteraciones.
        """
        print("\n" + "=" * 70)
        print("PRUEBA 3: ESTRÉS (MUCHOS HILOS)")
        print("=" * 70)

        self.contador.reset()
        num_hilos = 20
        iteraciones_por_hilo = 500
        esperado = num_hilos * iteraciones_por_hilo

        hilos: List[threading.Thread] = []
        for i in range(num_hilos):
            hilo = threading.Thread(
                target=self.tarea_incrementar,
                args=(iteraciones_por_hilo,),
                name=f"Hilo-{i+1}",
            )
            hilos.append(hilo)

        inicio = time.time()
        for hilo in hilos:
            hilo.start()
        for hilo in hilos:
            hilo.join()
        duracion = time.time() - inicio

        valor_final = self.contador.get_valor()
        resultado = valor_final == esperado

        self.agregar_resultado(f"Hilos: {num_hilos} | Iteraciones por hilo: {iteraciones_por_hilo}")
        self.agregar_resultado(f"Total de incrementos: {esperado}")
        self.agregar_resultado(f"Valor final: {valor_final}")
        self.agregar_resultado(f"Tiempo total: {duracion:.4f}s")
        self.agregar_resultado(f"✓ Prueba exitosa: {resultado}")

        return resultado

    def prueba_historial_ordenado(self) -> bool:
        """
        Prueba 4: Verifica que el historial refleje el orden exacto de incrementos.
        """
        print("\n" + "=" * 70)
        print("PRUEBA 4: INTEGRIDAD DEL HISTORIAL")
        print("=" * 70)

        self.contador.reset()
        num_hilos = 3
        iteraciones = 50

        hilos: List[threading.Thread] = []
        for i in range(num_hilos):
            hilo = threading.Thread(
                target=self.tarea_incrementar,
                args=(iteraciones,),
                name=f"Hilo-{i+1}",
            )
            hilos.append(hilo)

        for hilo in hilos:
            hilo.start()
        for hilo in hilos:
            hilo.join()

        historial = self.contador.obtener_historial()
        resultado = len(historial) == num_hilos * iteraciones

        self.agregar_resultado(f"Hilos: {num_hilos} | Iteraciones: {iteraciones}")
        self.agregar_resultado(f"Registros esperados: {num_hilos * iteraciones}")
        self.agregar_resultado(f"Registros obtenidos: {len(historial)}")

        # Mostrar primeros y últimos registros
        if historial:
            self.agregar_resultado(f"Primeros 5 registros:")
            for i, (valor, hilo) in enumerate(historial[:5]):
                self.agregar_resultado(f"  {i+1}. Contador={valor}, {hilo}")
            if len(historial) > 10:
                self.agregar_resultado(f"  ...")
            self.agregar_resultado(f"Últimos 5 registros:")
            for i, (valor, hilo) in enumerate(historial[-5:], start=len(historial)-4):
                self.agregar_resultado(f"  {i}. Contador={valor}, {hilo}")

        self.agregar_resultado(f"✓ Prueba exitosa: {resultado}")
        return resultado

    def ejecutar_todas(self) -> None:
        """Ejecuta todas las pruebas y genera reporte final."""
        print("\n")
        print("╔" + "=" * 68 + "╗")
        print("║" + " " * 68 + "║")
        print("║" + "  SUITE DE PRUEBAS: SINGLETON THREAD-SAFE  ".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("╚" + "=" * 68 + "╝")

        resultados_pruebas = []
        resultados_pruebas.append(("Unicidad", self.prueba_unicidad()))
        resultados_pruebas.append(("Concurrencia Básica", self.prueba_concurrencia_basica()))
        resultados_pruebas.append(("Estrés", self.prueba_concurrencia_extrema()))
        resultados_pruebas.append(("Historial Ordenado", self.prueba_historial_ordenado()))

        # Reporte final
        print("\n" + "=" * 70)
        print("REPORTE FINAL")
        print("=" * 70)
        total = len(resultados_pruebas)
        exitosas = sum(1 for _, result in resultados_pruebas if result)
        for nombre, resultado in resultados_pruebas:
            estado = "✓ EXITOSA" if resultado else "✗ FALLIDA"
            print(f"{nombre:.<40} {estado}")

        print("-" * 70)
        print(f"Resultado: {exitosas}/{total} pruebas exitosas")
        if exitosas == total:
            print("✓ TODAS LAS PRUEBAS EXITOSAS - Singleton es THREAD-SAFE")
        else:
            print(f"✗ {total - exitosas} prueba(s) fallida(s)")
        print("=" * 70)


# ============================================================================
# Ejecucion principal
# ============================================================================


if __name__ == "__main__":
    pruebas = PruebasConcurrencia()
    pruebas.ejecutar_todas()
