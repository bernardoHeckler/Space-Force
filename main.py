import pygame
import random
import os
from tkinter import simpledialog

pygame.init()

relogio = pygame.time.Clock()
icone = pygame.image.load("Recursos/icone.png")
nave = pygame.image.load("Recursos/nave.png")
alien = pygame.image.load("Recursos/alien.png")
fundo = pygame.image.load("Recursos/estratosferaFundoDeTela.png")
fundoStart = pygame.image.load("Recursos/fundoStart.png")
fundoDead = pygame.image.load("Recursos/fundoDead.png")
asteroide = pygame.image.load("Recursos/asteroide.png")
tamanho = (800, 600)
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Space Force")
pygame.display.set_icon(icone)
missileSound = pygame.mixer.Sound("Recursos/missile.mp3")
explosaoSound = pygame.mixer.Sound("Recursos/explosao.wav")
fonte = pygame.font.SysFont("comicsans", 28)
fonteStart = pygame.font.SysFont("comicsans", 55)
fonteMorte = pygame.font.SysFont("arial", 120)
pygame.mixer.music.load("Recursos/ironsound.mp3")

amarelo = (255, 255, 0)
branco = (255, 255, 255)
preto = (0, 0, 0)

def dead(nome, pontos):
    tela.blit(fundoDead, (0,0))
    texto = fonteMorte.render("GAME OVER", True, branco)
    tela.blit(texto, (20, 250))
    texto_pontos = fonte.render(nome + "PONTOS: " + str(pontos), True, branco)
    tela.blit(texto_pontos, (10, 10))
    pygame.display.update()
    pygame.time.wait(2000)

def jogar(nome):
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    posicaoXPersona = 300
    posicaoYPersona = 450
    movimentoXPersona = 0
    posicaoXMissel = 400
    posicaoYMissel = -90
    velocidadeMissel = 1
    pontos = 0
    larguraPersona = 150
    alturaPersona = 149
    larguraMissel = 100
    alturaMissel = 76
    dificuldade = 20

    alien_rect = alien.get_rect()
    alien_rect.x = 0
    alien_rect.y = (300 - alien_rect.height) // 2

    alien_speed = 3
    direita = True

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    movimentoXPersona = 10
                elif evento.key == pygame.K_LEFT:
                    movimentoXPersona = -10
            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    movimentoXPersona = 0

        posicaoXPersona += movimentoXPersona

        if posicaoXPersona < 0:
            posicaoXPersona = 0
        elif posicaoXPersona > 800 - larguraPersona:
            posicaoXPersona = 800 - larguraPersona

        alien_rect.x += alien_speed if direita else -alien_speed
        if alien_rect.x > 800 - alien_rect.width or alien_rect.x < 0:
            direita = not direita

        tela.fill(branco)
        tela.blit(fundo, (0, 0))
        tela.blit(nave, (posicaoXPersona, posicaoYPersona))
        tela.blit(alien, alien_rect)

        posicaoYMissel += velocidadeMissel
        if posicaoYMissel > 600:
            posicaoYMissel = -240
            pontos += 1
            velocidadeMissel += 1
            posicaoXMissel = random.randint(0, 800 - larguraMissel)
            pygame.mixer.Sound.play(missileSound)

        tela.blit(asteroide, (posicaoXMissel, posicaoYMissel))


        texto = fonte.render(nome + "PONTOS: " + str(pontos), True, branco)
        tela.blit(texto, (10, 10))

        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona + larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona + alturaPersona))
        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + larguraMissel))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + alturaMissel))

        if len(set(pixelsMisselY).intersection(pixelsPersonaY)) > dificuldade:
            if len(set(pixelsMisselX).intersection(pixelsPersonaX)) > dificuldade:
                dead(nome, pontos)
                return

        pygame.display.update()
        relogio.tick(60)

def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    
    jogadas  = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8")
        jogadas = eval(arquivo.read())
        arquivo.close()
    except:
        arquivo = open("historico.txt","w",encoding="utf-8")
        arquivo.close()
 
    jogadas[nome] = pontos   
    arquivo = open("historico.txt","w",encoding="utf-8") 
    arquivo.write(str(jogadas))
    arquivo.close()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jogar(nome)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        textoStart = fonteStart.render("RESTART", True, branco)
        tela.blit(textoStart, (400,482))
        textoEnter = fonte.render("Press enter to continue...", True, branco)
        tela.blit(textoEnter, (60,482))
        pygame.display.update()
        relogio.tick(60)


def ranking():
    estrelas = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8" )
        estrelas = eval(arquivo.read())
        arquivo.close()
    except:
        pass
    
    nomes = sorted(estrelas, key=estrelas.get,reverse=True)
    print(estrelas)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    start()

        tela.fill(preto)
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        textoStart = fonteStart.render("BACK TO START", True, branco)
        tela.blit(textoStart, (330,482))
        
        
        posicaoY = 50
        for key,nome in enumerate(nomes):
            if key == 13:
                break
            textoJogador = fonte.render(nome + " - "+str(estrelas[nome]), True, branco)
            tela.blit(textoJogador, (300,posicaoY))
            posicaoY = posicaoY + 30

            
        
        pygame.display.update()
        relogio.tick(60)


def start():
    nome = simpledialog.askstring("Space Force","Nome Completo:")
    
    
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
                elif buttonRanking.collidepoint(evento.pos):
                    ranking()

        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        buttonStart = pygame.draw.rect(tela, amarelo, (300,482,250,100),0)
        buttonRanking = pygame.draw.rect(tela, preto, (570,50,200,50),0,30)
        textoRanking = fonte.render("Ranking", True, branco)
        tela.blit(textoRanking, (620,50))
        textoStart = fonteStart.render("START", True, preto)
        tela.blit(textoStart, (330,482))

        
        
        pygame.display.update()
        relogio.tick(60)

start()