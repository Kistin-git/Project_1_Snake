from unittest.mock import patch, MagicMock, mock_open
from GameManager import GameManager  # Замените `your_module_name` на имя вашего модуля

# Замокаем необходимые функции из pygame
mock_image = MagicMock()
mock_image.get_width.return_value = 20
mock_image.get_height.return_value = 20

m_open = mock_open()

@patch('pygame.font.Font', return_value=MagicMock())
@patch('pygame.image.load', return_value=mock_image)
@patch('pygame.transform.scale', return_value=mock_image)
@patch('pygame.display.set_mode', return_value=MagicMock())
@patch('pygame.display.flip', return_value=None)
@patch('pygame.display.update', return_value=None)
@patch('builtins.open', m_open)
def test_check_collision_with_food_true(mock_font, mock_load, mock_scale, mock_set_mode, mock_flip, mock_update):
    gm = GameManager(800, 600, 20, 20)
    gm.snake.segments[0] = [-20, 100]
    gm.loop_boundary()
    assert gm.snake.get_head_position() == [780, 100]

@patch('pygame.font.Font', return_value=MagicMock())
@patch('pygame.image.load', return_value=mock_image)
@patch('pygame.transform.scale', return_value=mock_image)
@patch('pygame.display.set_mode', return_value=MagicMock())
@patch('pygame.display.flip', return_value=None)
@patch('pygame.display.update', return_value=None)
@patch('builtins.open', m_open)
def test_check_collision_with_food_true(mock_font, mock_load, mock_scale, mock_set_mode, mock_flip, mock_update):
    gm = GameManager(800, 600, 20, 20)
    gm.snake.segments[0] = [100, 100]
    gm.food.position = [100, 100]
    assert gm.check_collision_with_food()
@patch('pygame.font.Font', return_value=MagicMock())
@patch('pygame.image.load', return_value=mock_image)
@patch('pygame.transform.scale', return_value=mock_image)
@patch('pygame.display.set_mode', return_value=MagicMock())
@patch('pygame.display.flip', return_value=None)
@patch('pygame.display.update', return_value=None)
@patch('builtins.open', m_open)
def test_check_collision_with_food_true(mock_font, mock_load, mock_scale, mock_set_mode, mock_flip, mock_update):
    gm = GameManager(800, 600, 20, 20)
    gm.snake.segments = [[100, 100], [120, 100], [140, 100], [100, 100]]
    assert gm.check_collision_with_self()
