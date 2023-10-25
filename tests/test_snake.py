import pygame
from unittest.mock import patch, MagicMock
from Snake import Snake  # Замените your_module_name на имя вашего модуля

# Инициализация pygame для тестовых нужд
pygame.init()

# Мокаем загрузку изображения, чтобы не тратить ресурсы на реальную загрузку
mock_image = MagicMock()
mock_image.get_width.return_value = 20
mock_image.get_height.return_value = 20

@patch('pygame.image.load', return_value=mock_image)
@patch('pygame.transform.scale', return_value=mock_image)
def test_snake_move(mock_load, mock_scale):
    snake = Snake(20)
    initial_head = snake.get_head_position()

    snake.move()
    new_head = snake.get_head_position()

    assert new_head == [initial_head[0] + 20, initial_head[1]]

@patch('pygame.image.load', return_value=mock_image)
@patch('pygame.transform.scale', return_value=mock_image)
def test_snake_grow(mock_load, mock_scale):
    snake = Snake(20)
    initial_length = len(snake.segments)

    snake.grow()
    assert len(snake.segments) == initial_length + 1

@patch('pygame.image.load', return_value=mock_image)
@patch('pygame.transform.scale', return_value=mock_image)
def test_snake_set_color_green(mock_load, mock_scale):
    snake = Snake(20)
    snake.set_color('green')
    assert snake.snake_image == mock_image

@patch('pygame.image.load', return_value=mock_image)
@patch('pygame.transform.scale', return_value=mock_image)
def test_snake_reset(mock_load, mock_scale):
    snake = Snake(20)
    snake.move()
    snake.grow()
    snake.change_direction([-20, 0])
    snake.set_color('red')

    snake.reset()

    assert snake.get_head_position() == [100, 100]
    assert len(snake.segments) == 3
    assert snake.direction == [20, 0]
    assert snake.snake_image == mock_image
