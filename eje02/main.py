import sys
import os
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from patrones import SingletonMeta

class Logger(metaclass=SingletonMeta):
    """
    Sistema de Log centralizado
    Escribe mensajes en un archivo de texto con marca de tiempo
    """
    
    def __init__(self):
        # Definimos el nombre del archivo de log
        self.nombre_archivo = "bitacora.log"
    
    def log(self, mensaje: str) -> None:
        """
        Registra un mensaje en el archivo de log
        Formato: [YYYY-MM-DD HH:MM:SS] Mensaje
        """
        # Obtenemos fecha y hora actual
        ahora = datetime.datetime.now()
        timestamp = ahora.strftime("%Y-%m-%d %H:%M:%S")
        
        # Preparamos la línea a escribir
        entrada_log = f"[{timestamp}] {mensaje}\n"
        
        # Abrimos en modo 'append' (a) para no sobrescribir el historial
        # Usamos 'utf-8' para soportar tildes y caracteres especiales
        try:
            with open(self.nombre_archivo, "a", encoding="utf-8") as archivo:
                archivo.write(entrada_log)
            print(f"[Consola] Log registrado: {mensaje}")
        except IOError as e:
            print(f"Error crítico escribiendo en log: {e}")

# --- Bloque de Prueba ---
if __name__ == "__main__":
    print("--- Ejercicio 02: Logger Centralizado ---")
    
    # Simulación de diferentes partes del sistema
    logger_sistema = Logger()
    logger_auth = Logger()
    
    # Registrar eventos desde "distintos" loggers
    logger_sistema.log("El sistema ha iniciado correctamente.")
    logger_auth.log("Usuario 'admin' ha iniciado sesión.")
    
    # Verificación de Singleton
    print(f"\nVerificando integridad referencial...")
    if logger_sistema is logger_auth:
        print("ÉXITO: Ambos loggers son la misma instancia.")
    else:
        print("ERROR: Instancias duplicadas detectadas.")
        
    print(f"\nRevisa el archivo '{logger_sistema.nombre_archivo}' para ver los resultados.")