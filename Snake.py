import pygame

class Snake:
    def __init__(self, size):
        """Инициализирует начальное состояние змеи."""
        self.segments = [[100, 100], [80, 100], [60, 100]]
        self.direction = [size, 0]
        self.size = size
        self.snake_images = [
            pygame.transform.scale(pygame.image.load('../pythonProject3/images/snake_green.png'), (size, size)),
            pygame.transform.scale(pygame.image.load('../pythonProject3/images/snake_red.png'), (size, size)),
            pygame.transform.scale(pygame.image.load('../pythonProject3/images/snake_blue.png'), (size, size))
        ]
        self.current_image_index = 0

        self.snake_image = pygame.transform.scale(self.snake_images[0], (size, size))

    def move(self):
        """Перемещает змею в текущем направлении."""
        head_pos = [self.segments[0][0] + self.direction[0], self.segments[0][1] + self.direction[1]]
        self.segments.insert(0, head_pos)
        self.segments.pop()

    def change_direction(self, direction):
        """Изменяет направление движения змеи, если это возможно."""
        if (direction[0] == -self.direction[0] and direction[1] == self.direction[1]) or \
                (direction[1] == -self.direction[1] and direction[0] == self.direction[0]):
            return
        self.direction = direction

    def grow(self):
        """Увеличивает размер змеи, добавляя сегмент."""
        tail_direction = [self.segments[-2][0] - self.segments[-1][0], self.segments[-2][1] - self.segments[-1][1]]

        new_tail_pos = [self.segments[-1][0] - tail_direction[0], self.segments[-1][1] - tail_direction[1]]

        self.segments.append(new_tail_pos)

    def get_head_position(self):
        """Возвращает позицию головы змеи."""
        return self.segments[0]

    def get_size(self):
        """Возвращает размер одного сегмента змеи."""
        return self.size

    def draw(self, surface, snake_size):
        """Отображает змею на экране."""
        for segment in self.segments:
            surface.blit(self.snake_image, (segment[0], segment[1]))

    def set_color(self, color):
        """Устанавливает цвет змеи."""
        color_mappings = {
            "green": 0,
            "red": 1,
            "blue": 2
        }

        if color in color_mappings:
            self.current_image_index = color_mappings[color]
            self.snake_image = self.snake_images[self.current_image_index]

    def reset(self):
        """Сбросить змею в начальное состояние."""
        self.segments = [[100, 100], [80, 100], [60, 100]]
        self.direction = [self.size, 0]


