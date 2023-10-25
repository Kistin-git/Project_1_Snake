import sys

import pygame

from ColorChangeScreen import ColorChangeScreen
from Food import Food
from InputHandler import InputHandler
from LevelEditor import LevelEditor
from Menu import Menu
from Snake import Snake


class GameManager:
    def __init__(self, screen_width, screen_height, snake_size, block_size):
        """Инициализирует начальное состояние игры."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_game_active = False
        self.current_level = 1
        self.menu = Menu(self.screen_width, self.screen_height)
        self.snake_size = snake_size
        self.block_size = block_size
        self.background_image = pygame.image.load('images/background.png')
        self.obstacle_image = pygame.transform.scale(self.background_image, (self.block_size, self.block_size))
        self.start_time = pygame.time.get_ticks()
        self.display_info = False
        self.show_leaderboard = False
        self.waiting_for_name_input = False
        self.snake_speed = 5
        self.clock = pygame.time.Clock()
        snake = Snake(snake_size)
        self.color_change_screen = ColorChangeScreen(self.screen_width, self.screen_height, snake)
        self.current_screen = "menu"

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')

        self.snake = Snake(snake_size)
        self.level_editor = LevelEditor(self.block_size, "levels/empty.txt")
        self.food = Food(screen_width, screen_height, snake_size, self.level_editor)

        self.input_handler = InputHandler()

    def loop_boundary(self):
        """Обрабатывает прохождение границ экрана."""
        head_position = self.snake.get_head_position()
        if head_position[0] < 0:
            self.snake.segments[0][0] = self.screen_width - self.snake_size
        elif head_position[0] >= self.screen_width:
            self.snake.segments[0][0] = 0
        if head_position[1] < 0:
            self.snake.segments[0][1] = self.screen_height - self.snake_size
        elif head_position[1] >= self.screen_height:
            self.snake.segments[0][1] = 0

    def check_collision_with_food(self):
        """Проверяет столкновение головы змеи с едой."""
        head_position = self.snake.get_head_position()
        head_rect = pygame.Rect(head_position[0], head_position[1], self.snake_size, self.snake_size)
        food_rect = pygame.Rect(self.food.position[0], self.food.position[1], self.food.size, self.food.size)

        return head_rect.colliderect(food_rect)

    def check_collision_with_self(self):
        """Проверяет столкновение головы змеи с самой собой."""
        head_position = self.snake.get_head_position()
        for segment in self.snake.segments[1:]:
            if segment == head_position:
                return True
        return False

    def display_game_info(self, surface):
        """Отображает информацию об игре, такую как время и длина змеи."""
        font = pygame.font.Font(None, 36)

        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60

        time_string = f"Time: {minutes}:{seconds:02}"
        time_surface = font.render(time_string, True, (0, 0, 0))

        snake_length_string = f"Snake Length: {len(self.snake.segments)}"
        length_surface = font.render(snake_length_string, True, (0, 0, 0))

        surface.blit(time_surface, (10, 10))
        surface.blit(length_surface, (10, 50))

        level_text = font.render(f"Level: {self.current_level}", True, (0, 0, 0))
        surface.blit(level_text, (10, 30))

    def ask_player_name(self):
        """Запрашивает у игрока его имя для сохранения результата."""
        input_box = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2, 140, 30)
        color_inactive = pygame.Color('lightskyblue3')
        color = color_inactive
        text = ''
        font = pygame.font.Font(None, 32)
        instructions_font = pygame.font.Font(None, 24)

        instructions = [
            "Use WASD or ARROWS to control snake",
            "Press ENTER when you entered your name.",
            "During the game, press 'I' to see your statistics."
        ]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                active = True
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            return text
                        if event.key == pygame.K_ESCAPE:
                            return None
                        if event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            self.screen.fill((30, 30, 30))

            for idx, instruction in enumerate(instructions):
                inst_surface = instructions_font.render(instruction, True, (200, 200, 200))
                self.screen.blit(inst_surface, (self.screen_width // 2 - inst_surface.get_width() // 2,
                                                self.screen_height // 2 - 80 + idx * 25))

            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.screen, color, input_box, 2)

            pygame.display.flip()

    @staticmethod
    def save_score(name, snake_length, time_played):
        """Сохраняет или обновляет рекорд игрока в файле."""
        scores = {}

        # Читаем существующие данные и заполняем словарь
        try:
            with open("scores.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        scores[parts[0]] = (int(parts[1]), float(parts[2]))
        except FileNotFoundError:
            pass  # Файл еще не создан, пропускаем чтение

        # Обновляем данные для текущего игрока
        scores[name] = (snake_length, time_played)

        # Перезаписываем файл с обновленными данными
        with open("scores.txt", "w") as file:
            for name, (snake_length, time_played) in scores.items():
                file.write(f"{name},{snake_length},{time_played}\n")

    @staticmethod
    def get_top_scores():
        """
        Получает пять лучших результатов игры из файла с результатами.

        Returns:
            list: Список из пяти лучших результатов игры.
        """
        try:
            with open("scores.txt", "r") as f:
                scores = [line.strip().split(",") for line in f.readlines()]

                for score in scores:
                    score[1] = int(score[1])
                    score[2] = float(score[2]) // 1

                sorted_scores = sorted(scores, key=lambda x: (-x[1], x[2]))

                return sorted_scores[:5]
        except FileNotFoundError:
            return []

    def display_leaderboard(self):
        """
        Отображает лидерборд на экране.
        """
        self.show_leaderboard = True

        while self.show_leaderboard:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button_rect = pygame.Rect((self.screen_width - 200) // 2, self.screen_height - 100, 200, 50)
                    if button_rect.collidepoint(event.pos):
                        self.show_leaderboard = False
                        return

            self.draw_leaderboard()
            pygame.display.flip()

    def draw_leaderboard(self):
        """
        Рисует лидерборд на экране, включая заголовок и список лучших результатов.
        """
        self.screen.fill((0, 0, 0))

        font = pygame.font.Font(None, 74)
        title = font.render("Leaderboard", 1, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 50))

        font = pygame.font.Font(None, 36)
        top_scores = self.get_top_scores()
        for index, (name, level, time) in enumerate(top_scores):
            text = f"{name} - Level {level} in {time}s"
            score_text = font.render(text, 1, (255, 255, 255))
            self.screen.blit(score_text, (self.screen_width // 2 - score_text.get_width() // 2, 150 + index * 40))

        button_rect = pygame.Rect((self.screen_width - 200) // 2, self.screen_height - 100, 200, 50)
        pygame.draw.rect(self.screen, (0, 128, 0), button_rect)
        button_text = font.render("Return", 1, (255, 255, 255))
        self.screen.blit(button_text, (self.screen_width // 2 - button_text.get_width() // 2, self.screen_height - 85))

    @staticmethod
    def render_winning_text():
        """
        Создает текстовую поверхность с сообщением о победе.

        Returns:
            pygame.Surface: Текстовая поверхность с сообщением о победе.
        """
        font_size = 72
        font = pygame.font.SysFont(None, font_size)
        text_surface = font.render("You Won!", True, (255, 0, 0))
        return text_surface

    def get_centered_position(self, surface):
        """
        Получает координаты, которые центрируют переданную поверхность на экране.

        Args:
            surface (pygame.Surface): Поверхность, которую необходимо центрировать.

        Returns:
            tuple: Координаты (x, y), чтобы центрировать поверхность на экране.
        """
        screen_width, screen_height = self.screen.get_size()
        text_width, text_height = surface.get_size()

        center_x = (screen_width - text_width) // 2
        center_y = (screen_height - text_height) // 2

        return center_x, center_y

    def next_level(self):
        """
        Переходит на следующий уровень игры, обновляя все атрибуты в соответствии с новым уровнем.
        """
        self.level_editor.current_level_index += 1
        if self.level_editor.current_level_index < len(self.level_editor.levels):
            self.level_editor.blocks.clear()
            self.level_editor.load_from_file(self.level_editor.levels[self.level_editor.current_level_index])
            self.snake.reset()
            self.food.randomize_position_and_type()
            if self.current_level == 2:
                self.snake_speed = 5
                self.food.randomize_position_and_type()
                self.food.randomize_position_and_type()
                self.food.randomize_position_and_type()
            elif self.current_level == 3:
                self.snake_speed = 6
            elif self.current_level == 4:
                self.snake_speed = 7
            elif self.current_level == 5:
                self.snake_speed = 8
        else:
            self.level_editor.current_level_index = 0

    def default_level(self):
        """
        Сбрасывает игру на начальный уровень и обновляет все атрибуты в соответствии с этим уровнем.
        """
        self.level_editor.current_level_index = 0
        self.level_editor.blocks.clear()
        self.level_editor.load_from_file(self.level_editor.levels[self.level_editor.current_level_index])
        self.snake.reset()
        self.food.randomize_position_and_type()
        self.snake_speed = 5

    def run_game(self):
        """
        Определяет ход основного игрового цикла.
        """
        clock = pygame.time.Clock()
        self.default_level()
        direction = [0, self.block_size]

        while True:

            events = pygame.event.get()
            for event in events:
                if self.waiting_for_name_input:
                    continue
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if not self.is_game_active:
                    self.level_editor.current_level_index = 0
                    self.current_level = 1

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        action = None
                        if self.current_screen == "menu":
                            action = self.menu.check_button_click(event.pos)

                        elif self.current_screen == "color_change":
                            action = self.color_change_screen.check_button_click(event.pos)
                            if action in ["red", "blue", "green"]:
                                self.snake.set_color(action)

                        if action == "play":
                            player_name = self.ask_player_name()
                            if player_name is None:
                                self.current_screen = "menu"
                                continue
                            self.is_game_active = True
                            direction = [0, self.block_size]
                            self.start_time = pygame.time.get_ticks()
                            self.snake.reset()
                            pygame.event.clear()
                            self.food.randomize_position_and_type()
                        elif action == "leaderboard":
                            self.display_leaderboard()
                        elif action == "change color":
                            self.current_screen = "color_change"
                            if action in ["red", "blue", "green"]:
                                self.snake.set_color(action)
                        elif action == "back":
                            self.current_screen = "menu"

                elif self.is_game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_i:
                            self.display_info = not self.display_info
                        direction = self.input_handler.get_direction(events, self.snake.direction, self.snake_size)

            if self.is_game_active:
                if direction:
                    self.snake.change_direction(direction)
                else:
                    direction = [0, self.block_size]

                next_position = [self.snake.get_head_position()[0] + direction[0],
                                 self.snake.get_head_position()[1] + direction[1]]

                tile_width, tile_height = self.obstacle_image.get_size()
                for x in range(0, self.screen_width, tile_width):
                    for y in range(0, self.screen_height, tile_height):
                        self.screen.blit(self.obstacle_image, (x, y))
                self.level_editor.draw(self.screen)
                self.screen.blit(self.background_image, (0, 0))
                self.snake.draw(self.screen, self.snake_size)
                self.food.draw(self.screen)

                if self.level_editor.check_collision(next_position,
                                                     self.snake_size) or self.check_collision_with_self():
                    self.is_game_active = False
                    self.default_level()
                    self.snake.reset()
                    self.level_editor.current_level_index = 0
                    elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
                    self.save_score(player_name, self.current_level, int(elapsed_time))

                self.snake.move()
                self.loop_boundary()

                if self.check_collision_with_food():
                    if self.food.food_type == 'apple':
                        self.snake.grow()
                    elif self.food.food_type == 'pear':
                        self.snake.grow()
                        self.snake.grow()
                    if self.current_level >= len(self.level_editor.levels):
                        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
                        self.save_score(player_name, self.current_level, elapsed_time)
                        self.screen.fill((0, 0, 0))
                        text_surface = self.render_winning_text()
                        text_position = self.get_centered_position(text_surface)
                        self.screen.blit(text_surface, text_position)
                        pygame.display.flip()
                        pygame.time.wait(2500)
                        self.current_screen = "menu"
                        self.level_editor.current_level_index = 0
                        self.is_game_active = False
                        self.default_level()
                        self.snake.reset()
                    if len(self.snake.segments) >= 8:
                        self.current_level += 1
                        direction = [0, self.block_size]
                        self.next_level()
                    self.food.randomize_position_and_type()
                if self.display_info:
                    self.display_game_info(self.screen)
                pygame.display.flip()
                clock.tick(self.snake_speed)

            else:
                if self.show_leaderboard:
                    self.draw_leaderboard()
                elif self.current_screen == "menu":
                    self.menu.draw(self.screen)
                elif self.current_screen == "color_change":
                    self.color_change_screen.draw(self.screen)

                pygame.display.flip()
                clock.tick(30)
