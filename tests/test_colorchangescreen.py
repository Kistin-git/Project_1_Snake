from unittest.mock import Mock, patch
from ColorChangeScreen import ColorChangeScreen

@patch("ColorChangeScreen.pygame.font.Font", return_value=Mock(render=Mock(return_value=Mock(get_width=Mock(return_value=50), get_height=Mock(return_value=20)))))
@patch("ColorChangeScreen.pygame.draw.rect", return_value=None)
def test_color_change_screen_init(mock_draw_rect, mock_font):
    snake = Mock()
    screen_width = 800
    screen_height = 600
    screen = ColorChangeScreen(screen_width, screen_height, snake)

    assert screen.screen_width == screen_width
    assert screen.screen_height == screen_height
    assert screen.snake == snake
    mock_font.assert_called_once_with(None, 60)

@patch("ColorChangeScreen.pygame.font.Font", return_value=Mock(render=Mock(return_value=Mock(get_width=Mock(return_value=50), get_height=Mock(return_value=20)))))
@patch("ColorChangeScreen.pygame.draw.rect", return_value=None)
def test_color_change_screen_draw(mock_draw_rect, mock_font):
    snake = Mock()
    screen_width = 800
    screen_height = 600
    screen_obj = Mock()
    color_screen = ColorChangeScreen(screen_width, screen_height, snake)

    color_screen.draw(screen_obj)

    screen_obj.fill.assert_called_once_with((0, 0, 0))
    assert mock_draw_rect.call_count == 4
    assert mock_font.return_value.render.call_count == 4
    assert screen_obj.blit.call_count == 4

@patch("ColorChangeScreen.pygame.font.Font", return_value=Mock(render=Mock(return_value=Mock(get_width=Mock(return_value=50), get_height=Mock(return_value=20)))))
@patch("ColorChangeScreen.pygame.draw.rect", return_value=None)
def test_color_change_screen_check_button_click(mock_draw_rect, mock_font):
    snake = Mock()
    screen_width = 800
    screen_height = 600
    color_screen = ColorChangeScreen(screen_width, screen_height, snake)

    result = color_screen.check_button_click((100, screen_height - 50))
    assert result == "back"

    result = color_screen.check_button_click((90, 75))
    assert result == "red"

    result = color_screen.check_button_click((340, 75))
    assert result == "blue"

    result = color_screen.check_button_click((590, 75))
    assert result == "green"

    result = color_screen.check_button_click((screen_width // 2, screen_height // 2 + 25))
    assert result == "change_color"

    result = color_screen.check_button_click((0, 0))
    assert result == None
