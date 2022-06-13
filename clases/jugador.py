import pygame
from clases import disparo

class Nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self);
        self.imagenNave = pygame.image.load('img/nave.png');
        self.imagenExplota = pygame.image.load('img/naveExplota.png');

        # Rectangulo de la imagen
        self.rect = self.imagenNave.get_rect();

        # Posicion inicial 
        self.rect.centerx = 240;
        self.rect.centery = 690;
        self.velocidad = 2;
        self.vida = True;
        self.listaDisparo = [];
        self.sonidoDisparo = pygame.mixer.Sound("audio/disparo.aiff");

        # Movimiento
        self.movimiento_izquierda = False;
        self.movimiento_derecha = False;
    
    # Permite que el movimiento de la nave pueda ser fluido
    def movimiento(self):
        if self.movimiento_izquierda:
            self.rect.left -= self.velocidad;
        elif self.movimiento_derecha:
            self.rect.right+= self.velocidad;

    # Restringe los limites de movimiento y permite que la nave se mueva dentro 
    # de los limites
    def mover(self):
        if self.vida == True:
            if self.rect.left <= 0: # Limite izquierdo
                self.rect.left = 0;
            elif self.rect.right > 490: # Limite derecho
                self.rect.right = 490;
        self.movimiento();
    
    # Disparo de la nave
    def disparo(self, x, y): 
        if self.vida == True:
            misil = disparo.Misil(x,y);
            self.listaDisparo.append(misil);
            self.sonidoDisparo.play();
    
    # Representacion de la imagen
    def dibujar(self, superficie):
        if self.vida == True: # Nave normal
            superficie.blit(self.imagenNave, self.rect); 
        else: # Nave cuando muere
            superficie.blit(self.imagenExplota, self.rect);


