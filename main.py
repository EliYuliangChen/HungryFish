import pygame
import random
from object import Object
from fish import Fish, SmallFish, Bass, Shark, Whale
from player import Player

if __name__ == "__main__":
    pygame.init()

    screen_width = 1600
    screen_height = 1200
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Example")

    player = Player(screen_width // 2, screen_height // 2, 'fishSize1.png')
    objects = []

    # for _ in range(4):
    #     object_type = random.choice([SmallFish])  # 添加其他对象类型
    #     x = random.choice([0, screen_width])
    #     new_object = object_type(
    #         x,
    #         random.randint(0, screen_height),
    #         screen_width, 
    #         screen_height
    #     )
    #     objects.append(new_object)

    fish_choices = [SmallFish, Bass, Shark, Whale]  # Available fish types
    if player.size <= 1:
        object_type = random.choices(fish_choices, weights=[0.5, 0.3, 0.1, 0.1], k=1)[0]
    elif player.size <= 2:
        object_type = random.choices(fish_choices, weights=[0.4, 0.4, 0.1, 0.1], k=1)[0]
    elif player.size <= 3:
        object_type = random.choices(fish_choices, weights=[0.2, 0.3, 0.3, 0.2], k=1)[0]
    else:
        object_type = random.choices(fish_choices, weights=[0.1, 0.2, 0.5, 0.2], k=1)[0]

    font = pygame.font.Font(None, 36)  # 创建字体对象
    game_over_text = font.render("GameOver", True, (255, 0, 0))  # 创建 "GameOver" 文本
    ocean_image = pygame.image.load('ocean.png')  # Load the ocean image
    ocean_image = pygame.transform.scale(ocean_image, (screen_width, screen_height))  # Scale the background image to fit the screen
    sand_image = pygame.image.load('sand.png')  # Load the sand image
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

        player.update()
        player.update_size()
        
        for obj in objects:
            obj.update()

            if pygame.Rect(player.x, player.y, player.get_width(), player.get_height()).colliderect(
                pygame.Rect(obj.x, obj.y, obj.get_width(), obj.get_height())
            ):
                if isinstance(obj, Fish):
                    player.eat(obj)
                    if not player.is_game_over:
                        objects.remove(obj)

            obj.draw(screen)

        player.draw(screen)
        
        score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))  # Update the score text
        screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))  # 在屏幕右上角绘制分数文本

        if player.is_game_over:
        # 在屏幕中央绘制 "GameOver" 文本
            screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
        
        # 逐渐生成小鱼
        time_since_last_fish += clock.get_time()
        if time_since_last_fish >= fish_generation_interval:
            # object_type = random.choice([SmallFish, Bass, Shark, Whale])
            x = random.choice([0, screen_width])
            new_object = object_type(
                x,
                random.randint(int(screen_height / 7), int(screen_height * 6 / 7)),
                screen_width, 
                screen_height
            )
            objects.append(new_object)
            time_since_last_fish = 0  # 重置时间
        
        pygame.display.flip()
        clock.tick(60)  # 控制帧率

    pygame.quit()