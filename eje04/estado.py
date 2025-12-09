"""Lógica y estado del juego - módulo separado."""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Tuple

import pygame

# Agrega la carpeta raiz (..\) para importar patrones.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from patrones import SingletonMeta


# ============================================================================
# Tipos de objetos que caen
# ============================================================================


class TipoObjeto(Enum):
    """Tipos de objetos en el juego."""
    BLOQUE = 1  # Suma puntos
    ENEMIGO = 2  # Resta vidas


@dataclass
class Objeto:
    """Representa un bloque o enemigo que cae."""
    x: int
    y: float
    tipo: TipoObjeto
    radio: int
    color: Tuple[int, int, int]
    velocidad: float


# ============================================================================
# Configuracion del juego
# ============================================================================


@dataclass(frozen=True)
class Ajustes:
    """Configuración inmutable del juego."""
    ancho: int = 640
    alto: int = 480
    color_fondo: Tuple[int, int, int] = (18, 24, 32)
    color_jugador: Tuple[int, int, int] = (90, 180, 255)
    color_bloque: Tuple[int, int, int] = (255, 140, 0)
    color_enemigo: Tuple[int, int, int] = (220, 50, 50)
    color_texto: Tuple[int, int, int] = (235, 235, 235)
    paddle_ancho: int = 90
    paddle_alto: int = 18
    paddle_vel: int = 8
    objeto_radio: int = 13
    bloque_vel_ini: float = 3.0
    bloque_vel_inc: float = 0.15
    enemigo_vel_ini: float = 1.8
    enemigo_vel_inc: float = 0.08
    vidas_ini: int = 3
    freq_bloque: int = 1000  # ms
    freq_enemigo: int = 1500  # ms


# ============================================================================
# Singleton: Control del estado del juego
# ============================================================================


class ControlJuego(metaclass=SingletonMeta):
    """
    Singleton que gestiona todo el estado del juego.
    Responsabilidades: lógica, colisiones, puntuación, vidas, objetos.
    """

    def __init__(self) -> None:
        if getattr(self, "_init_ok", False):
            return
        self._init_ok = True
        self.cfg = Ajustes()
        self.reiniciar()

    def reiniciar(self) -> None:
        """Reinicia la partida con estado inicial."""
        self.puntaje = 0
        self.vidas = self.cfg.vidas_ini
        self.vel_bloque = self.cfg.bloque_vel_ini
        self.vel_enemigo = self.cfg.enemigo_vel_ini
        self.juego_activo = True
        self.jugador_x = (self.cfg.ancho - self.cfg.paddle_ancho) // 2
        self.objetos: List[Objeto] = []
        self.tiempo_ultimo_bloque = 0
        self.tiempo_ultimo_enemigo = 0

    def _crear_bloque(self, tiempo_actual: int) -> None:
        """Crea un bloque nuevo si es tiempo."""
        if tiempo_actual - self.tiempo_ultimo_bloque > self.cfg.freq_bloque:
            x = random.randint(self.cfg.objeto_radio, self.cfg.ancho - self.cfg.objeto_radio)
            bloque = Objeto(
                x=x,
                y=-self.cfg.objeto_radio,
                tipo=TipoObjeto.BLOQUE,
                radio=self.cfg.objeto_radio,
                color=self.cfg.color_bloque,
                velocidad=self.vel_bloque,
            )
            self.objetos.append(bloque)
            self.tiempo_ultimo_bloque = tiempo_actual

    def _crear_enemigo(self, tiempo_actual: int) -> None:
        """Crea un enemigo nuevo si es tiempo."""
        if tiempo_actual - self.tiempo_ultimo_enemigo > self.cfg.freq_enemigo:
            x = random.randint(self.cfg.objeto_radio, self.cfg.ancho - self.cfg.objeto_radio)
            enemigo = Objeto(
                x=x,
                y=-self.cfg.objeto_radio,
                tipo=TipoObjeto.ENEMIGO,
                radio=self.cfg.objeto_radio,
                color=self.cfg.color_enemigo,
                velocidad=self.vel_enemigo,
            )
            self.objetos.append(enemigo)
            self.tiempo_ultimo_enemigo = tiempo_actual

    def mover_jugador(self, dx: int) -> None:
        """Mueve el jugador dentro de los límites del tablero."""
        if not self.juego_activo:
            return
        self.jugador_x = max(0, min(self.jugador_x + dx, self.cfg.ancho - self.cfg.paddle_ancho))

    def actualizar(self, tiempo_actual: int) -> None:
        """
        Actualiza la lógica del juego: objetos, colisiones, puntuación.
        """
        if not self.juego_activo:
            return

        # Crear nuevos objetos
        self._crear_bloque(tiempo_actual)
        self._crear_enemigo(tiempo_actual)

        # Mover objetos y detectar colisiones
        objetos_a_eliminar = []
        jugador_rect = pygame.Rect(self.jugador_x, self.cfg.alto - 40, self.cfg.paddle_ancho, self.cfg.paddle_alto)

        for i, obj in enumerate(self.objetos):
            obj.y += obj.velocidad

            # Colisión con jugador
            obj_rect = pygame.Rect(obj.x - obj.radio, int(obj.y - obj.radio), obj.radio * 2, obj.radio * 2)
            if jugador_rect.colliderect(obj_rect):
                if obj.tipo == TipoObjeto.BLOQUE:
                    self.puntaje += 10
                    self.vel_bloque += self.cfg.bloque_vel_inc
                    objetos_a_eliminar.append(i)
                elif obj.tipo == TipoObjeto.ENEMIGO:
                    self.vidas -= 1
                    objetos_a_eliminar.append(i)
                    if self.vidas <= 0:
                        self.juego_activo = False
            # Objeto cae sin ser tocado
            elif obj.y > self.cfg.alto:
                if obj.tipo == TipoObjeto.BLOQUE:
                    self.vidas -= 1
                    if self.vidas <= 0:
                        self.juego_activo = False
                elif obj.tipo == TipoObjeto.ENEMIGO:
                    self.puntaje += 5  # Bonus por evitar enemigo
                    self.vel_enemigo += self.cfg.enemigo_vel_inc
                objetos_a_eliminar.append(i)

        # Eliminar objetos fuera de pantalla o colisionados
        for i in sorted(objetos_a_eliminar, reverse=True):
            del self.objetos[i]

    def obtener_estado(self) -> Tuple[int, int, bool]:
        """Devuelve puntaje, vidas y si el juego está activo."""
        return self.puntaje, self.vidas, self.juego_activo
