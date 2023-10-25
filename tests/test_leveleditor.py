import unittest
from unittest.mock import patch, MagicMock
from LevelEditor import LevelEditor
import pygame

sample_level_content = """(0,0)
(10,10)
(20,20)-(30,30)
"""

class TestLevelEditor(unittest.TestCase):

    def mock_pygame_image_load(self, *args, **kwargs):
        # Создаем настоящий pygame.Surface объект
        surface = pygame.Surface((10, 10))
        return surface

    @patch('pygame.image.load', side_effect=mock_pygame_image_load)
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=sample_level_content)
    def setUp(self, mock_open, mock_pygame):
        self.editor = LevelEditor(10, "dummy_file.txt")

    def test_init(self):
        self.assertEqual(self.editor.block_size, 10)
        self.assertIsNotNone(self.editor.blocks)
        self.assertIsNotNone(self.editor.levels)
        self.assertEqual(self.editor.current_level_index, 0)

    def test_load_from_file(self):
        self.assertIn([0,0], self.editor.blocks)
        self.assertIn([10,10], self.editor.blocks)
        self.assertIn([20,20], self.editor.blocks)

    @patch('pygame.Rect')
    def test_check_collision_true(self, MockRect):
        MockRect.side_effect = [MagicMock(colliderect=MagicMock(return_value=True)), MagicMock()]
        self.assertTrue(self.editor.check_collision([0, 0], 10))

    @patch('pygame.Surface')
    def test_draw(self, MockSurface):
        self.editor.draw(MockSurface())
        # Assert the number of times the image has been drawn to the surface.
        self.assertEqual(MockSurface().blit.call_count, len(self.editor.blocks))

if __name__ == '__main__':
    unittest.main()
