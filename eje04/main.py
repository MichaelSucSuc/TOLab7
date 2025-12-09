"""
Punto de entrada del juego 'Atrapa el Bloque'.
Demuestra el uso del patrón Singleton en una aplicación gráfica interactiva.

Módulos:
  - estado.py: Contiene ControlJuego (Singleton) con lógica de juego
  - interfaz.py: Contiene InterfazJuego con renderización y eventos
"""

from estado import ControlJuego
from interfaz import InterfazJuego


def demostrar_singleton() -> None:
    """Demuestra que ControlJuego es un Singleton."""
    print("=" * 60)
    print("DEMOSTRACION DEL PATRON SINGLETON")
    print("=" * 60)
    a = ControlJuego()
    b = ControlJuego()
    print(f"Instancia a: {id(a)}")
    print(f"Instancia b: {id(b)}")
    print(f"Misma instancia: {a is b}")
    a.puntaje = 20
    print(f"Puntaje en a: {a.puntaje} | Puntaje en b: {b.puntaje}")
    print("Iniciando juego...\n")


if __name__ == "__main__":
    demostrar_singleton()
    InterfazJuego().ejecutar()

