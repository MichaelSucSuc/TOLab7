# juego_singleton.py

import pygame
import sys
import random
from datetime import datetime
import threading

# ============================================================================
# SINGLETON: ControlJuego
# ============================================================================

class ControlJuego:
    """
    Clase Singleton que maneja el estado global del juego.
    """
    
    _instancia = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instancia is None:
            with cls._lock:
                if cls._instancia is None:
                    cls._instancia = super().__new__(cls)
                    cls._instancia._inicializar()
        return cls._instancia
    
    def _inicializar(self):
        """Inicializa el estado del juego"""
        self.nivel = 1
        self.puntaje = 0
        self.vidas = 3
        self.juego_activo = True
        self.enemigos_eliminados = 0
        self.tiempo_inicio = datetime.now()
        self.color_fondo = (30, 30, 50)
        self.ultimo_evento = ""
    
    def incrementar_puntaje(self, puntos):
        """Aumenta el puntaje"""
        with self._lock:
            self.puntaje += puntos
            self.ultimo_evento = f"+{puntos} puntos!"
    
    def perder_vida(self):
        """Reduce una vida"""
        with self._lock:
            if self.vidas > 0:
                self.vidas -= 1
                self.ultimo_evento = "¡Perdiste una vida!"
                if self.vidas == 0:
                    self.game_over()
                return True
            return False
    
    def ganar_vida(self):
        """Aumenta una vida"""
        with self._lock:
            self.vidas += 1
            self.ultimo_evento = "¡Vida extra!"
    
    def eliminar_enemigo(self):
        """Registra enemigo eliminado"""
        with self._lock:
            self.enemigos_eliminados += 1
            if self.enemigos_eliminados % 5 == 0:
                self.subir_nivel()
    
    def subir_nivel(self):
        """Sube de nivel"""
        with self._lock:
            self.nivel += 1
            self.ultimo_evento = f"¡Nivel {self.nivel}!"
            # Cambiar color de fondo según nivel
            colores = [(30, 30, 50), (40, 20, 40), (20, 40, 30), 
                      (50, 30, 20), (30, 20, 50)]
            self.color_fondo = colores[self.nivel % len(colores)]
    
    def game_over(self):
        """Termina el juego"""
        with self._lock:
            self.juego_activo = False
            self.ultimo_evento = "¡GAME OVER!"
    
    def reiniciar(self):
        """Reinicia el juego"""
        with self._lock:
            self._inicializar()
    
    def get_tiempo_juego(self):
        """Obtiene tiempo transcurrido"""
        return (datetime.now() - self.tiempo_inicio).seconds

# ============================================================================
# CLASES DEL JUEGO (PyGame)
# ============================================================================

class Jugador:
    def __init__(self):
        self.control = ControlJuego()
        self.x = 400
        self.y = 500
        self.ancho = 50
        self.alto = 30
        self.velocidad = 5
        self.color = (0, 200, 255)
        self.disparos = []
    
    def mover(self, direccion):
        """Mueve al jugador"""
        if direccion == "izquierda" and self.x > 0:
            self.x -= self.velocidad
        elif direccion == "derecha" and self.x < 800 - self.ancho:
            self.x += self.velocidad
    
    def disparar(self):
        """Crea un nuevo disparo"""
        if self.control.juego_activo:
            self.disparos.append(Disparo(self.x + self.ancho//2, self.y))
    
    def dibujar(self, pantalla):
        """Dibuja al jugador"""
        pygame.draw.rect(pantalla, self.color, 
                        (self.x, self.y, self.ancho, self.alto))
        # Triángulo para la nave
        puntos = [(self.x + self.ancho//2, self.y - 10),
                 (self.x + 10, self.y + 10),
                 (self.x + self.ancho - 10, self.y + 10)]
        pygame.draw.polygon(pantalla, (100, 255, 100), puntos)
    
    def actualizar_disparos(self, enemigos):
        """Actualiza los disparos y verifica colisiones"""
        nuevos_disparos = []
        for disparo in self.disparos:
            disparo.mover()
            if disparo.y > 0:
                # Verificar colisión con enemigos
                colision = False
                for enemigo in enemigos[:]:
                    if disparo.colisiona_con(enemigo):
                        enemigos.remove(enemigo)
                        self.control.incrementar_puntaje(100)
                        self.control.eliminar_enemigo()
                        colision = True
                        break
                
                if not colision:
                    nuevos_disparos.append(disparo)
                else:
                    disparo.explotar()
            
        self.disparos = nuevos_disparos
    
    def dibujar_disparos(self, pantalla):
        """Dibuja todos los disparos"""
        for disparo in self.disparos:
            disparo.dibujar(pantalla)


class Disparo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radio = 4
        self.velocidad = 7
        self.color = (255, 255, 0)
        self.explotando = False
        self.explosion_tiempo = 0
    
    def mover(self):
        """Mueve el disparo hacia arriba"""
        if not self.explotando:
            self.y -= self.velocidad
    
    def colisiona_con(self, enemigo):
        """Verifica colisión con un enemigo"""
        distancia = ((self.x - enemigo.x)**2 + (self.y - enemigo.y)**2)**0.5
        return distancia < (self.radio + enemigo.radio)
    
    def explotar(self):
        """Inicia animación de explosión"""
        self.explotando = True
        self.explosion_tiempo = pygame.time.get_ticks()
        self.color = (255, 100, 0)
        self.radio = 10
    
    def dibujar(self, pantalla):
        """Dibuja el disparo o explosión"""
        if self.explotando:
            pygame.draw.circle(pantalla, self.color, 
                             (int(self.x), int(self.y)), self.radio)
            # La explosión desaparece después de 200ms
            if pygame.time.get_ticks() - self.explosion_tiempo > 200:
                return False
            return True
        else:
            pygame.draw.circle(pantalla, self.color, 
                             (int(self.x), int(self.y)), self.radio)
            return True


class Enemigo:
    def __init__(self, nivel):
        self.control = ControlJuego()
        self.radio = 20
        self.x = random.randint(self.radio, 800 - self.radio)
        self.y = random.randint(-100, -40)
        self.velocidad_y = random.uniform(0.5, 1.5) + nivel * 0.1
        self.velocidad_x = random.uniform(-0.5, 0.5)
        self.color = (random.randint(150, 255), 
                     random.randint(50, 150), 
                     random.randint(50, 150))
        self.tiempo_aparicion = pygame.time.get_ticks()
    
    def mover(self):
        """Mueve al enemigo"""
        self.y += self.velocidad_y
        self.x += self.velocidad_x
        
        # Rebote en bordes laterales
        if self.x < self.radio or self.x > 800 - self.radio:
            self.velocidad_x *= -1
    
    def dibujar(self, pantalla):
        """Dibuja al enemigo"""
        pygame.draw.circle(pantalla, self.color, 
                         (int(self.x), int(self.y)), self.radio)
        # Ojos del enemigo
        pygame.draw.circle(pantalla, (255, 255, 255), 
                         (int(self.x - 6), int(self.y - 5)), 4)
        pygame.draw.circle(pantalla, (255, 255, 255), 
                         (int(self.x + 6), int(self.y - 5)), 4)
        pygame.draw.circle(pantalla, (0, 0, 0), 
                         (int(self.x - 6), int(self.y - 5)), 2)
        pygame.draw.circle(pantalla, (0, 0, 0), 
                         (int(self.x + 6), int(self.y - 5)), 2)
    
    def colisiona_con_jugador(self, jugador):
        """Verifica colisión con el jugador"""
        distancia = ((self.x - (jugador.x + jugador.ancho/2))**2 + 
                    (self.y - (jugador.y + jugador.alto/2))**2)**0.5
        return distancia < (self.radio + max(jugador.ancho, jugador.alto)/2)

# ============================================================================
# INTERFAZ GRÁFICA
# ============================================================================

class InterfazJuego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Juego Singleton - ControlJuego")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont(None, 28)
        self.fuente_grande = pygame.font.SysFont(None, 48)
        
        self.jugador = Jugador()
        self.enemigos = []
        self.control = ControlJuego()
        
        # Temporizadores
        self.tiempo_ultimo_enemigo = 0
        self.tiempo_ultima_vida = 0
    
    def crear_enemigos(self):
        """Crea nuevos enemigos periódicamente"""
        tiempo_actual = pygame.time.get_ticks()
        
        # Crear enemigos cada 1-2 segundos
        if (tiempo_actual - self.tiempo_ultimo_enemigo > 
            1000 - min(self.control.nivel * 100, 800)):
            self.enemigos.append(Enemigo(self.control.nivel))
            self.tiempo_ultimo_enemigo = tiempo_actual
        
        # Crear vida extra cada 15 segundos
        if (tiempo_actual - self.tiempo_ultima_vida > 15000 and 
            self.control.vidas < 5):
            self.crear_vida_extra()
            self.tiempo_ultima_vida = tiempo_actual
    
    def crear_vida_extra(self):
        """Crea una vida extra especial"""
        vida = Enemigo(self.control.nivel)
        vida.color = (0, 255, 0)  # Verde para vida extra
        vida.radio = 15
        vida.velocidad_y = 0.8
        self.enemigos.append(vida)
    
    def dibujar_ui(self):
        """Dibuja la interfaz de usuario"""
        pantalla = self.pantalla
        
        # Panel superior
        pygame.draw.rect(pantalla, (40, 40, 60), (0, 0, 800, 40))
        
        # Información del juego
        textos = [
            f"Nivel: {self.control.nivel}",
            f"Puntaje: {self.control.puntaje}",
            f"Vidas: {self.control.vidas}",
            f"Eliminados: {self.control.enemigos_eliminados}",
            f"Tiempo: {self.control.get_tiempo_juego()}s"
        ]
        
        for i, texto in enumerate(textos):
            texto_surf = self.fuente.render(texto, True, (255, 255, 255))
            pantalla.blit(texto_surf, (20 + i * 150, 10))
        
        # Último evento
        if self.control.ultimo_evento:
            evento_surf = self.fuente.render(
                self.control.ultimo_evento, True, (255, 255, 100))
            pantalla.blit(evento_surf, (300, 550))
        
        # Instrucciones
        instrucciones = [
            "Flechas: Mover | ESPACIO: Disparar | R: Reiniciar | ESC: Salir",
            "Objetivo: Eliminar enemigos (rojos). Vida extra (verde) = +1 vida"
        ]
        
        for i, instr in enumerate(instrucciones):
            instr_surf = self.fuente.render(instr, True, (200, 200, 200))
            pantalla.blit(instr_surf, (10, 570 + i * 20))
    
    def dibujar_game_over(self):
        """Dibuja pantalla de Game Over"""
        pantalla = self.pantalla
        
        # Fondo semitransparente
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        pantalla.blit(overlay, (0, 0))
        
        # Texto Game Over
        go_text = self.fuente_grande.render("GAME OVER", True, (255, 50, 50))
        pantalla.blit(go_text, (800//2 - go_text.get_width()//2, 200))
        
        # Puntaje final
        score_text = self.fuente.render(
            f"Puntaje Final: {self.control.puntaje}", True, (255, 255, 255))
        pantalla.blit(score_text, (800//2 - score_text.get_width()//2, 280))
        
        # Instrucciones
        reinicio_text = self.fuente.render(
            "Presiona R para reiniciar o ESC para salir", True, (200, 200, 200))
        pantalla.blit(reinicio_text, 
                     (800//2 - reinicio_text.get_width()//2, 350))
    
    def reiniciar_juego(self):
        """Reinicia completamente el juego"""
        self.control.reiniciar()
        self.jugador = Jugador()
        self.enemigos = []
        self.tiempo_ultimo_enemigo = pygame.time.get_ticks()
        self.tiempo_ultima_vida = pygame.time.get_ticks()
    
    def ejecutar(self):
        """Bucle principal del juego"""
        ejecutando = True
        
        while ejecutando:
            # Manejo de eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        ejecutando = False
                    elif evento.key == pygame.K_r:
                        self.reiniciar_juego()
                    elif evento.key == pygame.K_SPACE and self.control.juego_activo:
                        self.jugador.disparar()
            
            # Controles continuos
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT]:
                self.jugador.mover("izquierda")
            if teclas[pygame.K_RIGHT]:
                self.jugador.mover("derecha")
            
            # Crear enemigos
            if self.control.juego_activo:
                self.crear_enemigos()
            
            # Actualizar enemigos
            for enemigo in self.enemigos[:]:
                enemigo.mover()
                
                # Verificar si el enemigo llegó al fondo
                if enemigo.y > 600:
                    self.enemigos.remove(enemigo)
                    if enemigo.color != (0, 255, 0):  # No es vida extra
                        self.control.perder_vida()
                
                # Verificar colisión con jugador
                elif enemigo.colisiona_con_jugador(self.jugador):
                    self.enemigos.remove(enemigo)
                    if enemigo.color == (0, 255, 0):  # Es vida extra
                        self.control.ganar_vida()
                    else:
                        self.control.perder_vida()
            
            # Actualizar disparos
            self.jugador.actualizar_disparos(self.enemigos)
            
            # Dibujar
            self.pantalla.fill(self.control.color_fondo)
            
            # Dibujar elementos del juego
            for enemigo in self.enemigos:
                enemigo.dibujar(self.pantalla)
            
            self.jugador.dibujar(self.pantalla)
            self.jugador.dibujar_disparos(self.pantalla)
            
            # Dibujar UI
            self.dibujar_ui()
            
            # Dibujar Game Over si es necesario
            if not self.control.juego_activo:
                self.dibujar_game_over()
            
            pygame.display.flip()
            self.reloj.tick(60)
        
        pygame.quit()
        sys.exit()

# ============================================================================
# DEMOSTRACIÓN DEL SINGLETON
# ============================================================================

def demostrar_singleton():
    """Función que demuestra que ControlJuego es un Singleton"""
    print("="*60)
    print("DEMOSTRACIÓN DEL PATRÓN SINGLETON")
    print("="*60)
    
    # Crear múltiples referencias
    control1 = ControlJuego()
    control2 = ControlJuego()
    
    print(f"control1 id: {id(control1)}")
    print(f"control2 id: {id(control2)}")
    print(f"¿Son la misma instancia? {control1 is control2}")
    
    # Modificar desde una referencia
    control1.incrementar_puntaje(100)
    print(f"\nPuntaje desde control1: {control1.puntaje}")
    print(f"Puntaje desde control2: {control2.puntaje}")
    print("(Ambas referencias muestran el mismo valor)")
    
    print("\nIniciando juego...")
    print("="*60)

# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    # Mostrar demostración del Singleton
    demostrar_singleton()
    
    # Iniciar el juego
    juego = InterfazJuego()
    juego.ejecutar()