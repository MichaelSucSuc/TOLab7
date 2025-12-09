"""Snake clasico de Nokia implementado con Singleton para el estado global."""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import pygame

# Permite importar el Singleton definido en la carpeta raiz del laboratorio.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from patrones import SingletonMeta

