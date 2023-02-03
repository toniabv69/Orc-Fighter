from orc import Orc
from hero import Hero
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


def execute_hero_move(n):
    if n == 1:
        clear()
        damage = int(randrange(h.Moves[0][2], h.Moves[0][3], 1) * h.LevelAttackMult)
        if is_crit(h.CritChance):
            damage = int(damage * h.CritMult)
            print("You landed a critical hit!")
        o.take_damage(damage)
        print("You dealt {} damage!".format(damage))
        input("Press Enter to continue...")
        return True
    elif n == 2:
        healing = int(randrange(h.Moves[1][2], h.Moves[1][3], 1) * h.LevelAttackMult)
        h.take_healing(healing)
        clear()
        print("You healed for {} health!".format(healing))
        input("Press Enter to continue...")
        return True
    elif n == 3:
        clear()
        h.focus()
        print("You became focused! Your critical hit chance increased!")
        input("Press Enter to continue...")
        return True
    elif n == 4:
        clear()
        h.rage()
        print("You were consumed by rage! Your critical hits now deal more damage!")
        input("Press Enter to continue...")
        return True
    else:
        clear()
        print("Invalid input!")
        input("Press Enter to continue...")
        return False


def execute_orc_move(n):
    if n == 1:
        damage = int(randrange(o.Moves[0][2], o.Moves[0][3], 1) * o.LevelAttackMult)
        h.take_damage(damage)
        clear()
        print("You took {} damage!".format(damage))
        input("Press Enter to continue...")
    elif n == 2:
        healing = int(randrange(o.Moves[1][2], o.Moves[1][3], 1) * o.LevelAttackMult)
        o.take_healing(healing)
        clear()
        print("The orc healed for {} health!".format(healing))
        input("Press Enter to continue...")
    else:
        clear()
        print("Unexpected error: Invalid orc move")
        print("The game will now close")
        input("Press Enter to continue...")
        exit()


def end_fight():
    if not h.is_alive():
        clear()
        print("You died!")
        h.Health = h.MaxHealth
        h.CritChance = h.DefaultCritChance
        h.CritMult = h.DefaultCritMult
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
        h.CritMult = h.DefaultCritMult
    return 0


def fight():
    while h.is_alive() and o.is_alive():
        clear()
        print("{text:^40}".format(text="Lv.{level} {name}".format(level=o.Level, name=o.Name)))
        print("{text:^40}\n".format(text="Health: {health}/{max_health}".format(health=o.Health, max_health=o.MaxHealth)))
        print("{text:^40}".format(text="Lv.{level} {name} the {nickname}".format(level=h.Level,
                                                                                 name=h.Name, nickname=h.Nickname)))
        print("{text:^40}\n".format(text="Health: {health}/{max_health}".format(health=h.Health, max_health=h.MaxHealth)))
        for move in h.Moves:
            print("{id}. {move_name}".format(id=move[1], move_name=move[0]))
        choice = int(input("Choose an action: "))
        if not execute_hero_move(choice):
            clear()
            print("Invalid action!")
            input("Press Enter to continue...")
            continue
        if not o.is_alive():
            end_fight()
            break
        execute_orc_move(randint(1, 2))
        if not h.is_alive():
            end_fight()
            break
        continue


if first_time == 1:
    hero_name = input('Please input the Name of your character: ')
    clear()
    hero_nickname = input('Please input the Nickname of your character: ')
    clear()
    h = Hero(hero_name, 100, hero_nickname, 1, 0)
else:
    with open("save.txt", "rt") as f:
        stats = f.readlines()
        save_health = 100
        for i in range(2, int(stats[1]) + 1, 1):
            save_health += (int((10 + i - 2) / 2))
        stats[0] = stats[0].strip("\n")
        stats[2] = stats[2].strip("\n")
        h = Hero(stats[0], save_health, stats[2], int(stats[1]), int(stats[3]))

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
            orc_health += (int((10 + orc_level - 2) / 2))
        o = Orc("Orc", orc_health, float(randrange(100, 200, 1) / 100),
                orc_level, 10 * (orc_level + 1))
        fight()
    elif menu_choice == 2:
        with open("save.txt", "wt") as f:
            write_content = [h.Name, str(h.Level), h.Nickname, str(h.Experience)]
            for item in write_content:
                f.writelines(item + '\n')
            f.close()
            exit()
    else:
        clear()
        print("Invalid Choice!")
        input("Press Enter to continue...")
        continue






