WIDTH = 800
HEIGHT = 600

MENU = "menu"
GAME = "game"

game_state = MENU
music_on = True

start_button = Rect((300, 250), (200, 50))
music_button = Rect((300, 320), (200, 50))
exit_button = Rect((300, 390), (200, 50))

platforms = [
    Rect((0, 560), (800, 40)),
    Rect((100, 480), (120, 20)),
    Rect((260, 420), (120, 20)),
    Rect((420, 360), (120, 20)),
    Rect((580, 300), (120, 20)),
    Rect((420, 240), (120, 20)),
    Rect((260, 180), (120, 20)),
    Rect((100, 120), (120, 20)),
]

# ANIMAÇÕES
enemy_frames = ["inimigo-1", "inimigo-2", "inimigo-3"]

idle_frames = ["parado-1", "parado-2", "parado-3"]

walk_frames_right = [
    "movimentando-1",
    "movimentando-2",
    "movimentando-3",
    "movimentando-4",
    "movimentando-5",
]

walk_frames_left = [
    "movimentandoesq-1",
    "movimentandoesq-2",
    "movimentandoesq-3",
    "movimentandoesq-4",
    "movimentandoesq-5",
]

# PLAYER
player = None
player_speed = 3
velocity_y = 0
jumping = False

gravity = 0.8
jump_strength = -12

coyote_timer = 0
COYOTE_TIME = 6

current_frames = idle_frames
current_frame = 0
frame_timer = 0

# INIMIGO
enemy = None
enemy_speed = 2
enemy_direction = 1
enemy_min_x = 0
enemy_max_x = 0
enemy_frame = 0
enemy_frame_timer = 0


def play_music():
    if music_on:
        music.play("menu")
        music.set_volume(0.5)
    else:
        music.stop()


def start_game():
    global game_state, player
    global velocity_y, jumping, coyote_timer
    global current_frames, current_frame, frame_timer
    global enemy, enemy_min_x, enemy_max_x, enemy_direction

    game_state = GAME

    # PLAYER
    player = Actor(idle_frames[0])
    player.pos = (100, 500)

    velocity_y = 0
    jumping = False
    coyote_timer = 0

    current_frames = idle_frames
    current_frame = 0
    frame_timer = 0

    # INIMIGO NA PLATAFORMA
    plat = platforms[2]  # escolha a plataforma que quer que ele ande

    enemy = Actor(enemy_frames[0])
    enemy.bottom = plat.top
    enemy.x = plat.left

    enemy_min_x = plat.left -50
    enemy_max_x = plat.right
    enemy_direction = 1


def set_animation(frames):
    global current_frames, current_frame, frame_timer
    if current_frames != frames:
        current_frames = frames
        current_frame = 0
        frame_timer = 0
        player.image = current_frames[0]


def update():
    global velocity_y, jumping, coyote_timer
    global frame_timer, current_frame
    global enemy_frame, enemy_frame_timer, enemy_direction
    global game_state

    if game_state != GAME or not player:
        return

    # MOVIMENTO DO PLAYER
    if keyboard.right:
        player.x += player_speed
        set_animation(walk_frames_right)
    elif keyboard.left:
        player.x -= player_speed
        set_animation(walk_frames_left)
    else:
        set_animation(idle_frames)

    player.x = max(player.width // 2, min(WIDTH - player.width // 2, player.x))

    # GRAVIDADE
    velocity_y += gravity
    player.y += velocity_y

    if not jumping:
        coyote_timer = COYOTE_TIME
    else:
        coyote_timer -= 1

    if keyboard.up and coyote_timer > 0:
        velocity_y = jump_strength
        jumping = True
        coyote_timer = 0

    # COLISÃO COM PLATAFORMAS
    on_ground = False
    for plat in platforms:
        if player.colliderect(plat) and velocity_y >= 0:
            if player.bottom <= plat.top + 10:
                player.bottom = plat.top
                velocity_y = 0
                jumping = False
                on_ground = True

    if on_ground:
        coyote_timer = COYOTE_TIME

    if player.y > HEIGHT:
        start_game()

    # ANIMAÇÃO DO PLAYER
    frame_timer += 1
    if frame_timer >= 8:
        frame_timer = 0
        current_frame = (current_frame + 1) % len(current_frames)
        player.image = current_frames[current_frame]

    # MOVIMENTO DO INIMIGO
    if enemy:
        enemy.x += enemy_speed * enemy_direction

        if enemy.left <= enemy_min_x or enemy.right >= enemy_max_x:
            enemy_direction *= -1

        # ANIMAÇÃO DO INIMIGO
        enemy_frame_timer += 1
        if enemy_frame_timer >= 10:
            enemy_frame_timer = 0
            enemy_frame = (enemy_frame + 1) % len(enemy_frames)
            enemy.image = enemy_frames[enemy_frame]

    if enemy and player.colliderect(enemy):
        game_state = MENU


def draw():
    screen.clear()
    if game_state == MENU:
        draw_menu()
    else:
        draw_game()


def draw_menu():
    screen.fill("darkblue")
    screen.draw.text("MEU JOGO PLATFORMER",
                     center=(WIDTH // 2, 150),
                     fontsize=48,
                     color="white")

    screen.draw.filled_rect(start_button, "green")
    screen.draw.text("Iniciar", center=start_button.center, fontsize=30, color="black")

    screen.draw.filled_rect(music_button, "yellow")
    text = "Música: ON" if music_on else "Música: OFF"
    screen.draw.text(text, center=music_button.center, fontsize=26, color="black")

    screen.draw.filled_rect(exit_button, "red")
    screen.draw.text("Sair", center=exit_button.center, fontsize=30, color="black")


def draw_game():
    screen.fill((135, 206, 235))
    screen.draw.filled_rect(Rect((0, 400), (800, 200)), "lightgreen")
    screen.draw.filled_rect(Rect((0, 500), (800, 100)), "green")

    for i, plat in enumerate(platforms):
        color = "saddlebrown" if i % 2 == 0 else "peru"
        screen.draw.filled_rect(plat, color)

    if enemy:
        enemy.draw()

    player.draw()


def on_mouse_down(pos):
    global music_on

    if game_state == MENU:
        if start_button.collidepoint(pos):
            start_game()
        elif music_button.collidepoint(pos):
            music_on = not music_on
            play_music()
        elif exit_button.collidepoint(pos):
            quit()


play_music()
