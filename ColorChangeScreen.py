import pygame


class ColorChangeScreen:
    """Экран для изменения цвета змейки в игре.

    Этот класс предоставляет интерфейс для выбора цвета змейки и содержит кнопки для этой цели.

    Attributes:
        screen_width (int): Ширина экрана.
        screen_height (int): Высота экрана.
        snake (object): Объект змейки.
        font (Font): Шрифт для рисования текста на кнопках.
        back_btn (dict): Словарь атрибутов для кнопки "Назад".
        change_color_btn (dict): Словарь атрибутов для кнопки "Изменить цвет".
        red_color_btn (dict): Словарь атрибутов для кнопки выбора красного цвета.
        blue_color_btn (dict): Словарь атрибутов для кнопки выбора синего цвета.
        green_color_btn (dict): Словарь атрибутов для кнопки выбора зеленого цвета.
    """
    def __init__(self, screen_width, screen_height, snake):
        """Инициализирует экран для изменения цвета змейки.

        Args:
            screen_width (int): Ширина экрана.
            screen_height (int): Высота экрана.
            snake (object): Объект змейки.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.snake = snake
        self.font = pygame.font.Font(None, 60)
        self.back_btn = {"label": "Back", "x": 50, "y": screen_height - 100, "w": 150, "h": 50}
        self.change_color_btn = {"label": "Change Color", "x": screen_width // 2 - 75, "y": screen_height // 2,
                                 "w": 150, "h": 50}
        self.red_color_btn = {"label": "Red", "x": 70, "y": 50, "w": 150, "h": 50, "color": "red"}
        self.blue_color_btn = {"label": "Blue", "x": 320, "y": 50, "w": 150, "h": 50, "color": "blue"}
        self.green_color_btn = {"label": "Green", "x": 570, "y": 50, "w": 150, "h": 50, "color": "green"}

    def draw(self, screen):
        """Отрисовывает экран смены цвета и все его элементы на указанной поверхности.

        Args:
            screen (Surface): Поверхность для отрисовки.
        """
        screen.fill((0, 0, 0))

        for btn in [self.red_color_btn, self.blue_color_btn, self.green_color_btn]:
            pygame.draw.rect(screen, (255 if btn.get("label") == "Red" else 0,
                                      128 if btn.get("label") == "Green" else 0,
                                      255 if btn.get("label") == "Blue" else 0),
                             (btn["x"], btn["y"], btn["w"], btn["h"]))
            label = self.font.render(btn["label"], 1, (255, 255, 255))
            screen.blit(label, (btn["x"] + (btn["w"] - label.get_width()) // 2,
                                btn["y"] + (btn["h"] - label.get_height()) // 2))

        pygame.draw.rect(screen, (0, 128, 0), (self.back_btn["x"], self.back_btn["y"],
                                               self.back_btn["w"], self.back_btn["h"]))
        label = self.font.render(self.back_btn["label"], 1, (255, 255, 255))
        screen.blit(label, (self.back_btn["x"] + (self.back_btn["w"] - label.get_width()) // 2,
                            self.back_btn["y"] + (self.back_btn["h"] - label.get_height()) // 2))

    def check_button_click(self, pos):
        """Проверяет, была ли нажата какая-либо из кнопок.

        Args:
            pos (tuple): Координаты (x, y) места клика.

        Returns:
            str: Возвращает цвет или действие ('back', 'change_color'), если была нажата соответствующая кнопка.
                В противном случае возвращает None.
        """
        if self.back_btn["x"] <= pos[0] <= self.back_btn["x"] + self.back_btn["w"] and \
           self.back_btn["y"] <= pos[1] <= self.back_btn["y"] + self.back_btn["h"]:
            return "back"
        for btn in [self.red_color_btn, self.blue_color_btn, self.green_color_btn]:
            if btn["x"] <= pos[0] <= btn["x"] + btn["w"] and \
                    btn["y"] <= pos[1] <= btn["y"] + btn["h"]:
                return btn["color"]
        if self.change_color_btn["x"] <= pos[0] <= self.change_color_btn["x"] + self.change_color_btn["w"] and \
                self.change_color_btn["y"] <= pos[1] <= self.change_color_btn["y"] + self.change_color_btn["h"]:
            return "change_color"
        return None
