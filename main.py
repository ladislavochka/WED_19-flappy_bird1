from pygame import *
import random

from collect_data import DataCollector


init()

WIDTH = 600
HEIGHT = 500
FPS = 60

screen = display.set_mode(
    (WIDTH, HEIGHT)
)

display.set_caption(
    "Simple Flappy Bird"
)

clock = time.Clock()
game_font = font.Font(None, 40)


# Пташка
bird_x = 120
bird_y = 250
bird_radius = 18

bird_speed = 0
gravity = 0.5
jump_power = -8


# Перешкода
pipe_x = WIDTH
pipe_width = 70
pipe_gap = 170
pipe_speed = 4

gap_y = random.randint(
    120,
    HEIGHT - 120
)


score = 0
running = True

# Створюємо збирач даних
collector = DataCollector(
    "flappy_data.csv"
)

# Записуємо один приклад кожні 10 кадрів
collect_interval = 10
frame_count = 0


while running:
    clock.tick(FPS)

    frame_count += 1

    # За замовчуванням пташка не стрибає
    action = "wait"

    for current_event in event.get():
        if current_event.type == QUIT:
            running = False

        if current_event.type == KEYDOWN:
            if current_event.key == K_SPACE:
                # Записуємо стан до виконання стрибка
                action = "jump"

                collector.collect(
                    bird_y=bird_y,
                    bird_speed=bird_speed,
                    pipe_x=pipe_x,
                    gap_y=gap_y,
                    bird_x=bird_x,
                    score=score,
                    action=action,
                )

                bird_speed = jump_power

    # Записуємо приклади без стрибка
    if (
        frame_count % collect_interval == 0
        and action == "wait"
    ):
        collector.collect(
            bird_y=bird_y,
            bird_speed=bird_speed,
            pipe_x=pipe_x,
            gap_y=gap_y,
            bird_x=bird_x,
            score=score,
            action=action,
        )

    # Гравітація
    bird_speed += gravity
    bird_y += bird_speed

    # Рух перешкоди
    pipe_x -= pipe_speed

    # Створення нової перешкоди
    if pipe_x + pipe_width < 0:
        pipe_x = WIDTH

        gap_y = random.randint(
            120,
            HEIGHT - 120
        )

        score += 1

    top_pipe = Rect(
        pipe_x,
        0,
        pipe_width,
        gap_y - pipe_gap // 2
    )

    bottom_pipe = Rect(
        pipe_x,
        gap_y + pipe_gap // 2,
        pipe_width,
        HEIGHT
    )

    bird_rect = Rect(
        bird_x - bird_radius,
        bird_y - bird_radius,
        bird_radius * 2,
        bird_radius * 2
    )

    if (
        bird_rect.colliderect(top_pipe)
        or bird_rect.colliderect(bottom_pipe)
    ):
        running = False

    if (
        bird_y - bird_radius < 0
        or bird_y + bird_radius > HEIGHT
    ):
        running = False

    screen.fill(
        (120, 200, 255)
    )

    draw.circle(
        screen,
        (255, 220, 0),
        (bird_x, int(bird_y)),
        bird_radius
    )

    draw.rect(
        screen,
        (40, 180, 70),
        top_pipe
    )

    draw.rect(
        screen,
        (40, 180, 70),
        bottom_pipe
    )

    score_text = game_font.render(
        f"Score: {score}",
        True,
        (255, 255, 255)
    )

    data_text = game_font.render(
        f"Rows: {collector.step}",
        True,
        (255, 255, 255)
    )

    screen.blit(
        score_text,
        (20, 20)
    )

    screen.blit(
        data_text,
        (20, 55)
    )

    display.update()


quit()
