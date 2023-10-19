import pygame


class LevelEditor:
    """Редактор уровней для загрузки и отображения препятствий на игровом поле.

    Данный класс позволяет загружать определенные уровни препятствий из файлов и отображать их на игровом поле.
    Также предоставляется функция для проверки столкновений с препятствиями.

    Attributes:
        block_size (int): Размер каждого блока препятствия на поле.
        blocks (list): Список блоков препятствий, каждый из которых представлен координатами [x, y].
        levels (list): Список доступных файлов уровней.
        current_level_index (int): Индекс текущего уровня в списке levels.
        obstacle_image (pygame.Surface): Изображение препятствия.

    Methods:
        load_from_file(filename): Загружает уровень из файла.
        check_collision(pos, size): Проверяет столкновение с препятствиями.
        draw(surface): Рисует препятствия на заданной поверхности.
    """
    def __init__(self, block_size, filename=None):
        self.block_size = block_size
        self.blocks = []
        self.levels = ["levels/level1.txt", "levels/level2.txt", "levels/level3.txt", "levels/level4.txt", "levels/level5.txt"]
        self.current_level_index = 0
        self.obstacle_image = pygame.image.load('../pythonProject3/images/obstacle_tile.png')
        self.obstacle_image = pygame.transform.scale(self.obstacle_image, (self.block_size, self.block_size))

        if filename or self.current_level_index == 0:
            self.load_from_file(filename)

    def load_from_file(self, filename):
        """Загружает уровень препятствий из файла.

        Args:
            filename (str): Путь к файлу уровня.

        Note:
            Формат файла: каждая строка представляет собой координаты блока в формате (x, y) или диапазон в формате (start_x, start_y)-(end_x, end_y).
        """
        self.blocks.clear()
        with open(filename, 'r') as file:
            for line in file.readlines():
                line = line.strip()

                if '-' in line:
                    start, end = line.split('-')
                    start_x, start_y = map(int, start.strip('()').split(','))
                    end_x, end_y = map(int, end.strip('()').split(','))

                    for x in range(start_x, end_x + 1, self.block_size):
                        for y in range(start_y, end_y + 1, self.block_size):
                            self.blocks.append([x, y])
                else:
                    x, y = map(int, line.strip('()').split(','))
                    self.blocks.append([x, y])

    def check_collision(self, pos, size):
        """Проверяет столкновение объекта с заданными координатами и размером с препятствиями на уровне.

        Args:
            pos (list): Координаты объекта в формате [x, y].
            size (int): Размер объекта.

        Returns:
            bool: True, если происходит столкновение, иначе False.
        """
        head_rect = pygame.Rect(pos[0], pos[1], size, size)
        for block in self.blocks:
            block_rect = pygame.Rect(block[0], block[1], self.block_size, self.block_size)
            if head_rect.colliderect(block_rect):
                return True
        return False

    def draw(self, surface):
        """Отображает препятствия на заданной поверхности.

        Args:
            surface (pygame.Surface): Поверхность для рисования.
        """
        for block in self.blocks:
            surface.blit(self.obstacle_image, (block[0], block[1]))
