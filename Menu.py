import pygame

class Menu:
    def __init__(self, screen_width, screen_height):
        """
        Инициализация главного меню игры.

        :param screen_width: Ширина экрана.
        :param screen_height: Высота экрана.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 60)
        self.btn_color = (0, 128, 0)
        self.text_color = (255, 255, 255)
        self.buttons = [
            {"label": "Play Game", "action": "play"},
            {"label": "Leaderboard", "action": "leaderboard"},
            {"label": "Change color", "action": "change color"}
        ]

    def draw(self, screen):
        """
        Рисует главное меню на экране.

        :param screen: Экран для отображения.
        """
        screen.fill((0, 0, 0))

        button_width, button_height = 300, 100
        for index, button in enumerate(self.buttons):
            button_x = (self.screen_width - button_width) // 2
            button_y = (index * (button_height + 20)) + (self.screen_height - button_height) // 2

            pygame.draw.rect(screen, self.btn_color, (button_x, button_y, button_width, button_height))

            label = self.font.render(button["label"], 1, self.text_color)
            screen.blit(label, (self.screen_width // 2 - label.get_width() // 2,
                                button_y + button_height // 2 - label.get_height() // 2))

    def check_button_click(self, pos):
        """
        Проверяет, была ли нажата какая-либо кнопка в меню.

        :param pos: Координаты (x, y) нажатия мыши.
        :return: Действие, связанное с кнопкой, если была нажата кнопка, иначе None.
        """
        button_width, button_height = 300, 100
        for index, button in enumerate(self.buttons):
            button_x = (self.screen_width - button_width) // 2
            button_y = (index * (button_height + 20)) + (self.screen_height - button_height) // 2
            if button_x <= pos[0] <= button_x + button_width and button_y <= pos[1] <= button_y + button_height:
                return button["action"]
        return None
