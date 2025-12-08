import threading
from typing import Any, Dict, Type

class SingletonMeta(type):
    _instances: Dict[Type, Any] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        # Primer chequeo sin bloqueo 
        if cls not in cls._instances:
            # Bloqueo para garantizar atomicidad en la creación
            with cls._lock:
                # Double-Checked Locking
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]