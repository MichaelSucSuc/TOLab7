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


# ============================================================================
# Configuracion y constantes
# ============================================================================


@dataclass(frozen=True)
class Ajustes:
    ancho: int = 640
    alto: int = 480
    tam_celda: int = 20
    color_fondo: Tuple[int, int, int] = (12, 16, 24)
    color_cuadricula: Tuple[int, int, int] = (24, 32, 44)
    color_serpiente: Tuple[int, int, int] = (80, 200, 120)
    color_cabeza: Tuple[int, int, int] = (120, 220, 160)
    color_comida: Tuple[int, int, int] = (230, 80, 70)
    color_texto: Tuple[int, int, int] = (235, 235, 235)
    color_sombra: Tuple[int, int, int] = (0, 0, 0)
    fps_base: float = 8.0
    fps_incremento: float = 0.35


# ============================================================================
# Singleton que controla el estado del juego
# ============================================================================


class ControlJuego(metaclass=SingletonMeta):
    """Gestiona todo el estado de la serpiente y la partida."""

    def __init__(self) -> None:
        if getattr(self, "_inicializado", False):
            return

        self._inicializado = True
        self.conf = Ajustes()
        self.columnas = self.conf.ancho // self.conf.tam_celda
        self.filas = self.conf.alto // self.conf.tam_celda
        self.record = 0
        self.reiniciar()

    def reiniciar(self) -> None:
        """Coloca a la serpiente en el centro y reinicia la partida."""
        centro_x = self.columnas // 2
        centro_y = self.filas // 2
        self.serpiente: List[Tuple[int, int]] = [
            (centro_x, centro_y),
            (centro_x - 1, centro_y),
            (centro_x - 2, centro_y),
        ]
        self._direccion_actual: Tuple[int, int] = (1, 0)
        self._direccion_pendiente: Tuple[int, int] = (1, 0)
        self.pausado = False
        self.estado = "jugando"  # jugando | gameover
        self.puntaje = 0
        self.comida = self._generar_comida()

    def _generar_comida(self) -> Tuple[int, int]:
        """Devuelve una celda libre al azar para la comida."""
        libres = [
            (x, y)
            for x in range(self.columnas)
            for y in range(self.filas)
            if (x, y) not in self.serpiente
        ]
        return random.choice(libres) if libres else self.serpiente[0]

    def cambiar_direccion(self, nueva: Tuple[int, int]) -> None:
        """Cambia la direccion si no es opuesta a la actual."""
        if self.estado != "jugando":
            return

        opuesta = (-self._direccion_actual[0], -self._direccion_actual[1])
        if nueva != opuesta and nueva != self._direccion_actual:
            self._direccion_pendiente = nueva

    def alternar_pausa(self) -> None:
        """Activa o desactiva la pausa."""
        if self.estado == "jugando":
            self.pausado = not self.pausado

    def actualizar(self) -> None:
        """Avanza un paso la serpiente si el juego esta activo."""
        if self.estado != "jugando" or self.pausado:
            return

        self._direccion_actual = self._direccion_pendiente
        dx, dy = self._direccion_actual
        cabeza_x, cabeza_y = self.serpiente[0]
        nueva_cabeza = (cabeza_x + dx, cabeza_y + dy)

        # Verifica limites y colision propia.
        fuera_tablero = not (0 <= nueva_cabeza[0] < self.columnas and 0 <= nueva_cabeza[1] < self.filas)
        if fuera_tablero or nueva_cabeza in self.serpiente:
            self.estado = "gameover"
            return

        self.serpiente.insert(0, nueva_cabeza)
        if nueva_cabeza == self.comida:
            self.puntaje += 10
            self.record = max(self.record, self.puntaje)
            self.comida = self._generar_comida()
        else:
            self.serpiente.pop()

    def velocidad_actual(self) -> float:
        """Calcula los FPS en funcion del largo de la serpiente."""
        crecimiento = max(0, len(self.serpiente) - 3)
        return self.conf.fps_base + crecimiento * self.conf.fps_incremento

    def datos_ui(self) -> Tuple[int, int, float, str]:
        """Datos listos para renderizar."""
        estado = "EN PAUSA" if self.pausado else ("GAME OVER" if self.estado != "jugando" else "JUGANDO")
        return self.puntaje, self.record, self.velocidad_actual(), estado


# ============================================================================
# Interfaz grafica con pygame
# ============================================================================


class InterfazSnake:
    def __init__(self) -> None:
        pygame.init()
        self.control = ControlJuego()
        self.pantalla = pygame.display.set_mode((self.control.conf.ancho, self.control.conf.alto))
        pygame.display.set_caption("Snake - Singleton")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("consolas", 22)
        self.fuente_grande = pygame.font.SysFont("consolas", 36, bold=True)

    def _manejar_eventos(self) -> bool:
        """Procesa eventos y devuelve False si se debe cerrar."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                if evento.key == pygame.K_r:
                    self.control.reiniciar()
                if evento.key == pygame.K_SPACE:
                    self.control.alternar_pausa()
                if evento.key == pygame.K_UP:
                    self.control.cambiar_direccion((0, -1))
                if evento.key == pygame.K_DOWN:
                    self.control.cambiar_direccion((0, 1))
                if evento.key == pygame.K_LEFT:
                    self.control.cambiar_direccion((-1, 0))
                if evento.key == pygame.K_RIGHT:
                    self.control.cambiar_direccion((1, 0))
        return True

    def _dibujar_cuadricula(self) -> None:
        tam = self.control.conf.tam_celda
        for x in range(0, self.control.conf.ancho, tam):
            pygame.draw.line(self.pantalla, self.control.conf.color_cuadricula, (x, 0), (x, self.control.conf.alto))
        for y in range(0, self.control.conf.alto, tam):
            pygame.draw.line(self.pantalla, self.control.conf.color_cuadricula, (0, y), (self.control.conf.ancho, y))

    def _dibujar_serpiente(self) -> None:
        tam = self.control.conf.tam_celda
        for idx, (x, y) in enumerate(self.control.serpiente):
            color = self.control.conf.color_cabeza if idx == 0 else self.control.conf.color_serpiente
            rect = pygame.Rect(x * tam + 1, y * tam + 1, tam - 2, tam - 2)
            pygame.draw.rect(self.pantalla, color, rect, border_radius=4)

    def _dibujar_comida(self) -> None:
        tam = self.control.conf.tam_celda
        x, y = self.control.comida
        rect = pygame.Rect(x * tam + 2, y * tam + 2, tam - 4, tam - 4)
        pygame.draw.rect(self.pantalla, self.control.conf.color_comida, rect, border_radius=3)

    def _dibujar_texto(self, texto: str, pos: Tuple[int, int], grande: bool = False) -> None:
        fuente = self.fuente_grande if grande else self.fuente
        sombra = fuente.render(texto, True, self.control.conf.color_sombra)
        self.pantalla.blit(sombra, (pos[0] + 2, pos[1] + 2))
        superficie = fuente.render(texto, True, self.control.conf.color_texto)
        self.pantalla.blit(superficie, pos)

    def _dibujar_ui(self) -> None:
        puntaje, record, velocidad, estado = self.control.datos_ui()
        self._dibujar_texto(f"Puntaje: {puntaje}", (10, 10))
        self._dibujar_texto(f"Record: {record}", (10, 36))
        self._dibujar_texto(f"Velocidad: {velocidad:.1f} fps", (10, 62))
        self._dibujar_texto(f"Estado: {estado}", (10, 88))
        self._dibujar_texto("Flechas: mover | R: reiniciar | ESPACIO: pausa | ESC: salir", (10, self.control.conf.alto - 26))

    def _dibujar_overlays(self) -> None:
        if self.control.estado != "jugando":
            overlay = pygame.Surface((self.control.conf.ancho, self.control.conf.alto), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            self.pantalla.blit(overlay, (0, 0))
            self._dibujar_texto("GAME OVER", (self.control.conf.ancho // 2 - 100, self.control.conf.alto // 2 - 40), grande=True)
            self._dibujar_texto("Presiona R para intentarlo de nuevo", (self.control.conf.ancho // 2 - 190, self.control.conf.alto // 2))
        elif self.control.pausado:
            overlay = pygame.Surface((self.control.conf.ancho, self.control.conf.alto), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            self.pantalla.blit(overlay, (0, 0))
            self._dibujar_texto("Pausa", (self.control.conf.ancho // 2 - 40, self.control.conf.alto // 2 - 20), grande=True)

    def dibujar(self) -> None:
        self.pantalla.fill(self.control.conf.color_fondo)
        self._dibujar_cuadricula()
        self._dibujar_comida()
        self._dibujar_serpiente()
        self._dibujar_ui()
        self._dibujar_overlays()
        pygame.display.flip()

    def ejecutar(self) -> None:
        """Bucle principal del juego."""
        corriendo = True
        while corriendo:
            corriendo = self._manejar_eventos()
            self.control.actualizar()
            self.dibujar()
            self.reloj.tick(self.control.velocidad_actual())

        pygame.quit()
        sys.exit()

