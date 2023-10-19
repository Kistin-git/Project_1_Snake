import pygame
from GameManager import GameManager

def main():
    """Главная функция, инициализирующая и запускающая игру."""
    pygame.init()

    screen_width = 800
    screen_height = 600
    snake_size = 20
    block_size = 20

    game_manager = GameManager(screen_width, screen_height, snake_size, block_size)
    game_manager.run_game()

    pygame.quit()


if __name__ == "__main__":
    main()
