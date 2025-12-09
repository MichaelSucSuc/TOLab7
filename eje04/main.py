"""Mini juego sencillo (atrapar bloques) con Singleton para el estado global."""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import pygame

# Agrega la carpeta raiz (..\) para importar patrones.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from patrones import SingletonMeta


# ============================================================================
# Configuracion del juego
# ============================================================================


@dataclass(frozen=True)
class Ajustes:
    ancho: int = 640
    alto: int = 480
    color_fondo: Tuple[int, int, int] = (18, 24, 32)
    color_jugador: Tuple[int, int, int] = (90, 180, 255)
    color_bloque: Tuple[int, int, int] = (255, 140, 0)
    color_texto: Tuple[int, int, int] = (235, 235, 235)
    paddle_ancho: int = 90
    paddle_alto: int = 18
    paddle_vel: int = 8
    bloque_lado: int = 26
    bloque_vel_ini: float = 3.0
    bloque_vel_inc: float = 0.15
    vidas_ini: int = 3


# ============================================================================
# Singleton que maneja el estado del juego
# ============================================================================


class ControlJuego(metaclass=SingletonMeta):
    """Estado global: puntaje, vidas, velocidad, posiciones."""

    def __init__(self) -> None:
        if getattr(self, "_init_ok", False):
            return
        self._init_ok = True
        self.cfg = Ajustes()
        self.reiniciar()

    def reiniciar(self) -> None:
        self.puntaje = 0
        self.vidas = self.cfg.vidas_ini
        self.vel_bloque = self.cfg.bloque_vel_ini
        self.juego_activo = True
        self.jugador_x = (self.cfg.ancho - self.cfg.paddle_ancho) // 2
        self.bloque_x, self.bloque_y = self._nuevo_bloque()

    def _nuevo_bloque(self) -> Tuple[int, int]:
        x = random.randint(0, self.cfg.ancho - self.cfg.bloque_lado)
        y = -self.cfg.bloque_lado
        return x, y

    def mover_jugador(self, dx: int) -> None:
        if not self.juego_activo:
            return
        self.jugador_x = max(0, min(self.jugador_x + dx, self.cfg.ancho - self.cfg.paddle_ancho))

    def actualizar(self) -> None:
        if not self.juego_activo:
            return
        self.bloque_y += self.vel_bloque
        jugador_rect = pygame.Rect(self.jugador_x, self.cfg.alto - 40, self.cfg.paddle_ancho, self.cfg.paddle_alto)
        bloque_rect = pygame.Rect(self.bloque_x, int(self.bloque_y), self.cfg.bloque_lado, self.cfg.bloque_lado)

        if jugador_rect.colliderect(bloque_rect):
            self.puntaje += 10
            self.vel_bloque += self.cfg.bloque_vel_inc
            self.bloque_x, self.bloque_y = self._nuevo_bloque()
        elif self.bloque_y > self.cfg.alto:
            self.vidas -= 1
            self.bloque_x, self.bloque_y = self._nuevo_bloque()
            if self.vidas <= 0:
                self.juego_activo = False

    def datos_ui(self) -> Tuple[int, int, bool]:
        return self.puntaje, self.vidas, self.juego_activo


# ============================================================================
# Interfaz grafica con pygame
# ============================================================================


class InterfazJuego:
    def __init__(self) -> None:
        pygame.init()
        self.control = ControlJuego()
        self.cfg = self.control.cfg
        self.pantalla = pygame.display.set_mode((self.cfg.ancho, self.cfg.alto))
        pygame.display.set_caption("Atrapa el bloque - Singleton")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("consolas", 22)
        self.fuente_grande = pygame.font.SysFont("consolas", 32, bold=True)

    def _manejar_eventos(self) -> bool:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                if evento.key == pygame.K_r:
                    self.control.reiniciar()
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.control.mover_jugador(-self.cfg.paddle_vel)
        if teclas[pygame.K_RIGHT]:
            self.control.mover_jugador(self.cfg.paddle_vel)
        return True

    def _dibujar_texto(self, texto: str, pos: Tuple[int, int], grande: bool = False) -> None:
        fuente = self.fuente_grande if grande else self.fuente
        sombra = fuente.render(texto, True, (0, 0, 0))
        self.pantalla.blit(sombra, (pos[0] + 2, pos[1] + 2))
        surf = fuente.render(texto, True, self.cfg.color_texto)
        self.pantalla.blit(surf, pos)

    def _dibujar(self) -> None:
        self.pantalla.fill(self.cfg.color_fondo)
        pygame.draw.rect(self.pantalla, self.cfg.color_jugador, (self.control.jugador_x, self.cfg.alto - 40, self.cfg.paddle_ancho, self.cfg.paddle_alto), border_radius=4)
        pygame.draw.rect(self.pantalla, self.cfg.color_bloque, (self.control.bloque_x, int(self.control.bloque_y), self.cfg.bloque_lado, self.cfg.bloque_lado), border_radius=3)

        puntaje, vidas, activo = self.control.datos_ui()
        self._dibujar_texto(f"Puntaje: {puntaje}", (12, 12))
        self._dibujar_texto(f"Vidas: {vidas}", (12, 38))
        self._dibujar_texto("Flechas mover | R reiniciar | ESC salir", (12, self.cfg.alto - 28))

        if not activo:
            overlay = pygame.Surface((self.cfg.ancho, self.cfg.alto), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            self.pantalla.blit(overlay, (0, 0))
            self._dibujar_texto("GAME OVER", (self.cfg.ancho // 2 - 90, self.cfg.alto // 2 - 40), grande=True)
            self._dibujar_texto("R para reiniciar", (self.cfg.ancho // 2 - 90, self.cfg.alto // 2), grande=False)

        pygame.display.flip()

    def ejecutar(self) -> None:
        corriendo = True
        while corriendo:
            corriendo = self._manejar_eventos()
            self.control.actualizar()
            self._dibujar()
            self.reloj.tick(60)
        pygame.quit()
        sys.exit()


# ============================================================================
# Demostracion del Singleton
# ============================================================================


def demostrar_singleton() -> None:
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

