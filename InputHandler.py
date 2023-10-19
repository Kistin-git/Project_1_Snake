import pygame


class InputHandler:
    """Обработчик пользовательского ввода для управления направлением движения.

    Этот класс предоставляет статический метод для определения направления движения на основе событий, полученных от pygame.

    Methods:
        get_direction(events, current_direction, size): Определяет направление движения на основе ввода пользователя.
    """

    @staticmethod
    def get_direction(events, current_direction, size):
        """Определяет направление движения на основе ввода пользователя.

        Этот метод принимает текущее направление и проверяет события ввода от pygame, чтобы определить,
        следует ли изменить направление. Направления определяются на основе нажатий клавиш стрелок или WASD.

        Args:
            events (list): Список событий, полученных от pygame.
            current_direction (list): Текущее направление движения в формате [x, y].
            size (int): Размер, который используется для определения шага движения.

        Returns:
            list: Новое направление движения в формате [x, y]. Если направление не изменяется, возвращается current_direction.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    return [0, -size]
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    return [0, size]
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    return [-size, 0]
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    return [size, 0]

        return current_direction
