import pygame
import runpy
from settings import *
from orc import Orc
from swordsman import Swordsman
from item import Item
from healer import Healer
from tank import Tank
from mage import Mage
from random import randrange, randint
from os import system, name, remove, path

if path.isfile('save.txt'):
    first_time = 0
else:
    first_time = 1

fight_lines = []
pygame.init()
clock = pygame.time.Clock()


def reset_frame():
    WIN.fill(WHITE)
    pygame.display.update()


def fill_screen(color: tuple[int, int, int]):
    WIN.fill(color)
    pygame.display.update()


def print_message(message_text: str):
    message_run = True
    message_font = pygame.font.SysFont('cambodia', 22)
    font = pygame.font.SysFont('cambodia', int(40 / 1.2))
    title_font = pygame.font.SysFont('cambodia', 70)
    message_box_outer = pygame.Rect(300, 200, 300, 200)
    message_box_inner = pygame.Rect(310, 210, 280, 180)
    ok_text = 'OK'
    ok_button_x, ok_button_y = 410, 320
    ok_button_size_x, ok_button_size_y = 80, 50
    ok_button_outer = pygame.Rect(ok_button_x, ok_button_y, ok_button_size_x, ok_button_size_y)
    ok_button_inner = pygame.Rect(ok_button_x + 5, ok_button_y + 5, ok_button_size_x - 10, ok_button_size_y - 10)
    WIN.fill(BLACK, message_box_outer)
    WIN.fill(WHITE, message_box_inner)
    WIN.fill(BLACK, ok_button_outer)
    WIN.fill(WHITE, ok_button_inner)
    rendered = message_font.render(message_text, True, BLACK)
    ok_rendered = font.render(ok_text, True, BLACK)
    WIN.blit(rendered, (325, 250))
    while message_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_button_outer.collidepoint(event.pos):
                    message_run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    message_run = False
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        if ok_button_x <= mouse_pos_x <= ok_button_x + ok_button_size_x and \
                ok_button_y <= mouse_pos_y <= ok_button_y + ok_button_size_y:
            ok_rendered = font.render(ok_text, True, pygame.Color('green'))
        else:
            ok_rendered = font.render(ok_text, True, pygame.Color('black'))
        WIN.blit(ok_rendered, (ok_button_x + 20, ok_button_y + 15))
        pygame.display.update()


def print_fight_lines(lines: list):
    font = pygame.font.SysFont('cambodia', int(40 / 1.2))
    title_font = pygame.font.SysFont('cambodia', 70)
    surface_outer = pygame.Rect(0, 300, 900, 300)
    surface_inner = pygame.Rect(0, 310, 900, 290)
    for i, line in enumerate(lines):
        WIN.fill(BLACK, surface_outer)
        WIN.fill(WHITE, surface_inner)
        current_line_render = (title_font if len(line) < 35 else font).render(line, True, BLACK)
        WIN.blit(current_line_render, (100, 350))
        pygame.display.update()
        print_run = True
        while print_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print_run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        print_run = False
    return 0


def is_crit(crit_chance):
    n = float(randrange(0, 100, 1) / 100)
    if n < crit_chance:
        return True
    else:
        return False


def execute_hero_move(n, move_type, o):
    fight_lines.clear()
    if move_type == 0:
        h.spend_mana(h.get_moves()[n][4])
        damage = int(randrange(h.get_moves()[n][2], h.get_moves()[n][3], 1) * h.get_level_attack_mult() *
                     h.get_attack_mult())
        items = h.get_equipped_items()
        for item in items:
            if item.get_amplifier_type() == 0:
                damage = int(damage + (damage * item.get_amplifier()))
        if is_crit(h.get_crit_chance()):
            damage = int(damage * h.get_crit_mult())
            fight_lines.append("You landed a critical hit!")
        o.take_damage(damage)
        fight_lines.append("You dealt {} damage!".format(damage))
        return True
    elif move_type == 1:
        h.spend_mana(h.get_moves()[n][4])
        healing = int(randrange(h.get_moves()[n][2], h.get_moves()[n][3], 1) * h.get_level_attack_mult())
        items = h.get_equipped_items()
        for item in items:
            if item.get_amplifier_type() == 1:
                healing = int(healing + (healing * item.get_amplifier()))
        h.take_healing(healing)
        fight_lines.append("You healed for {} health!".format(healing))
        return True
    elif move_type == 2:
        h.spend_mana(h.get_moves()[n][4])
        h.focus(n)
        fight_lines.append("You became focused! Your critical hit chance increased!")
        return True
    elif move_type == 3:
        mana = int(randrange(h.get_moves()[n][2], h.get_moves()[n][3], 1))
        items = h.get_equipped_items()
        for item in items:
            if item.get_amplifier_type() == 3:
                mana = int(mana + (mana * item.get_amplifier()))
        h.regen_mana(mana)
        fight_lines.append("You restored {} mana!".format(mana))
        return True
    elif move_type == 4:
        h.spend_mana(h.get_moves()[n][4])
        h.rage(n)
        fight_lines.append("You were consumed by rage! You now deal more damage!")
        return True
    else:
        return False


def execute_orc_move(n, move_type, o):
    fight_lines.clear()
    if move_type == 0:
        o.spend_mana(o.get_moves()[n][4])
        damage = int(randrange(o.get_moves()[n][2], o.get_moves()[n][3], 1) *
                     o.get_level_attack_mult() * o.get_berserk_factor())
        items = h.get_equipped_items()
        for item in items:
            if item.get_amplifier_type() == 2:
                damage -= int(damage * item.get_amplifier())
        h.take_damage(damage)
        fight_lines.append("You took {} damage!".format(damage))
    elif move_type == 1:
        o.spend_mana(o.get_moves()[n][4])
        healing = int(randrange(o.get_moves()[n][2], o.get_moves()[n][3], 1) * o.get_level_attack_mult())
        o.take_healing(healing)
        fight_lines.append("The orc healed for {} health!".format(healing))
    elif move_type == 3:
        mana = int(randrange(o.get_moves()[n][2], o.get_moves()[n][3], 1))
        o.regen_mana(mana)
        fight_lines.append("The orc restored {} mana!".format(mana))
    else:
        fight_lines.append("Unexpected error: Invalid orc move")
        fight_lines.append("The game will now close")
        print_fight_lines(fight_lines)
        pygame.quit()


def draw_button(text: str, font: pygame.font.Font, text_color: tuple[int, int, int],
                outline_color: tuple[int, int, int],
                fill_color: tuple[int, int, int],
                button_x: int, button_y: int,
                button_size_x: int, button_size_y: int):
    button_outer = pygame.Rect(button_x, button_y, button_size_x, button_size_y)
    button_inner = pygame.Rect(button_x + button_size_x / 10,
                               button_y + button_size_y / 10,
                               4 / 5 * button_size_x,
                               4 / 5 * button_size_y)
    WIN.fill(outline_color, button_outer)
    WIN.fill(fill_color, button_inner)
    button_text = font.render(text, True, text_color)
    WIN.blit(button_text, (button_x + button_size_x / (3 if text.__len__() < (8 if button_size_x > 180 else 6) else 5),
                           button_y + button_size_y / 4))
    return button_outer


def draw_healthbar(health: int or float, max_health: int or float, x: int, y: int, size_x: int, size_y: int):
    health_bar_outer = pygame.Rect(x, y, size_x, size_y)
    health_bar_inner = pygame.Rect(int(x + size_x / 55),
                                   int(y + size_y / 10),
                                   int(size_x - 2 * size_x / 55),
                                   int(size_y - 2 * size_y / 10))
    WIN.fill(BLACK, health_bar_outer)
    WIN.fill(WHITE, health_bar_inner)
    percent_health = int(health / max_health * 100)
    if percent_health <= 20:
        color = RED
    elif percent_health <= 40:
        color = YELLOW
    else:
        color = GREEN
    for i in range(1, 100, 1):
        if percent_health >= i:
            current = pygame.Rect(
                int((x + size_x / 22 - (size_x - (size_x / 11)) / 100) + (i * (size_x - (size_x / 11)) / 100)),
                int(y + 1 / 4 * size_y),
                int((size_x - (size_x / 11)) / 100),
                int(size_y / 2))
            WIN.fill(color, current)


def draw_manabar(mana: int or float, max_mana: int or float, x: int, y: int, size_x: int, size_y: int):
    color = BLUE
    health_bar_outer = pygame.Rect(x, y, size_x, size_y)
    health_bar_inner = pygame.Rect(int(x + size_x / 55),
                                   int(y + size_y / 10),
                                   int(size_x - 2 * size_x / 55),
                                   int(size_y - 2 * size_y / 10))
    WIN.fill(BLACK, health_bar_outer)
    WIN.fill(WHITE, health_bar_inner)
    percent_mana = int(mana / max_mana * 100)
    for i in range(1, 100, 1):
        if percent_mana >= i:
            current = pygame.Rect(
                int((x + size_x / 22 - (size_x - (size_x / 11)) / 100) + (i * (size_x - (size_x / 11)) / 100)),
                int(y + 1 / 4 * size_y),
                int((size_x - (size_x / 11)) / 100),
                int(size_y / 2))
            WIN.fill(color, current)


def orc_level_menu():
    pygame.display.set_caption("Choose Orc Level")
    font = pygame.font.SysFont('cambodia', int(40 / 1.2))
    title_font = pygame.font.SysFont('cambodia', 70)
    orc_level_text = 'Please input the orc level:'
    current_level_text = f'Your level is {h.get_level()}'
    fill_screen(RED)
    orc_level = 0
    text = ''
    render_text = ''
    orc_run = True
    active = False
    orc_level_render = title_font.render(orc_level_text, True, BLACK)
    current_level_render = font.render(current_level_text, True, BLACK)
    input_box_outer = pygame.Rect(350, 300, 200, 80)
    input_box_inner = pygame.Rect(355, 305, 190, 70)
    WIN.blit(orc_level_render, (160, 130))
    WIN.blit(current_level_render, (350, 260))
    WIN.fill(BLACK, input_box_outer)
    WIN.fill(WHITE, input_box_inner)
    while orc_run:
        WIN.fill(BLACK, input_box_outer)
        if active:
            WIN.fill(VERY_LIGHT_BLUE, input_box_inner)
        else:
            WIN.fill(WHITE, input_box_inner)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_inner.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        orc_level = int(text)
                        text = ''
                        orc_run = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        render_text = font.render(text, True, pygame.Color('black'))
        WIN.blit(render_text, (365, 333))
        pygame.display.update()
    orc_health = 100
    orc_gold = orc_level * 10
    if orc_gold < 0:
        orc_gold = 0
    for i in range(2, orc_level + 1, 1):
        orc_health += (int(i * 1.5))
    o = Orc("Orc", orc_health, float(randrange(100, 200, 1) / 100),
            orc_level, int(10 * (orc_level + 1) * (orc_level / 2)), 100, 1, orc_gold)
    begin_fight(o)


def end_fight(o: Orc):
    fight_lines.clear()
    if not h.is_alive():
        WIN.fill(WHITE, pygame.Rect(200, 300, 200, 200))
        fight_lines.append("You died!")
        h.set_health(h.get_max_health())
        h.set_crit_chance(h.get_default_crit_chance())
        h.set_mana(h.get_max_mana())
    if not o.is_alive():
        WIN.fill(WHITE, pygame.Rect(500, 110, 200, 190))
        fight_lines.append("You were victorious!")
        h.give_gold(o.get_gold_reward())
        fight_lines.append("You earned {} gold!".format(o.get_gold_reward()))
        fight_lines.append("You earned {} experience!".format(o.get_exp_reward()))
        if h.give_experience(o.get_exp_reward()):
            fight_lines.append("You leveled up to level {}!".format(h.get_level()))
        h.set_health(h.get_max_health())
        h.set_crit_chance(h.get_default_crit_chance())
        h.set_mana(h.get_max_mana())
    print_fight_lines(fight_lines)
    main_menu()


def begin_fight(o: Orc):
    pygame.display.set_caption("Fight")
    fight_run = True
    font = pygame.font.SysFont('cambodia', int(40 / 1.2))
    title_font = pygame.font.SysFont('cambodia', 70)
    character = pygame.image.load('char.png')
    orc_level_text = "Lv. {} ".format(o.get_level()) + 'Orc'
    hero_level_text = "Lv. {} ".format(h.get_level()) + str(h)
    move_text_surfaces = []
    move_buttons = []
    pygame.mixer.music.stop()
    pygame.mixer.music.load('BotD.mp3')
    pygame.mixer.music.play(loops=1000)
    char = pygame.image.load('char.png')
    orc_level_render = font.render(orc_level_text, True, BLACK)
    hero_level_render = font.render(hero_level_text, True, BLACK)
    for i, move in enumerate(h.get_moves()):
        move_text_surfaces.append(font.render(move[0] + "   MP Cost: {}".format(move[4]), True, BLACK))
        move_buttons.append(pygame.Rect(530, 380 + i * 42,
                                        move_text_surfaces[i].get_width(), move_text_surfaces[i].get_height()))
    reset_frame()
    while fight_run:
        hero_hp_text = "HP: {}".format(h.get_health())
        orc_hp_text = "HP: {}".format(o.get_health())
        hero_mp_text = "MP: {}".format(h.get_mana())
        orc_mp_text = "MP: {}".format(o.get_mana())
        hero_hp_render = font.render(hero_hp_text, True, BLACK)
        orc_hp_render = font.render(orc_hp_text, True, BLACK)
        hero_mp_render = font.render(hero_mp_text, True, BLACK)
        orc_mp_render = font.render(orc_mp_text, True, BLACK)
        hero_hp_rect = pygame.Rect(25, 420, hero_hp_render.get_width(), hero_hp_render.get_height())
        orc_hp_rect = pygame.Rect(265, 65, orc_hp_render.get_width(), orc_hp_render.get_height())
        hero_mp_rect = pygame.Rect(25, 460, hero_mp_render.get_width(), hero_mp_render.get_height())
        orc_mp_rect = pygame.Rect(265, 105, orc_mp_render.get_width(), orc_mp_render.get_height())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(move_buttons):
                    if button.collidepoint(event.pos):
                        if h.get_mana() >= h.get_moves()[i][4]:
                            execute_hero_move(i, h.get_moves()[i][5], o)
                        else:
                            fight_lines.clear()
                            fight_lines.append('Not enough mana!')
                            print_fight_lines(fight_lines)
                            reset_frame()
                            WIN.blit(char, (250, 300))
                            WIN.blit(char, (500, 100))
                            WIN.blit(orc_level_render, (265, 25))
                            WIN.blit(hero_level_render, (25, 380))
                            hero_hp_text = "HP: {}".format(h.get_health())
                            orc_hp_text = "HP: {}".format(o.get_health())
                            hero_mp_text = "MP: {}".format(h.get_mana())
                            orc_mp_text = "MP: {}".format(o.get_mana())
                            hero_hp_render = font.render(hero_hp_text, True, BLACK)
                            orc_hp_render = font.render(orc_hp_text, True, BLACK)
                            hero_mp_render = font.render(hero_mp_text, True, BLACK)
                            orc_mp_render = font.render(orc_mp_text, True, BLACK)
                            WIN.fill(WHITE, hero_hp_rect)
                            WIN.fill(WHITE, orc_hp_rect)
                            WIN.fill(WHITE, hero_mp_rect)
                            WIN.fill(WHITE, orc_mp_rect)
                            hero_hp_rect = pygame.Rect(25, 420, hero_hp_render.get_width(), hero_hp_render.get_height())
                            orc_hp_rect = pygame.Rect(265, 65, orc_hp_render.get_width(), orc_hp_render.get_height())
                            hero_mp_rect = pygame.Rect(25, 460, hero_mp_render.get_width(), hero_mp_render.get_height())
                            orc_mp_rect = pygame.Rect(265, 105, orc_mp_render.get_width(), orc_mp_render.get_height())
                            WIN.fill(WHITE, hero_hp_rect)
                            WIN.fill(WHITE, orc_hp_rect)
                            WIN.fill(WHITE, hero_mp_rect)
                            WIN.fill(WHITE, orc_mp_rect)
                            WIN.blit(orc_hp_render, (265, 65))
                            WIN.blit(hero_hp_render, (25, 420))
                            WIN.blit(orc_mp_render, (265, 105))
                            WIN.blit(hero_mp_render, (25, 460))
                            draw_healthbar(h.get_health(), h.get_max_health(), 20, 500, 440, 40)
                            draw_healthbar(o.get_health(), o.get_max_health(), 440, 20, 440, 40)
                            draw_manabar(h.get_mana(), h.get_max_mana(), 20, 550, 440, 40)
                            draw_manabar(o.get_mana(), o.get_max_mana(), 440, 70, 440, 40)
                            moves_outer = pygame.Rect(500, 350, 400, 250)
                            moves_inner = pygame.Rect(510, 360, 390, 240)
                            WIN.fill(BLACK, moves_outer)
                            WIN.fill(WHITE, moves_inner)
                            continue
                        draw_healthbar(h.get_health(), h.get_max_health(), 20, 500, 440, 40)
                        draw_healthbar(o.get_health(), o.get_max_health(), 440, 20, 440, 40)
                        draw_manabar(h.get_mana(), h.get_max_mana(), 20, 550, 440, 40)
                        draw_manabar(o.get_mana(), o.get_max_mana(), 440, 70, 440, 40)
                        hero_hp_text = "HP: {}".format(h.get_health())
                        orc_hp_text = "HP: {}".format(o.get_health())
                        hero_mp_text = "MP: {}".format(h.get_mana())
                        orc_mp_text = "MP: {}".format(o.get_mana())
                        hero_hp_render = font.render(hero_hp_text, True, BLACK)
                        orc_hp_render = font.render(orc_hp_text, True, BLACK)
                        hero_mp_render = font.render(hero_mp_text, True, BLACK)
                        orc_mp_render = font.render(orc_mp_text, True, BLACK)
                        WIN.fill(WHITE, hero_hp_rect)
                        WIN.fill(WHITE, orc_hp_rect)
                        WIN.fill(WHITE, hero_mp_rect)
                        WIN.fill(WHITE, orc_mp_rect)
                        hero_hp_rect = pygame.Rect(25, 420, hero_hp_render.get_width(), hero_hp_render.get_height())
                        orc_hp_rect = pygame.Rect(265, 65, orc_hp_render.get_width(), orc_hp_render.get_height())
                        hero_mp_rect = pygame.Rect(25, 460, hero_mp_render.get_width(), hero_mp_render.get_height())
                        orc_mp_rect = pygame.Rect(265, 105, orc_mp_render.get_width(), orc_mp_render.get_height())
                        WIN.fill(WHITE, hero_hp_rect)
                        WIN.fill(WHITE, orc_hp_rect)
                        WIN.fill(WHITE, hero_mp_rect)
                        WIN.fill(WHITE, orc_mp_rect)
                        WIN.blit(orc_hp_render, (265, 65))
                        WIN.blit(hero_hp_render, (25, 420))
                        WIN.blit(orc_mp_render, (265, 105))
                        WIN.blit(hero_mp_render, (25, 460))
                        print_fight_lines(fight_lines)
                        if not o.is_alive() or not h.is_alive():
                            end_fight(o)
                        orc_move = randint(1, 3)
                        execute_orc_move(orc_move - 1, o.get_moves()[orc_move - 1][5], o)
                        draw_healthbar(h.get_health(), h.get_max_health(), 20, 500, 440, 40)
                        draw_healthbar(o.get_health(), o.get_max_health(), 440, 20, 440, 40)
                        draw_manabar(h.get_mana(), h.get_max_mana(), 20, 550, 440, 40)
                        draw_manabar(o.get_mana(), o.get_max_mana(), 440, 70, 440, 40)
                        hero_hp_text = "HP: {}".format(h.get_health())
                        orc_hp_text = "HP: {}".format(o.get_health())
                        hero_mp_text = "MP: {}".format(h.get_mana())
                        orc_mp_text = "MP: {}".format(o.get_mana())
                        hero_hp_render = font.render(hero_hp_text, True, BLACK)
                        orc_hp_render = font.render(orc_hp_text, True, BLACK)
                        hero_mp_render = font.render(hero_mp_text, True, BLACK)
                        orc_mp_render = font.render(orc_mp_text, True, BLACK)
                        WIN.fill(WHITE, hero_hp_rect)
                        WIN.fill(WHITE, orc_hp_rect)
                        WIN.fill(WHITE, hero_mp_rect)
                        WIN.fill(WHITE, orc_mp_rect)
                        hero_hp_rect = pygame.Rect(25, 420, hero_hp_render.get_width(), hero_hp_render.get_height())
                        orc_hp_rect = pygame.Rect(265, 65, orc_hp_render.get_width(), orc_hp_render.get_height())
                        hero_mp_rect = pygame.Rect(25, 460, hero_mp_render.get_width(), hero_mp_render.get_height())
                        orc_mp_rect = pygame.Rect(265, 105, orc_mp_render.get_width(), orc_mp_render.get_height())
                        WIN.fill(WHITE, hero_hp_rect)
                        WIN.fill(WHITE, orc_hp_rect)
                        WIN.fill(WHITE, hero_mp_rect)
                        WIN.fill(WHITE, orc_mp_rect)
                        WIN.blit(orc_hp_render, (265, 65))
                        WIN.blit(hero_hp_render, (25, 420))
                        WIN.blit(orc_mp_render, (265, 105))
                        WIN.blit(hero_mp_render, (25, 460))
                        print_fight_lines(fight_lines)
                        if not o.is_alive() or not h.is_alive():
                            end_fight(o)
                        reset_frame()
                        WIN.blit(char, (250, 300))
                        WIN.blit(char, (500, 100))
                        WIN.blit(orc_level_render, (265, 25))
                        WIN.blit(hero_level_render, (25, 380))
                        hero_hp_text = "HP: {}".format(h.get_health())
                        orc_hp_text = "HP: {}".format(o.get_health())
                        hero_mp_text = "MP: {}".format(h.get_mana())
                        orc_mp_text = "MP: {}".format(o.get_mana())
                        hero_hp_render = font.render(hero_hp_text, True, BLACK)
                        orc_hp_render = font.render(orc_hp_text, True, BLACK)
                        hero_mp_render = font.render(hero_mp_text, True, BLACK)
                        orc_mp_render = font.render(orc_mp_text, True, BLACK)
                        WIN.fill(WHITE, hero_hp_rect)
                        WIN.fill(WHITE, orc_hp_rect)
                        WIN.fill(WHITE, hero_mp_rect)
                        WIN.fill(WHITE, orc_mp_rect)
                        hero_hp_rect = pygame.Rect(25, 420, hero_hp_render.get_width(), hero_hp_render.get_height())
                        orc_hp_rect = pygame.Rect(265, 65, orc_hp_render.get_width(), orc_hp_render.get_height())
                        hero_mp_rect = pygame.Rect(25, 460, hero_mp_render.get_width(), hero_mp_render.get_height())
                        orc_mp_rect = pygame.Rect(265, 105, orc_mp_render.get_width(), orc_mp_render.get_height())
                        WIN.fill(WHITE, hero_hp_rect)
                        WIN.fill(WHITE, orc_hp_rect)
                        WIN.fill(WHITE, hero_mp_rect)
                        WIN.fill(WHITE, orc_mp_rect)
                        WIN.blit(orc_hp_render, (265, 65))
                        WIN.blit(hero_hp_render, (25, 420))
                        WIN.blit(orc_mp_render, (265, 105))
                        WIN.blit(hero_mp_render, (25, 460))
                        draw_healthbar(h.get_health(), h.get_max_health(), 20, 500, 440, 40)
                        draw_healthbar(o.get_health(), o.get_max_health(), 440, 20, 440, 40)
                        draw_manabar(h.get_mana(), h.get_max_mana(), 20, 550, 440, 40)
                        draw_manabar(o.get_mana(), o.get_max_mana(), 440, 70, 440, 40)
                        moves_outer = pygame.Rect(500, 350, 400, 250)
                        moves_inner = pygame.Rect(510, 360, 390, 240)
                        WIN.fill(BLACK, moves_outer)
                        WIN.fill(WHITE, moves_inner)
        WIN.blit(char, (250, 300))
        WIN.blit(char, (500, 100))
        WIN.blit(orc_level_render, (265, 25))
        WIN.blit(hero_level_render, (25, 380))
        WIN.fill(WHITE, hero_hp_rect)
        WIN.fill(WHITE, orc_hp_rect)
        WIN.fill(WHITE, hero_mp_rect)
        WIN.fill(WHITE, orc_mp_rect)
        hero_hp_rect = pygame.Rect(25, 420, hero_hp_render.get_width(), hero_hp_render.get_height())
        orc_hp_rect = pygame.Rect(265, 65, orc_hp_render.get_width(), orc_hp_render.get_height())
        hero_mp_rect = pygame.Rect(25, 460, hero_mp_render.get_width(), hero_mp_render.get_height())
        orc_mp_rect = pygame.Rect(265, 105, orc_mp_render.get_width(), orc_mp_render.get_height())
        WIN.fill(WHITE, hero_hp_rect)
        WIN.fill(WHITE, orc_hp_rect)
        WIN.fill(WHITE, hero_mp_rect)
        WIN.fill(WHITE, orc_mp_rect)
        WIN.blit(orc_hp_render, (265, 65))
        WIN.blit(hero_hp_render, (25, 420))
        WIN.blit(orc_mp_render, (265, 105))
        WIN.blit(hero_mp_render, (25, 460))
        draw_healthbar(h.get_health(), h.get_max_health(), 20, 500, 440, 40)
        draw_healthbar(o.get_health(), o.get_max_health(), 440, 20, 440, 40)
        draw_manabar(h.get_mana(), h.get_max_mana(), 20, 550, 440, 40)
        draw_manabar(o.get_mana(), o.get_max_mana(), 440, 70, 440, 40)
        moves_outer = pygame.Rect(500, 350, 400, 250)
        moves_inner = pygame.Rect(510, 360, 390, 240)
        WIN.fill(BLACK, moves_outer)
        WIN.fill(WHITE, moves_inner)
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        for i, button in enumerate(move_buttons):
            if mouse_pos_x > 500 and mouse_pos_y > 380:
                if move_buttons[i].collidepoint(mouse_pos_x, mouse_pos_y):
                    move_text_surfaces[i] = font.render(h.get_moves()[i][0]
                                                        + "   MP Cost: {}".format(h.get_moves()[i][4]),
                                                        True, pygame.Color('green'))
                else:
                    move_text_surfaces[i] = font.render(h.get_moves()[i][0]
                                                        + "   MP Cost: {}".format(h.get_moves()[i][4]),
                                                        True, BLACK)
            WIN.blit(move_text_surfaces[i], (530, 380 + 42 * i))
        pygame.display.update()
    pygame.mixer.music.stop()
    main_menu()


def save_and_exit():
    with open("save.txt", "wt") as f:
        write_content = [h.get_name(), str(h.get_level()), h.get_nickname(), str(h.get_experience()),
                         str(h.get_classid()), str(h.get_gold())]
        for item in write_content:
            f.writelines(item + '\n')
        for item in h.get_items():
            f.writelines(str(item.get_id()) + '\n')
        f.close()
        pygame.quit()
    exit()
    # save is in this order: name, level, nickname, experience, class_id(1 - Swordsman, 2 - Healer,
    # 3 - Tank, 4 - Mage), gold, items(using class item ids, each one is on new line)


def inventory():
    pygame.display.set_caption("Inventory")
    small_font = pygame.font.SysFont('cambodia', 22)
    font = pygame.font.SysFont('cambodia', int(40 / 1.2))
    title_font = pygame.font.SysFont('cambodia', 70)
    fill_screen(BLUE)
    inv_run = True
    equip_text = "Equip"
    unequip_text = "Unequip"
    equip_buttons = []
    gold_text = 'Your Gold: {}'.format(h.get_gold())
    back_text = 'Back'
    back_button_x, back_button_y = 680, 550
    back_button_size_x, back_button_size_y = 200, 40
    pygame.mixer.music.stop()
    pygame.mixer.music.load('shop_inv_jeff.mp3')
    pygame.mixer.music.play(loops=1000)
    gold_render = title_font.render(gold_text, True, BLACK)
    while inv_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_outer.collidepoint(event.pos):
                    inv_run = False
                for i, button in enumerate(equip_buttons):
                    if button.collidepoint(event.pos):
                        if h.get_items()[i] not in h.get_equipped_items():
                            h.equip_item(h.get_items()[i].get_id())
                        else:
                            h.unequip_item(h.get_items()[i].get_id())
        WIN.blit(gold_render, (20, 20))
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        equip_buttons.clear()
        for i, item in enumerate(h.get_items()):
            current_text = item.get_name() + ' ' + item.get_type()
            current_render = (font if len(current_text) < 15 else small_font).render(current_text, True, BLACK)
            WIN.blit(current_render, (70 + (i - 4 if i >= 4 else i) * 205, 100 + (1 if i >= 4 else 0) * 250))
            current_outer = pygame.Rect(70 + (i - 4 if i >= 4 else i) * 205,
                                        140 + (1 if i >= 4 else 0) * 250, 145, 145)
            current_inner = pygame.Rect(70 + (i - 4 if i >= 4 else i) * 205 + 10,
                                        140 + (1 if i >= 4 else 0) * 250 + 10, 125, 125)
            WIN.fill(BLACK, current_outer)
            WIN.fill(WHITE, current_inner)
            if item.get_amplifier_type() == 0:
                if item.get_type() == "Sword":
                    current_image = pygame.image.load('sword_{}.png'.format(item.get_id() + 1))
                else:
                    current_image = pygame.image.load('a-10_thunderbolt.png')
            elif item.get_amplifier_type() == 1:
                current_image = pygame.image.load('healer_orb_{}.png'.format(item.get_id() + 1))
            elif item.get_amplifier_type() == 2:
                current_image = pygame.image.load('shield_{}.png'.format(item.get_id() + 1))
            elif item.get_amplifier_type() == 3:
                current_image = pygame.image.load('mana_restore_orb_{}.png'.format(item.get_id() + 1))
            elif item.get_amplifier_type() == 4:
                current_image = pygame.image.load('focus_sash.png')
            WIN.blit(current_image, (70 + (i - 4 if i >= 4 else i) * 205 + 10, 140 + (1 if i >= 4 else 0) * 250 + 10))
            current_button_text = "Unequip" if item in h.get_equipped_items() else "Equip"
            current_button_x, current_button_y = 70 + (i - 4 if i >= 4 else i) * 205, 305 + (1 if i >= 4 else 0) * 250
            current_button_size_x, current_button_size_y = 145, 40
            current_button_outer = draw_button(current_button_text, font, pygame.Color('green') if\
                                                                        current_button_x < mouse_pos_x\
                                                                        < current_button_x + current_button_size_x and\
                                                                        current_button_y < mouse_pos_y\
                                                                        < current_button_y + current_button_size_y
                                               else BLACK, BLACK, WHITE,
                                               current_button_x, current_button_y,
                                               current_button_size_x, current_button_size_y)
            equip_buttons.append(current_button_outer)
        if back_button_x < mouse_pos_x < back_button_x + back_button_size_x and\
                back_button_y < mouse_pos_y < back_button_y + back_button_size_y:
            back_render = font.render(back_text, True, LIGHT_GREEN)
        else:
            back_render = font.render(back_text, True, BLACK)
        back_button_outer = draw_button(back_text, font, BLACK, BLACK, WHITE, back_button_x, back_button_y,
                                        back_button_size_x, back_button_size_y)
        WIN.blit(back_render, (back_button_x + back_button_size_x / (3 if back_text.__len__() < 8 else 5),
                                     back_button_y + back_button_size_y / 4))
        pygame.display.update()
    main_menu()


def shop():
    pygame.display.set_caption("Shop")
    small_font = pygame.font.SysFont('cambodia', 22)
    font = pygame.font.SysFont('cambodia', int(40 / 1.2))
    title_font = pygame.font.SysFont('cambodia', 70)
    fill_screen(LIGHT_BROWN)
    shop_run = True
    shop_buttons = []
    back_text = 'Back'
    back_button_x, back_button_y = 680, 550
    back_button_size_x, back_button_size_y = 200, 40
    pygame.mixer.music.stop()
    pygame.mixer.music.load('shop_inv_jeff.mp3')
    pygame.mixer.music.play(loops=1000)
    gold_text = 'Your Gold: {}'.format(h.get_gold())
    gold_render = title_font.render(gold_text, True, BLACK)
    while shop_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_outer.collidepoint(event.pos):
                    shop_run = False
                for i, button in enumerate(shop_buttons):
                    if button.collidepoint(event.pos):
                        if h.get_class_items()[i] not in h.get_items():
                            if h.get_gold() >= h.get_class_items()[i].get_cost():
                                h.spend_gold(int(h.get_class_items()[i].get_cost()))
                                h.add_item(h.get_class_items()[i])
                                h.equip_item(h.get_class_items()[i].get_id())
                        else:
                            h.give_gold(int(h.get_class_items()[i].get_cost() / 2))
                            h.unequip_item(h.get_class_items()[i].get_id())
                            h.remove_item(h.get_class_items()[i])
        gold_rect = pygame.Rect(20, 20, gold_render.get_width(), gold_render.get_height())
        WIN.fill(LIGHT_BROWN, gold_rect)
        gold_text = 'Your Gold: {}'.format(h.get_gold())
        gold_render = title_font.render(gold_text, True, BLACK)
        gold_rect = pygame.Rect(20, 20, gold_render.get_width(), gold_render.get_height())
        WIN.fill(LIGHT_BROWN, gold_rect)
        WIN.blit(gold_render, (20, 20))
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        shop_buttons.clear()
        for i, item in enumerate(h.get_class_items()):
            current_text = item.get_name() + ' ' + item.get_type()
            current_render = (font if len(current_text) < 15 else small_font).render(current_text, True, BLACK)
            WIN.blit(current_render, (70 + (i - 4 if i >= 4 else i) * 205, 100 + (1 if i >= 4 else 0) * 250))
            current_outer = pygame.Rect(70 + (i - 4 if i >= 4 else i) * 205,
                                        140 + (1 if i >= 4 else 0) * 250, 145, 145)
            current_inner = pygame.Rect(70 + (i - 4 if i >= 4 else i) * 205 + 10,
                                        140 + (1 if i >= 4 else 0) * 250 + 10, 125, 125)
            WIN.fill(BLACK, current_outer)
            WIN.fill(WHITE, current_inner)
            if item.get_amplifier_type() == 0:
                if item.get_type() == "Sword":
                    current_image = pygame.image.load('sword_{}.png'.format(item.get_id() + 1))
                else:
                    current_image = pygame.image.load('a-10_thunderbolt.png')
            elif item.get_amplifier_type() == 1:
                current_image = pygame.image.load('healer_orb_{}.png'.format(item.get_id() + 1))
            elif item.get_amplifier_type() == 2:
                current_image = pygame.image.load('shield_{}.png'.format(item.get_id() + 1))
            elif item.get_amplifier_type() == 3:
                current_image = pygame.image.load('mana_restore_orb_{}.png'.format(item.get_id() + 1))
            elif item.get_amplifier_type() == 4:
                current_image = pygame.image.load('focus_sash.png')
            WIN.blit(current_image, (70 + (i - 4 if i >= 4 else i) * 205 + 10, 140 + (1 if i >= 4 else 0) * 250 + 10))
            current_button_text = 'Sell: {}$'.format(int(item.get_cost() / 2)) if item in h.get_items() else\
                                                                                'Buy: {}$'.format(int(item.get_cost()))
            current_button_x, current_button_y = 70 + (i - 4 if i >= 4 else i) * 205, 305 + (1 if i >= 4 else 0) * 250
            current_button_size_x, current_button_size_y = 145, 40
            current_button_outer = draw_button(current_button_text, font if current_button_text.__len__() < 9 else\
                small_font, pygame.Color('green') if \
                current_button_x < mouse_pos_x \
                < current_button_x + current_button_size_x and \
                current_button_y < mouse_pos_y \
                < current_button_y + current_button_size_y
            else BLACK, BLACK, WHITE,
                                               current_button_x, current_button_y,
                                               current_button_size_x, current_button_size_y)
            shop_buttons.append(current_button_outer)
        if back_button_x < mouse_pos_x < back_button_x + back_button_size_x and \
                back_button_y < mouse_pos_y < back_button_y + back_button_size_y:
            back_render = font.render(back_text, True, LIGHT_GREEN)
        else:
            back_render = font.render(back_text, True, BLACK)
        back_button_outer = draw_button(back_text, font, BLACK, BLACK, WHITE, back_button_x, back_button_y,
                                        back_button_size_x, back_button_size_y)
        WIN.blit(back_render, (back_button_x + back_button_size_x / (3 if back_text.__len__() < 8 else 5),
                               back_button_y + back_button_size_y / 4))
        pygame.display.update()
    main_menu()


def delete_save():
    fight_lines.clear()
    if path.exists("save.txt"):
        remove("save.txt")
        fight_lines.append("Your save file has been deleted!")
    else:
        fight_lines.append("There was no save file to delete!")
    print_message(fight_lines[0])


def title_screen():
    title_run = True
    pygame.display.set_caption(TITLE)
    pygame.mixer.music.stop()
    font = pygame.font.SysFont('cambodia', int(40 / 1.2))
    title_font = pygame.font.SysFont('cambodia', 70)
    button_play_x, button_play_y = 200, 450
    button_quit_x, button_quit_y = 500, 450
    button_size_x, button_size_y = BUTTON_WIDTH, BUTTON_HEIGHT
    button_play_outer = pygame.Rect(button_play_x, button_play_y, button_size_x, button_size_y)
    button_quit_outer = pygame.Rect(button_quit_x, button_quit_y, button_size_x, button_size_y)
    button_play_inner = pygame.Rect(button_play_x + button_size_x / 10,
                                    button_play_y + button_size_y / 10,
                                    4 / 5 * button_size_x,
                                    4 / 5 * button_size_y)
    button_quit_inner = pygame.Rect(button_quit_x + button_size_x / 10,
                                    button_quit_y + button_size_y / 10,
                                    4 / 5 * button_size_x,
                                    4 / 5 * button_size_y)
    play_text = 'Play'
    quit_text = 'Quit'
    button_play_text = font.render(play_text, True, pygame.Color('black'))
    button_quit_text = font.render(quit_text, True, pygame.Color('black'))
    title_text = title_font.render('Orc Fighter', True, pygame.Color('black'))
    reset_frame()
    WIN.fill(BLACK, button_play_outer)
    WIN.fill(BLACK, button_quit_outer)
    WIN.fill(WHITE, button_play_inner)
    WIN.fill(WHITE, button_quit_inner)
    while title_run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                title_run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_quit_outer.collidepoint(event.pos):
                    title_run = False
                elif button_play_outer.collidepoint(event.pos):
                    main_menu()
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        if button_play_x <= mouse_pos_x <= button_play_x + button_size_x and \
                button_play_y <= mouse_pos_y <= button_play_y + button_size_y:
            button_play_text = font.render('Play', True, pygame.Color('green'))
        else:
            button_play_text = font.render('Play', True, pygame.Color('black'))
        if button_quit_x <= mouse_pos_x <= button_quit_x + button_size_x and \
                button_quit_y <= mouse_pos_y <= button_quit_y + button_size_y:
            button_quit_text = font.render('Quit', True, pygame.Color('green'))
        else:
            button_quit_text = font.render('Quit', True, pygame.Color('black'))
        WIN.blit(button_play_text, (button_play_x + button_size_x / (3 if play_text.__len__() < 8 else 5),
                                    button_play_y + button_size_y / 4))
        WIN.blit(button_quit_text, (button_quit_x + button_size_x / (3 if quit_text.__len__() < 8 else 5),
                                    button_quit_y + button_size_y / 4))
        WIN.blit(title_text, (300, 150))
        pygame.display.update()

    pygame.quit()


def main_menu():
    fill_screen(LIGHT_GREEN)
    menu_run = True
    pygame.mixer.music.stop()
    pygame.mixer.music.load('PassInf.mp3')
    pygame.mixer.music.play(loops=1000)
    font = pygame.font.SysFont('cambodia', int(40 / 1.2))
    title_font = pygame.font.SysFont('cambodia', 70)
    pygame.display.set_caption('Main Menu')
    title_text = title_font.render('Orc Fighter', True, pygame.Color('black'))
    button_size_x, button_size_y = BUTTON_WIDTH, BUTTON_HEIGHT
    fight_text = 'Fight'
    save_text = 'Save & Exit'
    inv_text = 'Inventory'
    back_text = 'Back'
    shop_text = 'Shop'
    del_text = 'Delete Save'
    button_fight_x, button_fight_y = 150, 150
    button_fight_outer = draw_button(fight_text, font, BLACK, BLACK, LIGHT_GREEN, button_fight_x,
                                     button_fight_y, button_size_x, button_size_y)
    button_save_x, button_save_y = 550, 150
    button_save_outer = draw_button(save_text, font, BLACK, BLACK, LIGHT_GREEN, button_save_x,
                                     button_save_y, button_size_x, button_size_y)
    button_inv_x, button_inv_y = 150, 250
    button_inv_outer = draw_button(inv_text, font, BLACK, BLACK, LIGHT_GREEN, button_inv_x,
                                   button_inv_y, button_size_x, button_size_y)
    button_del_x, button_del_y = 550, 250
    button_del_outer = draw_button(del_text, font, BLACK, BLACK, LIGHT_GREEN, button_del_x,
                                   button_del_y, button_size_x, button_size_y)
    button_back_x, button_back_y = 550, 350
    button_back_outer = draw_button(back_text, font, BLACK, BLACK, LIGHT_GREEN, button_back_x,
                                   button_back_y, button_size_x, button_size_y)
    button_shop_x, button_shop_y = 150, 350
    button_shop_outer = draw_button(shop_text, font, BLACK, BLACK, LIGHT_GREEN, button_shop_x,
                                   button_shop_y, button_size_x, button_size_y)
    while menu_run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_fight_outer.collidepoint(event.pos):
                    orc_level_menu()
                elif button_save_outer.collidepoint(event.pos):
                    save_and_exit()
                elif button_inv_outer.collidepoint(event.pos):
                    inventory()
                elif button_back_outer.collidepoint(event.pos):
                    title_screen()
                elif button_del_outer.collidepoint(event.pos):
                    delete_save()
                    fill_screen(LIGHT_GREEN)
                    button_fight_outer = draw_button(fight_text, font, BLACK, BLACK, LIGHT_GREEN, button_fight_x,
                                                     button_fight_y, button_size_x, button_size_y)
                    button_save_outer = draw_button(save_text, font, BLACK, BLACK, LIGHT_GREEN, button_save_x,
                                                    button_save_y, button_size_x, button_size_y)
                    button_inv_outer = draw_button(inv_text, font, BLACK, BLACK, LIGHT_GREEN, button_inv_x,
                                                   button_inv_y, button_size_x, button_size_y)
                    button_del_outer = draw_button(del_text, font, BLACK, BLACK, LIGHT_GREEN, button_del_x,
                                                   button_del_y, button_size_x, button_size_y)
                    button_back_outer = draw_button(back_text, font, BLACK, BLACK, LIGHT_GREEN, button_back_x,
                                                    button_back_y, button_size_x, button_size_y)
                    button_shop_outer = draw_button(shop_text, font, BLACK, BLACK, LIGHT_GREEN, button_shop_x,
                                                    button_shop_y, button_size_x, button_size_y)
                elif button_shop_outer.collidepoint(event.pos):
                    shop()
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        if button_fight_x <= mouse_pos_x <= button_fight_x + button_size_x and \
                button_fight_y <= mouse_pos_y <= button_fight_y + button_size_y:
            button_fight_text = font.render(fight_text, True, pygame.Color('red'))
        else:
            button_fight_text = font.render(fight_text, True, pygame.Color('black'))
        if button_save_x <= mouse_pos_x <= button_save_x + button_size_x and \
                button_save_y <= mouse_pos_y <= button_save_y + button_size_y:
            button_save_text = font.render(save_text, True, pygame.Color('green'))
        else:
            button_save_text = font.render(save_text, True, pygame.Color('black'))
        if button_inv_x <= mouse_pos_x <= button_inv_x + button_size_x and \
                button_inv_y <= mouse_pos_y <= button_inv_y + button_size_y:
            button_inv_text = font.render(inv_text, True, pygame.Color('blue'))
        else:
            button_inv_text = font.render(inv_text, True, pygame.Color('black'))
        if button_back_x <= mouse_pos_x <= button_back_x + button_size_x and \
                button_back_y <= mouse_pos_y <= button_back_y + button_size_y:
            button_back_text = font.render(back_text, True, pygame.Color('white'))
        else:
            button_back_text = font.render(back_text, True, pygame.Color('black'))
        if button_del_x <= mouse_pos_x <= button_del_x + button_size_x and \
                button_del_y <= mouse_pos_y <= button_del_y + button_size_y:
            button_del_text = font.render(del_text, True, VERY_LIGHT_BLUE)
        else:
            button_del_text = font.render(del_text, True, pygame.Color('black'))
        if button_shop_x <= mouse_pos_x <= button_shop_x + button_size_x and \
                button_shop_y <= mouse_pos_y <= button_shop_y + button_size_y:
            button_shop_text = font.render(shop_text, True, LIGHT_BROWN)
        else:
            button_shop_text = font.render(shop_text, True, pygame.Color('black'))
        WIN.blit(title_text, (300, 50))
        WIN.blit(button_fight_text, (button_fight_x + button_size_x / (3 if fight_text.__len__() < 8 else 5),
                                     button_fight_y + button_size_y / 4))
        WIN.blit(button_save_text, (button_save_x + button_size_x / (3 if save_text.__len__() < 8 else 5),
                                     button_save_y + button_size_y / 4))
        WIN.blit(button_inv_text, (button_inv_x + button_size_x / (3 if inv_text.__len__() < 8 else 5),
                                     button_inv_y + button_size_y / 4))
        WIN.blit(button_back_text, (button_back_x + button_size_x / (3 if back_text.__len__() < 8 else 5),
                                   button_back_y + button_size_y / 4))
        WIN.blit(button_del_text, (button_del_x + button_size_x / (3 if del_text.__len__() < 8 else 5),
                                    button_del_y + button_size_y / 4))
        WIN.blit(button_shop_text, (button_shop_x + button_size_x / (3 if shop_text.__len__() < 8 else 5),
                                   button_shop_y + button_size_y / 4))
        pygame.display.update()
    title_screen()


if first_time == 1:
    font = pygame.font.SysFont('cambodia', int(40 / 1.2))
    title_font = pygame.font.SysFont('cambodia', 70)
    reset_frame()
    input_box_outer = pygame.Rect(300, 300, 300, 80)
    input_box_inner = pygame.Rect(305, 305, 290, 70)
    WIN.fill(BLACK, input_box_outer)
    WIN.fill(WHITE, input_box_inner)
    text = ''
    hero_name = ''
    hero_nickname = ''
    name_text = 'Please input your name: '
    nickname_text = 'Please input your nickname: '
    class_text = 'Please choose your class: '
    swordsman_text = 'Swordsman'
    healer_text = 'Healer'
    tank_text = 'Tank'
    mage_text = 'Mage'
    active = False
    run = True
    name_render = title_font.render(name_text, True, BLACK)
    WIN.blit(name_render, (150, 150))
    while run:
        WIN.fill(BLACK, input_box_outer)
        if active:
            WIN.fill(VERY_LIGHT_BLUE, input_box_inner)
        else:
            WIN.fill(WHITE, input_box_inner)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_inner.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        hero_name = text
                        text = ''
                        run = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if text.__len__() < 15:
                            text += event.unicode
        render_text = font.render(text, True, pygame.Color('black'))
        WIN.blit(render_text, (315, 333))
        pygame.display.update()
    run = True
    fill_screen(WHITE)
    input_box_outer = pygame.Rect(300, 300, 300, 80)
    input_box_inner = pygame.Rect(305, 305, 290, 70)
    WIN.fill(BLACK, input_box_outer)
    WIN.fill(WHITE, input_box_inner)
    nickname_render = title_font.render(nickname_text, True, BLACK)
    WIN.blit(nickname_render, (125, 150))
    while run:
        WIN.fill(BLACK, input_box_outer)
        if active:
            WIN.fill(VERY_LIGHT_BLUE, input_box_inner)
        else:
            WIN.fill(WHITE, input_box_inner)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_inner.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        hero_nickname = text
                        text = ''
                        run = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if text.__len__() < 15:
                            text += event.unicode
        render_text = font.render(text, True, pygame.Color('black'))
        WIN.blit(render_text, (315, 333))
        pygame.display.update()
    sword = pygame.image.load('sword_5.png').convert()
    potion = pygame.image.load('healer_orb_4.png').convert()
    shield = pygame.image.load('shield_3.png').convert()
    pearl = pygame.image.load('mana_restore_orb_3.png').convert()
    swordsman_description = [
        "Health: Good",
        "Mana: Default",
        "Healing: Bad",
        "Attack: Great",
        "Special: Attack"
    ]
    healer_description = [
        "Health: OK",
        "Mana: Good",
        "Healing: Great",
        "Attack: Bad",
        "Special: Regen"
    ]
    tank_description = [
        "Health: Excellent",
        "Mana: OK",
        "Healing: OK",
        "Attack: Good",
        "Special: Rage"
    ]
    mage_description = [
        "Health: Awful",
        "Mana: Excellent",
        "Healing: OK",
        "Attack: Great",
        "Special: No Crits"
    ]
    class_render = title_font.render(class_text, True, BLACK)
    button_swordsman_x, button_swordsman_y = 70, 175
    button_healer_x, button_healer_y = 275, 175
    button_tank_x, button_tank_y = 480, 175
    button_mage_x, button_mage_y = 685, 175
    button_size_x, button_size_y = 145, 145
    fill_screen(WHITE)
    swordsman_render = font.render(swordsman_text, True, BLACK)
    healer_render = font.render(healer_text, True, BLACK)
    tank_render = font.render(tank_text, True, BLACK)
    mage_render = font.render(mage_text, True, BLACK)
    button_swordsman_outer = pygame.Rect(button_swordsman_x, button_swordsman_y, button_size_x, button_size_y)
    button_swordsman_inner = pygame.Rect(button_swordsman_x + 10, button_swordsman_y + 10,
                                         button_size_x - 20, button_size_y - 20)
    button_healer_outer = pygame.Rect(button_healer_x, button_healer_y, button_size_x, button_size_y)
    button_healer_inner = pygame.Rect(button_healer_x + 10, button_healer_y + 10,
                                      button_size_x - 20, button_size_y - 20)
    button_tank_outer = pygame.Rect(button_tank_x, button_tank_y, button_size_x, button_size_y)
    button_tank_inner = pygame.Rect(button_tank_x + 10, button_tank_y + 10,
                                    button_size_x - 20, button_size_y - 20)
    button_mage_outer = pygame.Rect(button_mage_x, button_mage_y, button_size_x, button_size_y)
    button_mage_inner = pygame.Rect(button_mage_x + 10, button_mage_y + 10,
                                    button_size_x - 20, button_size_y - 20)
    WIN.fill(BLACK, button_swordsman_outer)
    WIN.fill(WHITE, button_swordsman_inner)
    WIN.fill(BLACK, button_healer_outer)
    WIN.fill(WHITE, button_healer_inner)
    WIN.fill(BLACK, button_tank_outer)
    WIN.fill(WHITE, button_tank_inner)
    WIN.fill(BLACK, button_mage_outer)
    WIN.fill(WHITE, button_mage_inner)
    WIN.blit(class_render, (125, 55))
    WIN.blit(swordsman_render, (button_swordsman_x, 135))
    WIN.blit(healer_render, (button_healer_x, 135))
    WIN.blit(tank_render, (button_tank_x, 135))
    WIN.blit(mage_render, (button_mage_x, 135))
    WIN.blit(sword, (button_swordsman_x + 10, button_swordsman_y + 10))
    WIN.blit(potion, (button_healer_x + 10, button_healer_y + 10))
    WIN.blit(shield, (button_tank_x + 10, button_tank_y + 10))
    WIN.blit(pearl, (button_mage_x + 10, button_mage_y + 10))
    for i, text in enumerate(swordsman_description):
        description_render = font.render(text, True, BLACK)
        WIN.blit(description_render, (button_swordsman_x, 330 + (i * 42)))
    for i, text in enumerate(healer_description):
        description_render = font.render(text, True, BLACK)
        WIN.blit(description_render, (button_healer_x, 330 + (i * 42)))
    for i, text in enumerate(tank_description):
        description_render = font.render(text, True, BLACK)
        WIN.blit(description_render, (button_tank_x, 330 + (i * 42)))
    for i, text in enumerate(mage_description):
        description_render = font.render(text, True, BLACK)
        WIN.blit(description_render, (button_mage_x, 330 + (i * 42)))
    hero_class = 0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_swordsman_outer.collidepoint(event.pos):
                    run = False
                    hero_class = 1
                elif button_healer_outer.collidepoint(event.pos):
                    run = False
                    hero_class = 2
                elif button_tank_outer.collidepoint(event.pos):
                    run = False
                    hero_class = 3
                elif button_mage_outer.collidepoint(event.pos):
                    run = False
                    hero_class = 4
        pygame.display.update()
    if hero_class == 1:
        h = Swordsman(hero_name, 110, hero_nickname, 1, 0, 100, 1.1, hero_class, 0, [])
    elif hero_class == 2:
        h = Healer(hero_name, 90, hero_nickname, 1, 0, 120, 0.9, hero_class, 0, [])
    elif hero_class == 3:
        h = Tank(hero_name, 130, hero_nickname, 1, 0, 90, 1.3, hero_class, 0, [])
    elif hero_class == 4:
        h = Mage(hero_name, 75, hero_nickname, 1, 0, 150, 0.75, hero_class, 0, [])
    else:
        pass
else:
    with open("save.txt", "rt") as f:
        stats = f.readlines()
        stats[0] = stats[0].strip("\n")
        stats[2] = stats[2].strip("\n")
        stats[4] = int(stats[4])
        stats[5] = int(stats[5])
        save_items = []
        for i in range(6, len(stats), 1):
            stats[i] = int(stats[i])
            save_items.append(stats[i])
        if stats[4] == 1:
            save_health = 110
            for i in range(2, int(stats[1]) + 1, 1):
                save_health += int(i * 1.5 * 1.1)
            h = Swordsman(stats[0], save_health, stats[2], int(stats[1]), int(stats[3]), 100, 1.1, stats[4], stats[5],
                          save_items)
        elif stats[4] == 2:
            save_health = 90
            for i in range(2, int(stats[1]) + 1, 1):
                save_health += int(i * 1.5 * 0.9)
            h = Healer(stats[0], save_health, stats[2], int(stats[1]), int(stats[3]), 120, 0.9, stats[4], stats[5],
                       save_items)
        elif stats[4] == 3:
            save_health = 130
            for i in range(2, int(stats[1]) + 1, 1):
                save_health += int(i * 1.5 * 1.3)
            h = Tank(stats[0], save_health, stats[2], int(stats[1]), int(stats[3]), 90, 1.3, stats[4], stats[5],
                     save_items)
        elif stats[4] == 4:
            save_health = 75
            for i in range(2, int(stats[1]) + 1, 1):
                save_health += int(i * 1.5 * 0.75)
            h = Mage(stats[0], save_health, stats[2], int(stats[1]), int(stats[3]), 150, 0.75, stats[4], stats[5],
                     save_items)
        else:
            pygame.set_error('ERROR: Corrupted save file. Please delete the existing one and restart the game.')
            pygame.quit()
title_screen()
