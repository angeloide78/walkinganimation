"""
Walking Animation, el paseo de una joven por pantalla con problemas de ansiedad

    Copyright (C) 2023 Ángel Luis García García

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import pygame

dir_actual = os.path.dirname(os.path.abspath(__file__))

FICHERO_IMAGEN = [dir_actual, "assets", "imagen", "walking_animation.png"]
BACKGROUND = [dir_actual, "assets", "imagen", "background.png"]
SONIDO_GOLPE = [dir_actual, "assets", "sonido", "golpe.wav"]
SONIDO_YEAH = [dir_actual, "assets", "sonido", "yeah.wav"]

class Animacion:
    """Paseo de una joven por pantalla"""
    
    def __init__(self):
        """Inicializa el paseo de una joven"""
  
        # Inicializamos pygame.
        pygame.init()
        pygame.mixer.init()
        
        # Carga del archivo de sonido
        a =  os.path.join(*SONIDO_GOLPE)
        
        self.__sonido_golpe = pygame.mixer.Sound(os.path.join(*SONIDO_GOLPE))
        self.__sonido_yeah = pygame.mixer.Sound(os.path.join(*SONIDO_YEAH)) 
        
        # Pantalla.
        self.__ancho = 640
        self.__alto = 480
        
        self.__pantalla = pygame.display.\
            set_mode( (self.__ancho, self.__alto), 0, 32)
        
        pygame.display.set_caption("Walking Animation")

        # Se carga la imagen.
        self.__imagen = pygame.image.\
            load(os.path.join(*FICHERO_IMAGEN)).convert_alpha()

        # Y el fondo.
        self.__background = pygame.image.\
            load(os.path.join(*BACKGROUND)).convert_alpha()
        self.__background = pygame.transform.scale(self.__background, \
                                                   (self.__ancho, self.__alto))
        
        # Creamos rectángulos a partir de la imagen.
        self.rectanculos = self.__crear_rectangulos()
        
        # Atributos de control
        self.__puntero = 0      # Controla el rectángulo (imagen) actual.
        self.__x = 320          # Posición x
        self.__y = 352          # 480 - 128, en la parte baja de la pantalla. 
        self.__sentido = True   # Sentido del paseo.    
        self.__running = False
        self.__saltando = False
        self.__subiendo = True
    
    def run(self):
        """Ejecución de la aplicación"""
        
        self.__running = True
        fps_clock = pygame.time.Clock()
        
        seguir = True
        
        while self.__running:
            
            # Se procesan los eventos.
            self.__process_events()
            
            # Controlamos la velocidad del paseo.
            if seguir:
                seguir = False
                t_i = pygame.time.get_ticks()   # Tiempo inicial.
                contador = 0                    # Milisengundos de espera.            
            
            t_a = pygame.time.get_ticks()       # Tiempo actual.
            
            contador += (t_a - t_i)
            
            if contador > 200:

                # Se actualiza.
                self.__update()
                seguir = True
            
            # Se pinta.
            self.__render()

            # 60 frames.
            fps_clock.tick(60)
            
        self.__quit()    
    
    def __update(self):
        """Actualización de la imagen"""
        
        # Se controla el salto, y el comportamiento si se sube o baja.

        if self.__saltando:
            
            if self.__y < 300:
                self.__subiendo = False
            
            if self.__subiendo: self.__y -= 5
            else: self.__y += 5

            if self.__y == 352:
                self.__saltando = False
                self.__subiendo = True
        
        # Se controla el sentido del caminar.
        
        if self.__sentido:
            
            if self.__saltando: self.__x += 1
            else: self.__x += 5
            
            self.__puntero += 1
         
            if self.__puntero > 9:
                self.__puntero = 1
        
        else:
            
            if self.__saltando: self.__x -= 1
            else: self.__x -= 5
            
            self.__puntero += 1
         
            if self.__puntero > 19:
                self.__puntero = 11
                    
        # Comprobamos si llegamos a los límites de la ventana.
            
        if self.__ancho - self.__x <= 64:
            
            self.__puntero = 10
            self.__sonido_golpe.play()
            self.__sentido = False

        if self.__x <= 0:
            
            self.__puntero = 10
            self.__sonido_golpe.play()
            self.__sentido = True
        
    def __process_events(self):
        """Procesa eventos"""
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.__running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__salto()            
    
    def __render(self):
        """Visualiza gráficos por pantalla"""
        
        # Fondo de pantalla.
        self.__pantalla.blit(self.__background, (0, 0))

        # Recortamos imagen dentro del rectángulo.
        self.__pantalla.blit(self.__imagen, \
                             (self.__x, self.__y), \
                             self.rectanculos[self.__puntero])
        
        # Se dibuja el rectángulo.
        pygame.draw.rect(self.__pantalla, (0, 0, 0, 0), \
                         (0, 0, 0, 0), 0)
        
        # Visualizamos...
        pygame.display.flip()  

    def __quit(self):
        """Salir del programa"""
        
        pygame.quit()
        
    def __salto(self):
        """Inicio del salto"""
        
        self.__sonido_yeah.play()
        self.__saltando = True
        
    def __crear_rectangulos(self):
        """Devuelve una lista con todos los rectánculos
        
        Anchura: 640 pixeles
        Altura:  256 pixeles
        """
        
        ancho = 640
        alto = 256
        nfil = 2
        ncol = 10
        
        ancho_rec = int(ancho / ncol) # Ancho de un único rectángulo.
        largo_rec = int(alto / nfil)  # Largo de un único rectángulo.
        
        ret = []
        x = y = 0
    
        for j in range(nfil):
    
            for i in range(ncol):
                ret.append(pygame.Rect([x, y, ancho_rec, largo_rec]))
                x += ancho_rec  
    
            x = 0
            y += int(alto / nfil)
    
        return ret
    
