import pygame

class Misil(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self);
        self.imagenMisil = pygame.image.load("img/misil.png"); 
        self.rect = self.imagenMisil.get_rect(); # Obtiene el área rectangular de la superficie
        
        # Variables del disparo
        self.velocidadDisparo = 10;
        self.rect.top = posY;
        self.rect.left = posX;
    
    # De abajo hacia arriba
    def recorrido(self):
        self.rect.top = self.rect.top - self.velocidadDisparo;

    # Dibuja el disparo en la superficie
    def dibujar(self, superficie):
        superficie.blit(self.imagenMisil, self.rect);


