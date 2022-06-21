from curses import KEY_ENTER
import pygame, sys
from pygame.locals import *
from random import randint
from time import time
import json, os 

# Clases
from clases import jugador
from clases import asteroide

# Variables
ANCHO = 480;
ALTO = 700;
listaAsteroide = []
puntos = 0;
colorFuente = (120,200,40);
colorSeleccion = (232,227,16);

# Comprueba si estamos jugando
jugando = True;

# Carga asteroides
def cargarAsteroides(x,y):
    meteoro = asteroide.Asteroide(x,y);
    listaAsteroide.append(meteoro);


def gameOver():
    global jugando;
    jugando = False;

# Reinicia los puntos del jugador
def reiniciar():
    global jugando;
    jugando = True;
    global puntos;
    puntos = 0;

def pausa():
    global running;
    paused = True;
    while paused:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                paused = False;
                pygame.quit();
                sys.exit;
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    paused = False;
            elif evento.type == pygame.JOYBUTTONDOWN:
                if evento.button == button_keys['options']:
                    paused = False;

# Funcion principal
def Meteoritos():
    global button_keys;
    pygame.init();
    ventana = pygame.display.set_mode((ANCHO, ALTO));

    # imagen de fondo
    fondo = pygame.image.load("img/fondo.png");
    
    # titulo
    pygame.display.set_caption("Meteoritos");

    # Objeto jugador -> Instancia de la nave
    nave = jugador.Nave();

    # Contador para medir cada cuando debe salir un asteroide
    contador = 0;

    # Audio
    pygame.mixer.music.load("audio/fondo.wav");
    pygame.mixer.music.play(3);

    # Sonido colision
    sonidoColision = pygame.mixer.Sound("audio/colision.aiff");

    # Fuente marcador
    fuenteMarcador = pygame.font.SysFont("Arial", 20);

    # Boton y fuente para reiniciar el juego
    fuentePlay = pygame.font.SysFont("Arial", 30);
    botonPlay = Rect(167,400,150,50);

    ########## Incorporacion de control análogo ##############

    joysticks = [];
    for i in range(pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i));
    for joystick in joysticks:
        joystick.init();

    with open(os.path.join("ps4_keys.json"), 'r+') as file:
        button_keys = json.load(file)

    analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5:-1}

    ##########################################################

    # ciclo del juego
    while True:
        ventana.blit(fondo,(0,0));
        nave.dibujar(ventana);

        # Tiempo
        tiempo = time();
        
        # Marcador
        global puntos;
        textoMarcador = fuenteMarcador.render("Puntos: "+str(puntos), True, colorFuente);
        ventana.blit(textoMarcador, (10,10));

        # Creamos asteroides
        # Cada segundo se crea un asteroide que se coloca al azar
        # En la posición de las X (Horizontal)
        if tiempo - contador > 1:
            contador = tiempo;
            posX = randint(2, 478);
            cargarAsteroides(posX, 0);
        
        # Comprobamos lista Asteroides
        if len(listaAsteroide) > 0:
            for x in listaAsteroide:
                if jugando == True:
                    # Se pinta y se recorre el asteroide
                    x.dibujar(ventana);
                    x.recorrido();
                if x.rect.top > 700: # Cuando el asteroide rebasa la pantalla
                                    # Se elimina
                    listaAsteroide.remove(x);
                
                # Colisiones (Asteroide contra la nave)
                else: # El jugador pierde
                    if x.rect.colliderect(nave.rect):
                        listaAsteroide.remove(x); # Desaparece el asteroide que genero la colisión
                        sonidoColision.play();
                        nave.vida = False;
                        gameOver();

        # Disparo de proyectil
        if len(nave.listaDisparo) > 0:
            for x in nave.listaDisparo: # Dibujo y recorrido del disparo
                x.dibujar(ventana);
                x.recorrido();
                if x.rect.top < -10: # Cuando el disparo rebasa el recorrido 
                    nave.listaDisparo.remove(x);

                # Colisiones (Disparo contra asteroide)
                else:
                    for meteorito in listaAsteroide:
                        if x.rect.colliderect(meteorito.rect):
                            listaAsteroide.remove(meteorito); # Elimina el asteroide que impacto con el disparo
                            nave.listaDisparo.remove(x); # Elimina el disparo que impacto con el asteroide
                            puntos += 1; # Agrega un punto
        
        nave.mover(); # Permite el movimiento de la nave

        """ Eventos """

        # Los eventos de presionar y soltar una tecla en dirección derecha e izquierda
        # permiten el movimiento fluido del juego

        for evento in pygame.event.get():
            if evento.type == QUIT: # Evento de salida
                pygame.quit();
                sys.exit();
            elif evento.type == pygame.KEYDOWN: # Al presionar una tecla
                if jugando == True:
                    if evento.key == K_LEFT:
                        nave.movimiento_izquierda = True;
                    elif evento.key == K_RIGHT:
                        nave.movimiento_derecha = True;
                    elif evento.key == K_SPACE:
                        x, y = nave.rect.center; # Obtiene las coordenadas de la nave
                        nave.disparo(x, y); # Reproduce el disparo en las coordenadas de la nave
                    elif evento.key == K_RETURN:
                        pausa();
            elif evento.type == pygame.KEYUP: # Al soltar una tecla
                if jugando == True:
                    if evento.key == K_LEFT:
                        nave.movimiento_izquierda = False;
                    elif evento.key == K_RIGHT:
                        nave.movimiento_derecha = False;
            # Si se presiona el mouse, si se da click izquierdo
            elif evento.type == MOUSEBUTTONDOWN and evento.button==1:
                if botonPlay.collidepoint(pygame.mouse.get_pos()): # Si se dio click dentro del boton de reiniciar
                    pygame.mixer.music.play(3); # Vuelve a reproducir la música de fondo
                    tiempo = time(); # Vuelve a activar el tiempo
                    reiniciar(); # Reinicia los puntos 
                    del nave; # Elimina el objeto nave
                    nave = jugador.Nave(); # Vuelve a instaciar el objeto nave con sus valores inciales
        
        ############### Eventos del control análogo ########################

        # * La nave solo se mueve en horizontal
        
        # Eventos de presionar la cruceta
            elif evento.type == pygame.JOYBUTTONDOWN:
                if evento.button == button_keys['left_arrow']:
                    nave.movimiento_izquierda = True;
                elif evento.button == button_keys['right_arrow']:
                    nave.movimiento_derecha = True;
                elif evento.button == button_keys['options']:
                    # Configurar evento para dar pausa
                    pausa();
                elif evento.button == button_keys['x']: # Evento de disparo
                    x, y = nave.rect.center; # Obtiene las coordenadas de la nave
                    nave.disparo(x, y); # Reproduce el disparo en las coordenadas de la nave
        # Eventos de soltar la cruceta
            elif evento.type == pygame.JOYBUTTONUP:
                if evento.button == button_keys['left_arrow']:
                    nave.movimiento_izquierda = False;
                elif evento.button == button_keys['right_arrow']:
                    nave.movimiento_derecha = False;

        # Eventos de joystick analogo izquiero y gatillo derecho
            elif evento.type == pygame.JOYAXISMOTION:
                analog_keys[evento.axis] = evento.value;

                if abs(analog_keys[0]) > 0.4:
                    if analog_keys[0] < -0.7:
                        nave.movimiento_izquierda = True;
                    else:
                        nave.movimiento_izquierda = False;
                    if analog_keys[0] > 0.7:
                        nave.movimiento_derecha = True;
                    else:
                        nave.movimiento_derecha = False;

                if analog_keys[5] == 1: # Gatillo derecho -> Disparo
                    x, y = nave.rect.center; # Obtiene las coordenadas de la nave
                    nave.disparo(x, y); # Reproduce el disparo en las coordenadas de la nave
                    analog_keys[5] = -1;

        ####################################################################
        
        # Cuando el jugador pierde
        if jugando == False:
            FuenteGameOver = pygame.font.SysFont("Arial", 40);
            textoGameOver = FuenteGameOver.render("Game Over", True, colorFuente);
            ventana.blit(textoGameOver, (140, 350));
            pygame.mixer.music.fadeout(3000);
            tiempo = 0; # Detiene el tiempo

            # Elimina todos los asteroides creados hasta el momento
            for asteroide in listaAsteroide:
                listaAsteroide.remove(asteroide);

            # Boton para reiniciar juego
            textoPlay = fuentePlay.render("Play", True, (255,255,255));
            
            # Cuando el mouse esta dentro de la region del boton
            if botonPlay.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(ventana,colorSeleccion,botonPlay, 0, 5);
            else:
                pygame.draw.rect(ventana,colorFuente,botonPlay, 0, 5);
            
            ventana.blit(textoPlay, (botonPlay.x+(botonPlay.width-textoPlay.get_width())/2,
                                        botonPlay.y+(botonPlay.height-textoPlay.get_height())/2));

        pygame.display.update(); # Actualización de la pantalla

# Llamada a la función principal -> Ejecución del juego
Meteoritos();