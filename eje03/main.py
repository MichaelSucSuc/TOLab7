import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from patrones import SingletonMeta

class ConexionBD(metaclass=SingletonMeta):
    """
    Simulador de conexión a Base de Datos
    Gestiona un estado único de conexión para evitar múltiples accesos concurrentes no deseados
    """
    
    def __init__(self):
        # Estado interno: False = Desconectado, True = Conectado
        self._conectado: bool = False
        self.host: str = "192.168.1.10"
        self.puerto: int = 5432
    
    def conectar(self) -> None:
        """Establece la conexión si no está activa"""
        if not self._conectado:
            print(f"[BD] Iniciando conexión a {self.host}:{self.puerto}...")
            time.sleep(1) # Simulamos latencia de red
            self._conectado = True
            print("[BD] Conexión establecida exitosamente")
        else:
            print("[BD Warning] Ya existe una conexión activa, se retorna la sesión actual")

    def desconectar(self) -> None:
        """Cierra la conexión si está activa"""
        if self._conectado:
            print("[BD] Cerrando sesión...")
            time.sleep(0.5)
            self._conectado = False
            print("[BD] Desconectado correctamente")
        else:
            print("[BD Error] No se puede desconectar: No hay sesión activa")

    def estado(self) -> None:
        """Imprime el estado actual de la conexión"""
        status = "ONLINE" if self._conectado else "OFFLINE"
        print(f"Estado del Sistema: {status}")

# --- Bloque de Prueba ---
if __name__ == "__main__":
    print("--- Ejercicio 03: Singleton en Base de Datos ---")
    
    # Instanciamos dos variables que apuntan al Singleton
    conexion_principal = ConexionBD()
    conexion_reportes = ConexionBD()
    
    # Verificamos estado inicial
    conexion_principal.estado()
    
    # Intentamos conectar desde la principal
    print("\n--- Intento 1: Conectar Principal ---")
    conexion_principal.conectar()
    
    # Intentamos conectar desde reportes (debería detectar que ya está abierta)
    print("\n--- Intento 2: Conectar Reportes (Duplicado) ---")
    conexion_reportes.conectar()
    
    # Verificamos que ambos ven el mismo estado
    print("\n--- Verificación de Estado Cruzado ---")
    conexion_reportes.estado()
    
    # 6. Desconexión
    print("\n--- Desconexión ---")
    conexion_principal.desconectar()
    conexion_reportes.estado() # Debería estar offline también