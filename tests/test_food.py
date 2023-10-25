import pytest
from unittest.mock import patch, Mock
from Food import Food

@pytest.fixture
def mock_level_editor():
    mock = Mock()
    mock.check_collision.return_value = False
    return mock

@pytest.fixture
def mock_image():
    return Mock()


@patch('pygame.transform.scale', side_effect=lambda img, size: img)
@patch('pygame.image.load')
@patch('random.choice', return_value='apple')
@patch('random.randint', side_effect=[5, 10])  # Вернем к предыдущему значению
  # Учитываем размер блока
def test_randomize_position_and_type(mock_randint, mock_choice, mock_image_load, mock_scale, mock_image, mock_level_editor):
    mock_image_load.return_value = mock_image

    screen_width = 600
    screen_height = 600
    block_size = 20

    food = Food(screen_width, screen_height, block_size, mock_level_editor)

    assert food.position == [5*20, 10*20]
    assert food.food_type == 'apple'
    mock_level_editor.check_collision.assert_called_with([5*20, 10*20], block_size)

if __name__ == "__main__":
    pytest.main()
