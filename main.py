import pygame
from levelOne import run_level_one
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 1600
screen_height = 1200

# Colors
WHITE = (255, 255, 255)

# Create the screen and set the caption
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Big Fish Game")

# Load the background image
background_image = pygame.image.load('ocean.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load the button images
start_button = pygame.font.Font(None, 64).render("Start Game", True, WHITE)
exit_button = pygame.font.Font(None, 64).render("Exit Game", True, WHITE)

# Define button dimensions and positions
start_button_rect = start_button.get_rect(center=(screen_width//2, screen_height//2 - 50))
exit_button_rect = exit_button.get_rect(center=(screen_width//2, screen_height//2 + 50))

def level_selection_screen(screen):
    # Colors
    WHITE = (255, 255, 255)

    # Load the background image
    background_image = pygame.image.load('ocean.png')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Load the level button images
    level1_button = pygame.font.Font(None, 64).render("Level 1", True, WHITE)
    # Add more levels here if needed

    # Define button dimensions and positions
    level1_button_rect = level1_button.get_rect(center=(screen_width//2, screen_height//2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if level1_button_rect.collidepoint(event.pos):
                    result = run_level_one()
                    if result == 'main_menu':
                        continue
                # Add more levels here if needed

        # Draw background
        screen.blit(background_image, (0, 0))

        # Draw buttons
        screen.blit(level1_button, level1_button_rect.topleft)

        pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
                selected_level = level_selection_screen(screen)
            elif exit_button_rect.collidepoint(event.pos):
                running = False

    # Draw background
    screen.blit(background_image, (0, 0))

    # Draw buttons
    screen.blit(start_button, start_button_rect.topleft)
    screen.blit(exit_button, exit_button_rect.topleft)

    pygame.display.flip()

pygame.quit()
sys.exit()