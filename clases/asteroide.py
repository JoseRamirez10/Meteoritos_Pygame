import pygame

class Asteroide(pygame.sprite.Sprite):
    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self);
        self.imagenAsteroide = pygame.image.load("img/asteroide.png");
        
        # Rectangulo del asteroide
        self.rect = self.imagenAsteroide.get_rect();
        
        # Variables del asteroide
        self.velocidad = 2;
        self.rect.top = posY;
        self.rect.left = posX;
        self.listaAsteroides = [];

    # Recorrido del asteroide
    # De arriba hacia abajo
    def recorrido(self):
        self.rect.top = self.rect.top + self.velocidad;
        
    # Dibuja el asteroide en la superficie
    def dibujar(self, superficie):
        superficie.blit(self.imagenAsteroide, self.rect);