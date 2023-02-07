from orc import Orc
from swordsman import Swordsman
from healer import Healer
from tank import Tank
from mage import Mage
from random import randrange, randint
from os import system, path, name

if path.isfile('save.txt'):
    first_time = 0
else:
    first_time = 1


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def is_crit(crit_chance):
    n = float(randrange(0, 100, 1) / 100)
    if n < crit_chance:
        return True
    else:
        return False


def execute_hero_move(n, move_type):
    if move_type == 0:
        clear()
        h.spend_mana(h.Moves[n][4])
        damage = int(randrange(h.Moves[n][2], h.Moves[n][3], 1) * h.LevelAttackMult * h.AttackMult)
        if is_crit(h.CritChance):
            damage = int(damage * h.CritMult)
            print("You landed a critical hit!")
        o.take_damage(damage)
        print("You dealt {} damage!".format(damage))
        input("Press Enter to continue...")
        return True
    elif move_type == 1:
        h.spend_mana(h.Moves[n][4])
        healing = int(randrange(h.Moves[n][2], h.Moves[n][3], 1) * h.LevelAttackMult)
        h.take_healing(healing)
        clear()
        print("You healed for {} health!".format(healing))
        input("Press Enter to continue...")
        return True
    elif move_type == 2:
        clear()
        h.spend_mana(h.Moves[n][4])
        h.focus(n)
        print("You became focused! Your critical hit chance increased!")
        input("Press Enter to continue...")
        return True
    elif move_type == 3:
        mana = int(randrange(h.Moves[n][2], h.Moves[n][3], 1))
        h.regen_mana(mana)
        clear()
        print("You restored {} mana!".format(mana))
        input("Press Enter to continue...")
        return True
    elif move_type == 4:
        clear()
        h.spend_mana(h.Moves[n][4])
        h.rage(n)
        print("You were consumed by rage! You now deal more damage!")
        input("Press Enter to continue...")
        return True
    else:
        clear()
        print("Invalid input!")
        input("Press Enter to continue...")
        return False


def execute_orc_move(n, move_type):
    if move_type == 0:
        o.spend_mana(o.Moves[n][4])
        damage = int(randrange(o.Moves[n][2], o.Moves[n][3], 1) * o.LevelAttackMult * o.BerserkFactor)
        h.take_damage(damage)
        clear()
        print("You took {} damage!".format(damage))
        input("Press Enter to continue...")
    elif move_type == 1:
        o.spend_mana(o.Moves[n][4])
        healing = int(randrange(o.Moves[n][2], o.Moves[n][3], 1) * o.LevelAttackMult)
        o.take_healing(healing)
        clear()
        print("The orc healed for {} health!".format(healing))
        input("Press Enter to continue...")
    elif move_type == 3:
        mana = int(randrange(o.Moves[n][2], o.Moves[n][3], 1))
        o.regen_mana(mana)
        clear()
        print("The orc restored {} mana!".format(mana))
        input("Press Enter to continue...")
    else:
        clear()
        print("Unexpected error: Invalid orc move")
        print("The game will now close")
        input("Press Enter to close the game...")
        exit()


def end_fight():
    if not h.is_alive():
        clear()
        print("You died!")
        h.Health = h.MaxHealth
        h.CritChance = h.DefaultCritChance
        h.Mana = h.MaxMana
        input("Press Enter to continue...")
    if not o.is_alive():
        clear()
        level_check = 0
        print("You were victorious!")
        print("You earned {} experience!".format(o.ExpReward))
        input("Press Enter to continue...")
        h.Experience += o.ExpReward
        while h.Experience >= h.NeededExp:
            h.level_up()
            level_check = 1
        if level_check:
            clear()
            print("You leveled up to level {}!".format(h.Level))
            input("Press Enter to continue...")
        h.Health = h.MaxHealth
        h.CritChance = h.DefaultCritChance
        h.Mana = h.MaxMana
    return 0


def fight():
    while h.is_alive() and o.is_alive():
        clear()
        print("{text:^40}".format(text="Lv.{level} {name}".format(level=o.Level, name=o.Name)))
        print("{text:^40}".format(text="Health: {health}/{max_health}".format(health=o.Health, max_health=o.MaxHealth)))
        print("{text:^40}\n".format(text="Mana: {mana}/{max_mana}".format(mana=o.Mana, max_mana=o.MaxMana)))
        print("{text:^40}".format(text="Lv.{level} {name} the {nickname}".format(level=h.Level,
                                                                                 name=h.Name, nickname=h.Nickname)))
        print("{text:^40}".format(text="Health: {health}/{max_health}".format(health=h.Health, max_health=h.MaxHealth)))
        print("{text:^40}\n".format(text="Mana: {mana}/{max_mana}".format(mana=h.Mana, max_mana=h.MaxMana)))
        for move in h.Moves:
            print("{id}. {move_name}   Mana Cost: {mana_cost}".format(id=move[1], move_name=move[0], mana_cost=move[4]))
        choice = int(input("Choose an action: "))
        if choice > 5 or choice < 1:
            clear()
            print("Invalid action!")
            input("Press Enter to continue...")
            continue
        if not h.Mana < h.Moves[choice - 1][4]:
            if not execute_hero_move(choice - 1, h.Moves[choice - 1][5]):
                clear()
                print("Invalid action!")
                input("Press Enter to continue...")
                continue
        else:
            clear()
            print("Not enough mana!")
            input("Press Enter to continue...")
            continue
        if not o.is_alive():
            end_fight()
            break
        orc_move = randint(1, 3)
        execute_orc_move(orc_move - 1, o.Moves[orc_move - 1][5])
        if not h.is_alive():
            end_fight()
            break
        continue


if first_time == 1:
    hero_name = input('Please input the Name of your character: ')
    clear()
    hero_nickname = input('Please input the Nickname of your character: ')
    clear()
    print('Please choose the class of your character: ')
    print('1. Swordsman')
    print('2. Healer')
    print('3. Tank')
    print('4. Mage\n')
    hero_class = int(input('Choice: '))
    if hero_class == 1:
        h = Swordsman(hero_name, 110, hero_nickname, 1, 0, 100, 1.1, hero_class)
    elif hero_class == 2:
        h = Healer(hero_name, 90, hero_nickname, 1, 0, 120, 0.9, hero_class)
    elif hero_class == 3:
        h = Tank(hero_name, 130, hero_nickname, 1, 0, 90, 1.3, hero_class)
    elif hero_class == 4:
        h = Mage(hero_name, 75, hero_nickname, 1, 0, 150, 0.75, hero_class)
    else:
        clear()
        print("Unexpected error when creating character!")
        print("The game will now close")
        input("Press Enter to close the game...")
        exit()
else:
    with open("save.txt", "rt") as f:
        stats = f.readlines()
        stats[0] = stats[0].strip("\n")
        stats[2] = stats[2].strip("\n")
        stats[4] = int(stats[4])
        if stats[4] == 1:
            save_health = 110
            for i in range(2, int(stats[1]) + 1, 1):
                save_health += int(i * 1.5 * 1.1)
            h = Swordsman(stats[0], save_health, stats[2], int(stats[1]), int(stats[3]), 100, 1.1, stats[4])
        elif stats[4] == 2:
            save_health = 90
            for i in range(2, int(stats[1]) + 1, 1):
                save_health += int(i * 1.5 * 0.9)
            h = Healer(stats[0], save_health, stats[2], int(stats[1]), int(stats[3]), 120, 0.9, stats[4])
        elif stats[4] == 3:
            save_health = 130
            for i in range(2, int(stats[1]) + 1, 1):
                save_health += int(i * 1.5 * 1.3)
            h = Tank(stats[0], save_health, stats[2], int(stats[1]), int(stats[3]), 90, 1.3, stats[4])
        elif stats[4] == 4:
            save_health = 75
            for i in range(2, int(stats[1]) + 1, 1):
                save_health += int(i * 1.5 * 0.75)
            h = Mage(stats[0], save_health, stats[2], int(stats[1]), int(stats[3]), 150, 0.75, stats[4])
        else:
            clear()
            print("Unexpected error: Corrupted Save File! Please delete it and start over!")
            print("The game will now close")
            input("Press Enter to close the game...")
            exit()

while True:
    clear()
    print("Orc Fighter\n")
    print("1. Fight")
    print("2. Save & Exit")
    menu_choice = int(input('Please make a selection: '))
    if menu_choice == 1:
        clear()
        orc_level = int(input("Please choose an orc level to fight: "))
        orc_health = 100
        for i in range(2, orc_level + 1, 1):
            orc_health += (int(i * 1.5))
        o = Orc("Orc", orc_health, float(randrange(100, 200, 1) / 100),
                orc_level, int(10 * (orc_level + 1) * (orc_level / 2)), 100, 1)
        fight()
    elif menu_choice == 2:
        with open("save.txt", "wt") as f:
            write_content = [h.Name, str(h.Level), h.Nickname, str(h.Experience), str(h.ClassId)]
            for item in write_content:
                f.writelines(item + '\n')
            f.close()
            exit()
    else:
        clear()
        print("Invalid Choice!")
        input("Press Enter to continue...")
        continue






