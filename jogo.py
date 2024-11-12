# Exemplo 5 - Mapa com Câmera que segue o jogador
import pygame

# Configurações iniciais
width, height = 50 * 14, 50 * 10
mapa = []
tile = {}
player_walk = []
player_anim_frame = 1
playerpos_x, playerpos_y = 100, 225
player_anim_time = 0
gravity = 0.5
vel_y = 0
vel_x = 0.2
is_jumping = False
is_Running = False
RunningCoolDown = 0

# Variáveis da câmera
camera_x, camera_y = 0, 0
screen_width, screen_height = width, height  # Tamanho da tela de exibição

def load_mapa(filename):
    global mapa
    with open(filename, "r") as file:
        for line in file:
            mapa.append(line.strip())

def load():
    global clock, tile, player_walk, collider_mapa, collider_wall1, collider_wall2
    clock = pygame.time.Clock()
    load_mapa("mapa.txt")
    tile['A'] = pygame.image.load("water.png")
    tile['C'] = pygame.image.load("ground.png")
    tile['G'] = pygame.image.load("grass.png")
    tile['W'] = pygame.image.load("Wall.png")
    collider_mapa = pygame.Rect(0, 400, 800, 100)
    for i in range(1, 5): #carrega as imagens da animação
        player_walk.append(pygame.image.load("Hero_Walk_0" + str(i) + ".png"))
    for j in range(5, 9): #carrega as imagens da animação
        player_walk.append(pygame.image.load("Hero_Walk_0" + str(j) + ".png"))
    for k in range(8, 13): #carrega as imagens da animação
        if k <= 9:
            player_walk.append(pygame.image.load("Hero_Walk_0" + str(k) + ".png"))
        else:
            player_walk.append(pygame.image.load("Hero_Walk_" + str(k) + ".png"))        
    for l in range(13, 17): #carrega as imagens da animação
        player_walk.append(pygame.image.load("Hero_Walk_" + str(l) + ".png"))

def update(dt):
    global vel_y, vel_x, is_Running, RunningCoolDown, player_anim_frame, playerpos_x, playerpos_y, player_anim_time, old_x, old_y, collider_jogador, camera_x, camera_y, gravity, is_jumping
    old_x, old_y = playerpos_x, playerpos_y
    keys = pygame.key.get_pressed()

    # Aplicar gravidade ao jogador
    vel_y += gravity
    playerpos_y += vel_y
    RunningCoolDown += dt

    # Movimento lateral do jogador
    if keys[pygame.K_RIGHT]:
        playerpos_x += vel_x * dt
        player_anim_time += dt  # incrementa o tempo usando dt
        if player_anim_time > 100:  # quando acumular mais de 100 ms
            player_anim_frame += 1  # avança para o próximo frame
            if player_anim_frame > 3:  # loop da animação
                player_anim_frame = 0
            player_anim_time = 0  # reinicializa a contagem do tempo

    if keys[pygame.K_LSHIFT]:
        if(is_Running == False and RunningCoolDown > 100):
            vel_x = 2*vel_x
            is_Running = True
            RunningCoolDown = 0
        elif (is_Running == True) and RunningCoolDown > 100:
            vel_x = vel_x/2
            is_Running = False
            RunningCoolDown = 0
        

    if keys[pygame.K_LEFT]:
        if player_anim_frame < 5:
            player_anim_frame = 5
        playerpos_x -= vel_x * dt
        player_anim_time += dt
        if player_anim_time > 100:
            player_anim_frame += 1
            if player_anim_frame > 7:
                player_anim_frame = 5
            player_anim_time = 0

    # Fazer o jogador pular ao pressionar a seta para cima, se estiver no chão
    if keys[pygame.K_UP] and is_jumping == False:
        vel_y = -7  # Ajuste a velocidade de pulo conforme necessário
        playerpos_y += vel_y - gravity 
        is_jumping = True

    # Configura o retângulo de colisão do jogador
    collider_jogador = pygame.Rect(playerpos_x + 40, playerpos_y + 60, 40, 60)
    # Verifica a colisão com o chão
    if collider_jogador.colliderect(collider_mapa):
        playerpos_y = old_y  # reposiciona o jogador ao solo
        vel_y = 0  # zera a velocidade ao tocar o solo
        is_jumping = False  # permite outro pulo

    # Atualização da câmera para seguir o jogador
    camera_x = playerpos_x - screen_width // 2
    camera_y = playerpos_y - screen_height // 2

def draw_screen(screen):
    screen.fill((255, 255, 255))
    # Desenha o mapa com base na posição da câmera
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            tile_char = mapa[i][j]
            tile_image = tile.get(tile_char)
            if tile_image:
                screen.blit(tile_image, ((j * 50) - camera_x, (i * 50) - camera_y))

    # Desenha o herói com base na posição da câmera
    screen.blit(player_walk[player_anim_frame], (playerpos_x - camera_x, playerpos_y - camera_y))

def main_loop(screen):
    global clock
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                break
        clock.tick(60)
        dt = clock.get_time()
        update(dt)
        draw_screen(screen)
        pygame.display.update()

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
load()
main_loop(screen)
pygame.quit()
