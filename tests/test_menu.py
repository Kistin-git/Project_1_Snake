import pygame
import pytest
from Menu import Menu  # Замените your_module_name на имя вашего модуля
pygame.init()
@pytest.fixture
def setup_menu():
    menu = Menu(800, 600)
    return menu

def test_check_button_click_play_game(setup_menu):
    pos = (400, 250)  # координаты, где находится кнопка "Play Game"
    assert setup_menu.check_button_click(pos) == "play"

def test_check_button_click_leaderboard(setup_menu):
    pos = (400, 370)  # координаты, где находится кнопка "Leaderboard"
    assert setup_menu.check_button_click(pos) == "leaderboard"

def test_check_button_click_change_color(setup_menu):
    pos = (400, 490)  # координаты, где находится кнопка "Change color"
    assert setup_menu.check_button_click(pos) == "change color"

def test_check_button_click_no_button(setup_menu):
    pos = (100, 100)  # координаты, где нет кнопки
    assert setup_menu.check_button_click(pos) == None
