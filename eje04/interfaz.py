"""Interfaz gráfica - módulo separado."""

from __future__ import annotations

import sys
from typing import Tuple

import pygame

from estado import ControlJuego, TipoObjeto


# ============================================================================
# Interfaz gráfica con Pygame
# ============================================================================


class InterfazJuego:
    """
    Maneja toda la presentación visual y eventos de entrada.
    Responsabilidades: render, input, no tiene lógica de juego.
    """

    def __init__(self) -> None:
        pygame.init()
        self.control = ControlJuego()
        self.cfg = self.control.cfg
        self.pantalla = pygame.display.set_mode((self.cfg.ancho, self.cfg.alto))
        pygame.display.set_caption("Atrapa Bloques Evita Enemigos - Singleton")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("consolas", 22)
        self.fuente_grande = pygame.font.SysFont("consolas", 32, bold=True)
        self.tiempo_inicio = pygame.time.get_ticks()

    def _manejar_eventos(self) -> bool:
        """Procesa eventos de entrada. Devuelve False si se debe cerrar."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                if evento.key == pygame.K_r:
                    self.control.reiniciar()
                    self.tiempo_inicio = pygame.time.get_ticks()

        # Controles continuos
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.control.mover_jugador(-self.cfg.paddle_vel)
        if teclas[pygame.K_RIGHT]:
            self.control.mover_jugador(self.cfg.paddle_vel)

        return True

    def _dibujar_texto(self, texto: str, pos: Tuple[int, int], grande: bool = False) -> None:
        """Dibuja texto con sombra en la pantalla."""
        fuente = self.fuente_grande if grande else self.fuente
        sombra = fuente.render(texto, True, (0, 0, 0))
        self.pantalla.blit(sombra, (pos[0] + 2, pos[1] + 2))
        surf = fuente.render(texto, True, self.cfg.color_texto)
        self.pantalla.blit(surf, pos)

    def _dibujar_objetos(self) -> None:
        """Dibuja todos los objetos (bloques y enemigos)."""
        for obj in self.control.objetos:
            if obj.tipo == TipoObjeto.BLOQUE:
                # Bloques: círculos naranjas con contorno blanco
                pygame.draw.circle(
                    self.pantalla,
                    obj.color,
                    (int(obj.x), int(obj.y)),
                    obj.radio,
                )
                pygame.draw.circle(
                    self.pantalla,
                    (255, 255, 255),
                    (int(obj.x), int(obj.y)),
                    obj.radio,
                    2,
                )
            else:  # ENEMIGO
                # Enemigos: caras triangulares amenazantes rojas
                radio = obj.radio
                x, y = int(obj.x), int(obj.y)
                
                # Triángulo hacia abajo (cara amenazante)
                puntos = [
                    (x, y - radio),          # arriba
                    (x - radio, y + radio),  # abajo izquierda
                    (x + radio, y + radio),  # abajo derecha
                ]
                pygame.draw.polygon(self.pantalla, obj.color, puntos)
                pygame.draw.polygon(self.pantalla, (100, 0, 0), puntos, 3)  # Contorno oscuro
                
                # Ojos
                pygame.draw.circle(self.pantalla, (255, 255, 255), (x - 5, y - 2), 3)
                pygame.draw.circle(self.pantalla, (255, 255, 255), (x + 5, y - 2), 3)
                pygame.draw.circle(self.pantalla, (0, 0, 0), (x - 5, y - 2), 2)
                pygame.draw.circle(self.pantalla, (0, 0, 0), (x + 5, y - 2), 2)

    def _dibujar_jugador(self) -> None:
        """Dibuja la barra del jugador."""
        pygame.draw.rect(
            self.pantalla,
            self.cfg.color_jugador,
            (self.control.jugador_x, self.cfg.alto - 40, self.cfg.paddle_ancho, self.cfg.paddle_alto),
            border_radius=4,
        )

    def _dibujar_ui(self) -> None:
        """Dibuja información del juego (HUD)."""
        puntaje, vidas, activo = self.control.obtener_estado()
        tiempo_transcurrido = (pygame.time.get_ticks() - self.tiempo_inicio) // 1000
        self._dibujar_texto(f"Puntaje: {puntaje}", (12, 12))
        self._dibujar_texto(f"Vidas: {vidas}", (12, 38))
        self._dibujar_texto(f"Tiempo: {tiempo_transcurrido}s", (12, 64))
        self._dibujar_texto(f"Objetos: {len(self.control.objetos)}", (self.cfg.ancho - 200, 12))
        self._dibujar_texto("Flechas mover | R reiniciar | ESC salir", (12, self.cfg.alto - 28))

    def _dibujar_overlays(self) -> None:
        """Dibuja overlays de estado (GAME OVER)."""
        puntaje, vidas, activo = self.control.obtener_estado()
        if not activo:
            overlay = pygame.Surface((self.cfg.ancho, self.cfg.alto), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            self.pantalla.blit(overlay, (0, 0))
            self._dibujar_texto("GAME OVER", (self.cfg.ancho // 2 - 110, self.cfg.alto // 2 - 40), grande=True)
            self._dibujar_texto(f"Puntaje Final: {puntaje}", (self.cfg.ancho // 2 - 130, self.cfg.alto // 2), grande=False)
            self._dibujar_texto("R para reiniciar", (self.cfg.ancho // 2 - 100, self.cfg.alto // 2 + 40), grande=False)

    def _dibujar_leyenda(self) -> None:
        """Dibuja leyenda de colores."""
        fuente_pequeña = pygame.font.SysFont("consolas", 16)
        texto_bloque = fuente_pequeña.render("Naranja: +10pts", True, self.cfg.color_bloque)
        texto_enemigo = fuente_pequeña.render("Rojo: -1vida", True, self.cfg.color_enemigo)
        self.pantalla.blit(texto_bloque, (self.cfg.ancho - 200, self.cfg.alto - 50))
        self.pantalla.blit(texto_enemigo, (self.cfg.ancho - 200, self.cfg.alto - 25))

    def dibujar(self) -> None:
        """Renderiza un frame completo."""
        self.pantalla.fill(self.cfg.color_fondo)
        self._dibujar_objetos()
        self._dibujar_jugador()
        self._dibujar_ui()
        self._dibujar_leyenda()
        self._dibujar_overlays()
        pygame.display.flip()

    def ejecutar(self) -> None:
        """Bucle principal de la interfaz."""
        corriendo = True
        while corriendo:
            corriendo = self._manejar_eventos()
            tiempo_actual = pygame.time.get_ticks()
            self.control.actualizar(tiempo_actual)
            self.dibujar()
            self.reloj.tick(60)

        pygame.quit()
        sys.exit()
