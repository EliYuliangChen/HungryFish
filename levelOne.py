import pygame
import random
from object import Object
from fish import Fish, SmallFish, Bass, Shark, Whale
from player import Player

WHITE = (255, 255, 255)

def run_level_one():
    screen_width = 1600
    screen_height = 1200
    LEFT_SIDE = -50
    RIGHT_SIDE = screen_width + 50

    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Example")

    player = Player(screen_width // 2, screen_height // 2, 'fishSize1.png')
    objects = []
    
    font = pygame.font.Font(None, 36)  # 创建字体对象
    game_over_text = font.render("GameOver", True, (255, 0, 0))
    level_complete_text = font.render("Level Completed!", True, (0, 255, 0))
    next_level_button = pygame.font.Font(None, 50).render("Next Level", True, WHITE)
    retry_button = pygame.font.Font(None, 50).render("Try Again", True, WHITE)
    main_menu_button = pygame.font.Font(None, 50).render("Back to Main", True, WHITE)
    next_level_button_rect = next_level_button.get_rect(center=(screen_width//2, screen_height*3/4 + 50))
    retry_button_rect = retry_button.get_rect(center=(screen_width//2, screen_height*3/4 + 50))
    main_menu_button_rect = main_menu_button.get_rect(center=(screen_width//2, screen_height*3/4 + 100))
    level_complete = False

    ocean_image = pygame.image.load('ocean.png')  # Load the ocean image
    ocean_image = pygame.transform.scale(ocean_image, (screen_width, screen_height))  # Scale the background image to fit the screen
    sand_image = pygame.image.load('sand.png')  # Load the sand image
    sand_image = pygame.transform.scale(sand_image, (screen_width, int(screen_height*0.45)))
    # sand_image = pygame.transform.scale(sand_image, screen_width)

    time_since_last_fish = 0  # 记录自上一个小鱼生成以来的时间
    fish_generation_interval = random.randint(600, 1200)  # 生成小鱼的时间间隔，单位为毫秒


    running = True
    clock = pygame.time.Clock()  # 创建时钟实例
    while running:
        events = pygame.event.get()  # 获取事件列表
        screen.fill((0, 0, 0, 0))
        screen.blit(ocean_image, (0, 0))  # Draw the ocean image
        screen.blit(sand_image, (0, 0))  # Draw the sand image

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 鼠标左键按下
                player.accelerate()
        # Limit the player's movement within the desired range
        if player.y < screen_height / 4:
            player.y = screen_height / 4
        elif player.y > screen_height * 6 / 7:
            player.y = screen_height * 6 / 7
        player.update()
        # player.update_size()
        
        # 逐渐生成小鱼
        time_since_last_fish += clock.get_time()
        if time_since_last_fish >= fish_generation_interval:
            fish_choices = [SmallFish, Bass, Shark, Whale]  # Available fish types
            if player.size <= 1:
                object_type = random.choices(fish_choices, weights=[0.9, 0.1, 0, 0], k=1)[0]
            elif player.size <= 2:
                object_type = random.choices(fish_choices, weights=[0.4, 0.4, 0.2, 0], k=1)[0]
            elif player.size <= 3:
                object_type = random.choices(fish_choices, weights=[0.2, 0.3, 0.3, 0.2], k=1)[0]
            else:
                object_type = random.choices(fish_choices, weights=[0, 0.1, 0.1, 0.8], k=1)[0]

            
            x = random.choice([LEFT_SIDE, RIGHT_SIDE])
            new_object = object_type(
                x,
                random.randint(int(screen_height / 4), int(screen_height * 6 / 7)),
                screen_width, 
                screen_height
            )
            objects.append(new_object)
            time_since_last_fish = 0  # 重置时间
        
        for obj in objects:
            obj.update()

            if not obj.alive:
                objects.remove(obj)

            if pygame.Rect(player.x, player.y, player.get_width(), player.get_height()).colliderect(
                pygame.Rect(obj.x, obj.y, obj.get_width(), obj.get_height())
            ):
                player.eat(obj)
                if player.is_game_over:
                    # objects = []  # Clear all fish
                    # screen.blit(retry_button, retry_button_rect.topleft)
                    # screen.blit(main_menu_button, main_menu_button_rect.topleft)
                    break
                else :
                    objects.remove(obj)

            obj.draw(screen)

        player.draw(screen)
        # Check if player score has reached 50 and set level_complete to True
        if player.is_game_over:
            objects = []  # Clear all fish
            screen.blit(retry_button, retry_button_rect.topleft)
            screen.blit(main_menu_button, main_menu_button_rect.topleft)

        if player.score >= 50:
            level_complete = True
            objects = []  # Clear all fish

        if level_complete:
            screen.blit(level_complete_text, (screen_width // 2 - level_complete_text.get_width() // 2, screen_height * 3/4 - level_complete_text.get_height() // 2))
            screen.blit(next_level_button, next_level_button_rect.topleft)
            screen.blit(main_menu_button, main_menu_button_rect.topleft)

            # Make the player static
            player.vx = 0
            player.vy = 0
                
        score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))  # Update the score text
        screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))  # 在屏幕右上角绘制分数文本

        pygame.display.flip()
        for event in events:
            if player.is_game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button_rect.collidepoint(event.pos):
                        run_level_one()
                    elif main_menu_button_rect.collidepoint(event.pos):
                        return 'main_menu'
            if level_complete:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if next_level_button_rect.collidepoint(event.pos):
                        # TODO: Transition to next level (currently, it will restart level one)
                        run_level_one()
                    elif main_menu_button_rect.collidepoint(event.pos):
                        return 'main_menu'
        clock.tick(60)  # 控制帧率

    # pygame.quit()