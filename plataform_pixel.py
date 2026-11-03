
import pygame
import sys
import math
import random

# ==========================================
# 1. CONFIGURACOES
# ==========================================

pygame.init()

LARGURA = 900
ALTURA = 600
MUNDO_LARGURA = 3000
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Aventura Pixel")

relogio = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
PRETO = (15, 10, 25)
VERMELHO = (230, 35, 75)
ROSA = (255, 130, 170)
ROXO = (90, 40, 130)
AMARELO = (255, 210, 70)
VERDE = (70, 220, 130)

fonte = pygame.font.SysFont("arial", 20)
fonte_grande = pygame.font.SysFont("arial", 42)

# ==========================================
# 2. PERSONAGEM E SOBREVIVENCIA
# ==========================================

personagem = pygame.Rect(100, 430, 50, 60)

velocidade = 5
velocidade_y = 0
gravidade = 0.6
forca_pulo = -13
no_chao = False

vida_maxima = 5
vidas = 3

energia_maxima = 100
energia = 100

moedas = 0

inventario = {
    "Pocao de vida": 0,
    "Comida": 0,
    "Lanterna": 0
}

lanterna_ativa = False

ultimo_dano = 0
tempo_protecao = 1200

tempo_energia = pygame.time.get_ticks()
intervalo_energia = 2500

# ==========================================
# 3. CAMERA
# ==========================================

camera_x = 0

def atualizar_camera():
    global camera_x

    alvo = personagem.centerx - LARGURA // 2
    camera_x += (alvo - camera_x) * 0.10

    camera_x = max(
        0,
        min(camera_x, MUNDO_LARGURA - LARGURA)
    )

# ==========================================
# 4. PLATAFORMAS
# ==========================================

plataformas = [
    pygame.Rect(0, 540, MUNDO_LARGURA, 60),
    pygame.Rect(250, 450, 160, 20),
    pygame.Rect(500, 390, 150, 20),
    pygame.Rect(750, 460, 160, 20),
    pygame.Rect(1000, 400, 160, 20),
    pygame.Rect(1300, 450, 160, 20),
    pygame.Rect(1550, 380, 170, 20),
    pygame.Rect(1850, 450, 150, 20),
    pygame.Rect(2150, 390, 170, 20),
    pygame.Rect(2500, 450, 180, 20)
]

def desenhar_plataformas():
    for plataforma in plataformas:

        x = int(plataforma.x - camera_x)

        pygame.draw.rect(
            tela,
            (75, 55, 110),
            (x, plataforma.y, plataforma.width, plataforma.height)
        )

        pygame.draw.rect(
            tela,
            (160, 100, 210),
            (x, plataforma.y, plataforma.width, 5)
        )

# ==========================================
# 5. MOEDAS
# ==========================================

moedas_mapa = [
    pygame.Rect(280, 410, 20, 20),
    pygame.Rect(340, 410, 20, 20),
    pygame.Rect(530, 350, 20, 20),
    pygame.Rect(580, 350, 20, 20),
    pygame.Rect(790, 420, 20, 20),
    pygame.Rect(1050, 360, 20, 20),
    pygame.Rect(1350, 410, 20, 20),
    pygame.Rect(1600, 340, 20, 20),
    pygame.Rect(1900, 410, 20, 20),
    pygame.Rect(2200, 350, 20, 20),
    pygame.Rect(2550, 410, 20, 20)
]

# ==========================================
# 6. SISTEMA DE MISSOES
# ==========================================

npc_morador = pygame.Rect(1100, 480, 40, 60)

missao_status = "disponivel"

moedas_missao = 0
objetivo_missao = 5
recompensa_missao = 10

def atualizar_missao():
    global missao_status

    if missao_status == "ativa":

        if moedas_missao >= objetivo_missao:
            missao_status = "concluida"


def interagir_missao():
    global missao_status
    global moedas, moedas_missao

    if missao_status == "disponivel":

        missao_status = "ativa"
        moedas_missao = 0

    elif missao_status == "concluida":

        moedas += recompensa_missao
        missao_status = "resgatada"


def desenhar_morador():

    x = int(npc_morador.x - camera_x)

    # Corpo
    pygame.draw.rect(
        tela,
        (90, 60, 150),
        (x, npc_morador.y + 20, 40, 40),
        border_radius=6
    )

    # Cabeca
    pygame.draw.circle(
        tela,
        (230, 185, 150),
        (x + 20, npc_morador.y + 12),
        14
    )

    # Olhos
    pygame.draw.circle(
        tela, PRETO,
        (x + 15, npc_morador.y + 10), 2
    )

    pygame.draw.circle(
        tela, PRETO,
        (x + 25, npc_morador.y + 10), 2
    )

    # Indicador de missao
    if missao_status == "disponivel":
        pygame.draw.circle(
            tela, AMARELO,
            (x + 20, npc_morador.y - 15), 9
        )

    elif missao_status == "concluida":
        pygame.draw.circle(
            tela, VERDE,
            (x + 20, npc_morador.y - 15), 9
        )


def desenhar_mensagem_missao():

    if missao_status == "disponivel":
        mensagem = "Converse com o morador!"

    elif missao_status == "ativa":
        mensagem = "Colete moedas: " + str(moedas_missao) + "/5"

    elif missao_status == "concluida":
        mensagem = "Volte ao morador para receber a recompensa!"

    else:
        mensagem = "Missao 01 concluida!"

    texto = fonte.render(
        mensagem,
        True,
        AMARELO
    )

    tela.blit(texto, (300, 25))


# ==========================================
# 7. COLETAR MOEDAS
# ==========================================

def coletar_moedas():
    global moedas, moedas_missao

    for moeda in moedas_mapa[:]:

        if personagem.colliderect(moeda):

            moedas += 1
            moedas_mapa.remove(moeda)

            if missao_status == "ativa":

                moedas_missao += 1
                atualizar_missao()


def desenhar_moedas():

    for moeda in moedas_mapa:

        x = int(moeda.x - camera_x)

        pygame.draw.circle(
            tela,
            AMARELO,
            (x + 10, moeda.y + 10),
            10
        )

        pygame.draw.circle(
            tela,
            (255, 245, 160),
            (x + 7, moeda.y + 7),
            3
        )

# ==========================================
# 8. INIMIGOS
# ==========================================

inimigos = [
    {
        "rect": pygame.Rect(350, 485, 40, 55),
        "velocidade": 2,
        "esquerda": 300,
        "direita": 450,
        "cor": (130, 50, 180)
    },
    {
        "rect": pygame.Rect(850, 485, 40, 55),
        "velocidade": 3,
        "esquerda": 800,
        "direita": 1000,
        "cor": (40, 100, 200)
    },
    {
        "rect": pygame.Rect(1400, 485, 40, 55),
        "velocidade": 2,
        "esquerda": 1300,
        "direita": 1500,
        "cor": (180, 60, 90)
    },
    {
        "rect": pygame.Rect(2200, 485, 40, 55),
        "velocidade": 2,
        "esquerda": 2150,
        "direita": 2350,
        "cor": (40, 150, 120)
    }
]

def atualizar_inimigos():

    for inimigo in inimigos:

        inimigo["rect"].x += inimigo["velocidade"]

        if inimigo["rect"].right >= inimigo["direita"]:
            inimigo["velocidade"] *= -1

        if inimigo["rect"].left <= inimigo["esquerda"]:
            inimigo["velocidade"] *= -1


def desenhar_inimigos():

    for inimigo in inimigos:

        r = inimigo["rect"]
        x = int(r.x - camera_x)

        pygame.draw.rect(
            tela,
            inimigo["cor"],
            (x, r.y, r.width, r.height),
            border_radius=8
        )

        pygame.draw.circle(
            tela,
            (230, 190, 170),
            (x + 20, r.y + 8),
            14
        )

        pygame.draw.circle(
            tela, PRETO,
            (x + 15, r.y + 7), 2
        )

        pygame.draw.circle(
            tela, PRETO,
            (x + 25, r.y + 7), 2
        )


def verificar_colisao_inimigos():

    global vidas, ultimo_dano, velocidade_y

    agora = pygame.time.get_ticks()

    for inimigo in inimigos:

        if personagem.colliderect(inimigo["rect"]):

            if agora - ultimo_dano >= tempo_protecao:

                vidas -= 1
                ultimo_dano = agora

                if personagem.centerx < inimigo["rect"].centerx:
                    personagem.x -= 60
                else:
                    personagem.x += 60

                personagem.x = max(
                    0,
                    min(personagem.x, MUNDO_LARGURA - personagem.width)
                )

                velocidade_y = -5
                vidas = max(0, vidas)

                break

# ==========================================
# 9. PERSONAGEM CORACAO
# ==========================================

def desenhar_coracao():

    tempo = pygame.time.get_ticks()
    pulsacao = math.sin(tempo * 0.006) * 3

    x = personagem.centerx - camera_x
    y = personagem.centery

    tamanho = 25 + pulsacao

    pontos = [
        (x, y + tamanho),
        (x - tamanho, y),
        (x - tamanho, y - 12),
        (x - tamanho / 2, y - tamanho),
        (x, y - tamanho / 2),
        (x + tamanho / 2, y - tamanho),
        (x + tamanho, y - 12),
        (x + tamanho, y)
    ]

    pygame.draw.polygon(
        tela,
        VERMELHO,
        pontos
    )

    pygame.draw.circle(
        tela, PRETO,
        (int(x - 9), int(y - 8)), 3
    )

    pygame.draw.circle(
        tela, PRETO,
        (int(x + 9), int(y - 8)), 3
    )

    pygame.draw.circle(
        tela, ROSA,
        (int(x - 17), int(y + 4)), 4
    )

    pygame.draw.circle(
        tela, ROSA,
        (int(x + 17), int(y + 4)), 4
    )

# ==========================================
# 10. LOJAS E CASAS
# ==========================================

lojas = [
    {
        "nome": "Loja Magica",
        "area": pygame.Rect(650, 460, 100, 80)
    },
    {
        "nome": "Casa da Vila",
        "area": pygame.Rect(1700, 460, 100, 80)
    }
]

itens_loja = [
    {"nome": "Pocao de vida", "preco": 5},
    {"nome": "Comida", "preco": 3},
    {"nome": "Lanterna", "preco": 8}
]

loja_aberta = False

def desenhar_lojas():

    for loja in lojas:

        area = loja["area"]
        x = int(area.x - camera_x)

        pygame.draw.rect(
            tela,
            (65, 35, 100),
            (x, area.y, area.width, area.height)
        )

        pygame.draw.polygon(
            tela,
            (160, 50, 100),
            [
                (x - 10, area.y),
                (x + 50, area.y - 45),
                (x + 110, area.y)
            ]
        )

        pygame.draw.rect(
            tela,
            (35, 20, 55),
            (x + 35, area.y + 35, 30, 45)
        )

        nome = fonte.render(
            loja["nome"],
            True,
            BRANCO
        )

        tela.blit(nome, (x - 25, area.y - 75))


def comprar_item(numero):

    global moedas

    if numero < 0 or numero >= len(itens_loja):
        return

    item = itens_loja[numero]

    if moedas >= item["preco"]:

        moedas -= item["preco"]

        nome = item["nome"]

        inventario[nome] = inventario.get(nome, 0) + 1


def desenhar_loja():

    pygame.draw.rect(
        tela,
        (25, 15, 45),
        (200, 130, 500, 350),
        border_radius=15
    )

    pygame.draw.rect(
        tela,
        (170, 100, 220),
        (200, 130, 500, 350),
        3,
        border_radius=15
    )

    titulo = fonte_grande.render(
        "LOJA MAGICA",
        True,
        BRANCO
    )

    tela.blit(titulo, (310, 155))

    for i, item in enumerate(itens_loja):

        texto = fonte.render(
            f"{i + 1} - {item['nome']} - {item['preco']} moedas",
            True,
            BRANCO
        )

        tela.blit(texto, (250, 245 + i * 55))

    fechar = fonte.render(
        "ESC - Fechar loja",
        True,
        ROSA
    )

    tela.blit(fechar, (330, 420))

# ==========================================
# 11. SISTEMA DE ITENS
# ==========================================

def usar_pocao():

    global vidas

    if inventario["Pocao de vida"] > 0:

        if vidas < vida_maxima:

            vidas += 1
            inventario["Pocao de vida"] -= 1


def usar_comida():

    global energia

    if inventario["Comida"] > 0:

        energia = min(
            energia_maxima,
            energia + 30
        )

        inventario["Comida"] -= 1


def usar_lanterna():

    global lanterna_ativa

    if lanterna_ativa:

        lanterna_ativa = False

    elif inventario["Lanterna"] > 0:

        lanterna_ativa = True
        inventario["Lanterna"] -= 1

# ==========================================
# 12. SISTEMA DE ENERGIA
# ==========================================

def atualizar_energia():

    global energia, tempo_energia

    agora = pygame.time.get_ticks()
    teclas = pygame.key.get_pressed()

    andando = (
        teclas[pygame.K_RIGHT]
        or teclas[pygame.K_LEFT]
        or teclas[pygame.K_a]
        or teclas[pygame.K_d]
    )

    if andando and not loja_aberta:

        if agora - tempo_energia >= intervalo_energia:

            energia = max(0, energia - 1)
            tempo_energia = agora

    else:

        tempo_energia = agora

# ==========================================
# 13. LANTERNA
# ==========================================

def desenhar_lanterna():

    if lanterna_ativa:

        x = int(personagem.centerx - camera_x)
        y = personagem.centery

        luz = pygame.Surface(
            (LARGURA, ALTURA),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            luz,
            (255, 230, 130, 45),
            (x, y),
            170
        )

        tela.blit(luz, (0, 0))

# ==========================================
# 14. CIDADE NOTURNA
# ==========================================

estrelas = []

for i in range(80):

    estrelas.append((
        random.randint(0, MUNDO_LARGURA),
        random.randint(20, 300),
        random.randint(1, 3)
    ))


def desenhar_cenario():

    tela.fill((12, 8, 35))

    # Lua
    pygame.draw.circle(
        tela,
        (245, 230, 190),
        (750, 90),
        42
    )

    pygame.draw.circle(
        tela,
        (12, 8, 35),
        (765, 75),
        40
    )

    # Estrelas
    for estrela in estrelas:

        x, y, tamanho = estrela
        pos_x = x - camera_x * 0.3

        if -5 < pos_x < LARGURA + 5:

            pygame.draw.circle(
                tela,
                BRANCO,
                (int(pos_x), y),
                tamanho
            )

    # Predios
    for i in range(35):

        x = i * 100 - camera_x * 0.5
        altura = 150 + (i * 37 % 180)

        if -120 < x < LARGURA + 120:

            pygame.draw.rect(
                tela,
                (30, 20, 65),
                (x, 540 - altura, 75, altura)
            )

            for janela_y in range(
                int(550 - altura), 530, 35
            ):

                pygame.draw.rect(
                    tela,
                    (255, 210, 100),
                    (x + 15, janela_y, 10, 15)
                )

                pygame.draw.rect(
                    tela,
                    (120, 90, 200),
                    (x + 45, janela_y, 10, 15)
                )

    # Chao
    pygame.draw.rect(
        tela,
        (35, 25, 65),
        (0, 540, LARGURA, 60)
    )

    pygame.draw.line(
        tela,
        (130, 70, 180),
        (0, 540),
        (LARGURA, 540),
        4
    )

# ==========================================
# 15. HUD - INFORMACOES
# ==========================================

def desenhar_hud():

    texto_moedas = fonte.render(
        f"Moedas: {moedas}",
        True,
        AMARELO
    )

    texto_vidas = fonte.render(
        f"Vidas: {vidas}/{vida_maxima}",
        True,
        BRANCO
    )

    texto_energia = fonte.render(
        f"Energia: {energia}%",
        True,
        BRANCO
    )

    tela.blit(texto_moedas, (20, 20))
    tela.blit(texto_vidas, (20, 50))
    tela.blit(texto_energia, (20, 80))

    # Barra de energia
    pygame.draw.rect(
        tela,
        (70, 40, 60),
        (20, 110, 160, 15)
    )

    pygame.draw.rect(
        tela,
        VERDE,
        (
            20,
            110,
            int(160 * energia / energia_maxima),
            15
        )
    )

    # Inventario
    y = 140

    for nome, quantidade in inventario.items():

        texto = fonte.render(
            f"{nome}: {quantidade}",
            True,
            BRANCO
        )

        tela.blit(texto, (20, y))
        y += 25

    if lanterna_ativa:

        aviso = fonte.render(
            "Lanterna ligada",
            True,
            AMARELO
        )

        tela.blit(aviso, (20, 225))

    # Aviso de loja
    for loja in lojas:

        if personagem.colliderect(loja["area"]):

            aviso = fonte.render(
                "Pressione E para abrir a loja",
                True,
                AMARELO
            )

            tela.blit(aviso, (300, 550))

    # Aviso do morador
    if personagem.colliderect(npc_morador):

        if missao_status == "disponivel":
            mensagem = "E - Conversar com morador"

        elif missao_status == "concluida":
            mensagem = "E - Receber recompensa"

        elif missao_status == "ativa":
            mensagem = "Missao em andamento"

        else:
            mensagem = "Missao concluida!"

        aviso = fonte.render(
            mensagem,
            True,
            AMARELO
        )

        tela.blit(aviso, (300, 515))

    # Informacoes da missao
    desenhar_mensagem_missao()

# ==========================================
# 16. GAME OVER
# ==========================================

def tela_game_over():

    esperando = True

    while esperando:

        tela.fill((15, 5, 30))

        titulo = fonte_grande.render(
            "GAME OVER",
            True,
            VERMELHO
        )

        mensagem = fonte.render(
            "Pressione ENTER ou ESC para sair",
            True,
            BRANCO
        )

        tela.blit(
            titulo,
            (
                LARGURA // 2 - titulo.get_width() // 2,
                220
            )
        )

        tela.blit(
            mensagem,
            (
                LARGURA // 2 - mensagem.get_width() // 2,
                310
            )
        )

        pygame.display.flip()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key in (
                    pygame.K_RETURN,
                    pygame.K_ESCAPE
                ):

                    esperando = False

        relogio.tick(FPS)

# ==========================================
# 17. LOOP PRINCIPAL
# ==========================================

rodando = True

while rodando:

    relogio.tick(FPS)

    # EVENTOS
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            rodando = False

        if evento.type == pygame.KEYDOWN:

            # Pular
            if evento.key in (
                pygame.K_SPACE,
                pygame.K_w,
                pygame.K_UP
            ):

                if no_chao and not loja_aberta:

                    velocidade_y = forca_pulo
                    no_chao = False

            # Usar pocao
            if evento.key == pygame.K_h:
                usar_pocao()

            # Usar comida
            if evento.key == pygame.K_j:
                usar_comida()

            # Usar lanterna
            if evento.key == pygame.K_l:
                usar_lanterna()

            # Interagir com morador ou loja
            if evento.key == pygame.K_e:

                if not loja_aberta:

                    if personagem.colliderect(npc_morador):

                        interagir_missao()

                    else:

                        for loja in lojas:

                            if personagem.colliderect(loja["area"]):

                                loja_aberta = True
                                break

            # Comprar itens
            if loja_aberta:

                if evento.key == pygame.K_1:
                    comprar_item(0)

                if evento.key == pygame.K_2:
                    comprar_item(1)

                if evento.key == pygame.K_3:
                    comprar_item(2)

                if evento.key == pygame.K_ESCAPE:
                    loja_aberta = False

    # ======================================
    # MOVIMENTACAO
    # ======================================

    if not loja_aberta:

        teclas = pygame.key.get_pressed()

        velocidade_atual = velocidade

        # Energia baixa deixa o personagem mais lento
        if energia <= 0:
            velocidade_atual = 2

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            personagem.x += velocidade_atual

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            personagem.x -= velocidade_atual

        # Limites do mundo
        personagem.x = max(
            0,
            min(
                personagem.x,
                MUNDO_LARGURA - personagem.width
            )
        )

        # Gravidade
        velocidade_y += gravidade
        personagem.y += int(velocidade_y)

        no_chao = False

        # Colisao com plataformas
        for plataforma in plataformas:

            if personagem.colliderect(plataforma):

                if velocidade_y > 0:

                    personagem.bottom = plataforma.top
                    velocidade_y = 0
                    no_chao = True

                elif velocidade_y < 0:

                    personagem.top = plataforma.bottom
                    velocidade_y = 0

        # Atualizar inimigos
        atualizar_inimigos()

        # Verificar colisao com inimigos
        verificar_colisao_inimigos()

        # Coletar moedas
        coletar_moedas()

        # Atualizar energia
        atualizar_energia()

    # Atualizar camera
    atualizar_camera()

    # ======================================
    # DESENHO
    # ======================================

    desenhar_cenario()
    desenhar_lanterna()
    desenhar_plataformas()
    desenhar_morador()
    desenhar_moedas()
    desenhar_lojas()
    desenhar_inimigos()
    desenhar_coracao()
    desenhar_hud()

    if loja_aberta:
        desenhar_loja()

    pygame.display.flip()

    # Game Over
    if vidas <= 0:

        tela_game_over()
        rodando = False

pygame.quit()
sys.exit()


