import random
import pygame


class Food:
    """Класс, представляющий еду для змейки."""
    def __init__(self, screen_width, screen_height, size, level_editor):
        """Инициализация объекта Food.

        Args:
            screen_width (int): Ширина экрана.
            screen_height (int): Высота экрана.
            size (int): Размер единицы еды.
            level_editor (object): Объект редактора уровня для проверки столкновений.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = size
        self.position = []
        self.food_type = None
        self.level_editor = level_editor
        self.randomize_position_and_type()
        self.apple_image = pygame.image.load('../pythonProject3/images/apple.png')
        self.apple_image = pygame.transform.scale(self.apple_image, (self.size, self.size))
        self.pear_image = pygame.image.load('../pythonProject3/images/pear.png')
        self.pear_image = pygame.transform.scale(self.pear_image, (self.size, self.size))

    def randomize_position_and_type(self):
        """Выбирает случайное местоположение и тип еды, убедившись, что она не сталкивается со стеной."""
        while True:
            x = random.randint(0, (self.screen_width - self.size) // self.size) * self.size
            y = random.randint(0, (self.screen_height - self.size) // self.size) * self.size
            self.position = [x, y]
            if not self.level_editor.check_collision(self.position, self.size):
                break

        self.food_type = random.choice(['apple', 'pear'])

    def draw(self, surface):
        """Рисует еду на заданной поверхности.

        Args:
            surface (Surface): Поверхность pygame, на которой будет отрисована еда.
        """
        if self.food_type == 'apple':
            surface.blit(self.apple_image, (self.position[0], self.position[1]))
        else:
            surface.blit(self.pear_image, (self.position[0], self.position[1]))
