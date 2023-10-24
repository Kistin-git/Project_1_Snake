import pygame
from InputHandler import InputHandler

def test_input_handler_get_direction_arrow_keys():
    size = 10

    # Эмулируем событие нажатия стрелки вверх
    events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)]
    direction = InputHandler.get_direction(events, [0, 0], size)
    assert direction == [0, -size]

    # Эмулируем событие нажатия стрелки вниз
    events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)]
    direction = InputHandler.get_direction(events, [0, 0], size)
    assert direction == [0, size]

    # ... и так далее для других стрелок

def test_input_handler_get_direction_wasd_keys():
    size = 10

    # Эмулируем событие нажатия W
    events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w)]
    direction = InputHandler.get_direction(events, [0, 0], size)
    assert direction == [0, -size]

    # Эмулируем событие нажатия S
    events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s)]
    direction = InputHandler.get_direction(events, [0, 0], size)
    assert direction == [0, size]

    # ... и так далее для других букв

def test_input_handler_get_direction_no_change():
    size = 10
    current_direction = [0, size]

    # Передаем пустой список событий
    events = []
    direction = InputHandler.get_direction(events, current_direction, size)
    assert direction == current_direction

    # Эмулируем событие нажатия любой другой клавиши (не стрелки или WASD)
    events = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]
    direction = InputHandler.get_direction(events, current_direction, size)
    assert direction == current_direction
