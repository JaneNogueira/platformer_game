import pgzrun
import math
import random
from pgzero.actor import Actor
from pygame import Rect

# Configuração da janela do jogo
WIDTH = 512
HEIGHT = 512
TITLE = "Platformer Game"

# Estado do jogo inicial
game_state = "MENU"
music_on = True

# Definição da física do jogo
GRAVITY = 0.5
JUMP_VELOCITY = -11
MOVE_SPEED = 10
ANIMATION_SPEED = 10

# Classe do herói
class Hero:
    def __init__(self):
        self.images_idle = ["hero_duck", "hero_front","hero_idle","hero_front", "hero_duck"]
        self.images_run = ["hero_climb_a", "hero_climb_b", "hero_hit", "hero_idle"]
        self.actor = Actor(self.images_idle[0], (80, 200))
        self.vy = 0
        self.on_ground = False
        self.frame = 0
        self.anim_timer = 0
        self.invincible_timer = 60 # 1 segundo de invencibilidade inicial

    def apply_gravity(self):
        self.vy += GRAVITY
        if self.vy > 10:
            self.vy = 10
        self.actor.y += self.vy

    def handle_platforms(self):
        self.on_ground = False
        for plat in platforms:
            # Verifica colisão
            if self.actor.colliderect(plat):
                # Se o herói está caindo e toca a parte de cima da plataforma
                if self.vy >= 0 and self.actor.bottom >= plat.top and self.actor.bottom <= plat.top + 20:
                    self.actor.bottom = plat.top
                    self.vy = 0
                    self.on_ground = True

    def update_animation(self, running):
        self.anim_timer += 1
        if self.anim_timer >= ANIMATION_SPEED:
            self.anim_timer = 0
            if running and self.on_ground:
                self.frame = (self.frame + 1) % len(self.images_run)
                self.actor.image = self.images_run[self.frame]
            elif self.on_ground:
                self.frame = (self.frame + 1) % len(self.images_idle)
                self.actor.image = self.images_idle[self.frame]
            else:
                self.actor.image = "hero_jump"

    def update(self, running):
        self.apply_gravity()
        self.handle_platforms()
        self.update_animation(running)

    def jump(self):
        if self.on_ground:
            self.vy = JUMP_VELOCITY
            self.on_ground = False

    def draw(self):
        self.actor.draw()

# Classe do inimigo
class Enemy:
    def __init__(self, x, y):
        self.images = ["enemy_attack_a", "enemy_attack_b", "enemy_attack_rest"]
        self.actor = Actor(self.images[0], (x, y))
        self.frame = 0
        self.anim_timer = 0
        self.direction = random.choice([-1, 1])
        self.left_limit = x - 60 # Limite esquerdo do movimento
        self.right_limit = x + 60 # Limite direito do movimento

    def update(self):
        self.anim_timer += 1
        if self.anim_timer >= ANIMATION_SPEED:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % len(self.images)
            self.actor.image = self.images[self.frame]

        self.actor.x += self.direction
        if self.actor.x > self.right_limit:
            self.direction = -1
            self.actor.flip_x = True
        elif self.actor.x < self.left_limit:
            self.direction = 1
            self.actor.flip_x = False

    def draw(self):
        self.actor.draw()

# Plataformas (Rect é um retângulo de Pygame)
platforms = [
    Rect((10, 490), (200, 20)), # Plataforma inicial (inferior)
    Rect((300, 360), (200, 20)), # Plataforma meio
    Rect((10, 230), (200, 20)), # Plataforma superior 1
    Rect((300, 110), (200, 20)), # Plataforma de vitória (topo)
]

# Instâncias do herói e inimigos
hero = Hero()
# Posições iniciais dos inimigos (ajustadas para a plataforma)
enemies = [Enemy(420, 310), Enemy(350, 230)]

# Atualização do jogo
def update():
    global game_state
    if game_state == "PLAYING":
        running = keyboard.left or keyboard.right

        # Movimento lateral
        if keyboard.left and hero.actor.left > 0:
            hero.actor.x -= MOVE_SPEED
        if keyboard.right and hero.actor.right < WIDTH:
            hero.actor.x += MOVE_SPEED

        # Atualiza física, colisão e animação
        hero.update(running)

        # Contador de invencibilidade
        if hero.invincible_timer > 0:
            hero.invincible_timer -= 1

        # Verifica vitória: se o herói está em cima da última plataforma
        last_platform = platforms[-1]
        if hero.on_ground and hero.actor.bottom == last_platform.top:
            game_state = "WIN"

        # Atualiza inimigos e verifica colisão
        for enemy in enemies:
            enemy.update()

            if hero.invincible_timer == 0:
                # Calcula distância entre herói e inimigo
                dx = hero.actor.x - enemy.actor.x
                dy = hero.actor.y - enemy.actor.y
                dist = math.hypot(dx, dy)

                # Colisão: só considera se estiver perto
                if dist < 40:
                    game_state = "GAME_OVER"

# Desenho da tela
def draw():
    global start_btn, music_btn, exit_btn, restart_btn

    screen.clear()
    screen.fill((135, 206, 235))
    if game_state == "MENU":
        screen.draw.text("Platformer Game", center=(WIDTH//2, HEIGHT//2-50), fontsize=50, color="white")
        
        # Define os Retângulos dos Botões (Rect)
        start_btn = Rect((200, 250), (120, 40))
        music_btn = Rect((200, 300), (120, 40))
        exit_btn = Rect((200, 350), (120, 40))
        
        # Desenha os botões
        screen.draw.filled_rect(start_btn, (0, 255, 0))
        screen.draw.text("START", center=start_btn.center, fontsize=30, color="black")
        screen.draw.filled_rect(music_btn, (0, 200, 255))
        screen.draw.text("MUSIC", center=music_btn.center, fontsize=30, color="black")
        screen.draw.filled_rect(exit_btn, (255, 0, 0))
        screen.draw.text("EXIT", center=exit_btn.center, fontsize=30, color="black")

    elif game_state == "PLAYING":
        for plat in platforms:
            screen.draw.filled_rect(plat, (100, 100, 255))
        hero.draw()
        for enemy in enemies:
            enemy.draw()

    elif game_state == "GAME_OVER":
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")

        # Define os Retângulos dos Botões
        restart_btn = Rect((200, 300), (120, 40))
        exit_btn = Rect((200, 360), (120, 40))

        # Desenha os botões
        screen.draw.filled_rect(restart_btn, (0, 255, 0))
        screen.draw.text("RESTART", center=restart_btn.center, fontsize=30, color="black")
        screen.draw.filled_rect(exit_btn, (255, 0, 0))
        screen.draw.text("EXIT", center=exit_btn.center, fontsize=30, color="black")

    elif game_state == "WIN":
        screen.draw.text("YOU WIN!", center=(WIDTH//2, HEIGHT//2-80), fontsize=60, color="green")

        # Define o Retângulo do Botão
        restart_btn = Rect((200, 300), (120, 40))

        # Desenha o botão
        screen.draw.filled_rect(restart_btn, (0, 255, 0))
        screen.draw.text("RESTART", center=restart_btn.center, fontsize=30, color="black")

# Cliques do Mouse
def on_mouse_down(pos):
    global game_state, music_on, start_btn, music_btn, exit_btn, restart_btn
    
    if game_state == "MENU":
        if start_btn.collidepoint(pos):
            game_state = "PLAYING"
            # Reinicia posições
            hero.actor.pos = (100, 200)
            hero.vy = 0
            enemies.clear()
            enemies.extend([Enemy(400, 328), Enemy(120, 198)])
            if music_on:
                music.play("soundtrack_loop")
        elif music_btn.collidepoint(pos):
            music_on = not music_on
            if music_on:
                music.play("soundtrack_loop")
            else:
                music.stop()
        elif exit_btn.collidepoint(pos):
            exit()
    
    elif game_state == "PLAYING":
        hero.jump()
    
    elif game_state == "GAME_OVER":
        if restart_btn.collidepoint(pos):
            game_state = "PLAYING"
            # Reinicia posições
            hero.actor.pos = (100, 200)
            hero.vy = 0
            enemies.clear()
            enemies.extend([Enemy(400, 328), Enemy(120, 198)])
        elif exit_btn.collidepoint(pos):
            exit()

    elif game_state == "WIN":
        if restart_btn.collidepoint(pos):
            game_state = "PLAYING"
            # Reinicia posições
            hero.actor.pos = (100, 200)
            hero.vy = 0
            enemies.clear()
            enemies.extend([Enemy(400, 328), Enemy(120, 198)])

pgzrun.go()