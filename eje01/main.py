import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from patrones import SingletonMeta

class Configuracion(metaclass=SingletonMeta):
    """Clase Singleton para manejar la configuración global del sistema que almacena preferencias como idioma y zona horaria"""
    
    def __init__(self):
        # Inicializamos
        self.idioma: str = "ES"
        self.zona_horaria: str = "UTC-5"
    
    def mostrar_configuracion(self) -> None:
        """Imprime los valores actuales de la configuración"""
        print(f"Configuración Actual -> Idioma: {self.idioma} | Zona Horaria: {self.zona_horaria}")

# --- Bloque de Prueba ---
if __name__ == "__main__":
    print("--- Ejercicio 01: Configuración Global ---")
    
    # Creamos la primera instancia y modificamos valores
    config_admin = Configuracion()
    print(f"Valores en Objeto 1:")
    config_admin.mostrar_configuracion()
    
    print("\n[!] Cambiando idioma a 'EN' y zona a 'UTC+12' en Objeto 1...")
    config_admin.idioma = "EN"
    config_admin.zona_horaria = "UTC+12"
    
    # Creamos una segunda instancia en otra parte del código
    config_usuario = Configuracion()
    
    # Verificamos que la segunda instancia refleje los cambios de la primera
    print(f"\nValores en Objeto 2:")
    config_usuario.mostrar_configuracion()
    
    # Verificación (Singleton puro)
    print(f"\n¿Son config_admin y config_usuario el mismo objeto en memoria?")
    es_mismo_objeto = config_admin is config_usuario
    print(f"Resultado: {es_mismo_objeto}")
    
    if es_mismo_objeto:
        print("ÉXITO: El patrón Singleton funciona correctamente")
    else:
        print("ERROR: Se crearon instancias diferentes")