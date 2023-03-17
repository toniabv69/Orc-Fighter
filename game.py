from orc import Orc
from swordsman import Swordsman
from item import Item
from healer import Healer
from tank import Tank
from mage import Mage
from random import randrange, randint
from os import system, path, name, remove, path

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
        h.spend_mana(h.get_moves()[n][4])
        damage = int(randrange(h.get_moves()[n][2], h.get_moves()[n][3], 1) * h.get_level_attack_mult() *
                     h.get_attack_mult())
        items = h.get_equipped_items()
        for item in items:
            if item.get_amplifier_type() == 0:
                damage = int(damage + (damage * item.get_amplifier()))
        if is_crit(h.get_crit_chance()):
            damage = int(damage * h.get_crit_mult())
            print("You landed a critical hit!")
        o.take_damage(damage)
        print("You dealt {} damage!".format(damage))
        input("Press Enter to continue...")
        return True
    elif move_type == 1:
        h.spend_mana(h.get_moves()[n][4])
        healing = int(randrange(h.get_moves()[n][2], h.get_moves()[n][3], 1) * h.get_level_attack_mult())
        items = h.get_equipped_items()
        for item in items:
            if item.get_amplifier_type() == 1:
                healing = int(healing + (healing * item.get_amplifier()))
        h.take_healing(healing)
        clear()
        print("You healed for {} health!".format(healing))
        input("Press Enter to continue...")
        return True
    elif move_type == 2:
        clear()
        h.spend_mana(h.get_moves()[n][4])
        h.focus(n)
        print("You became focused! Your critical hit chance increased!")
        input("Press Enter to continue...")
        return True
    elif move_type == 3:
        mana = int(randrange(h.get_moves()[n][2], h.get_moves()[n][3], 1))
        items = h.get_equipped_items()
        for item in items:
            if item.get_amplifier_type() == 3:
                mana = int(mana + (mana * item.get_amplifier()))
        h.regen_mana(mana)
        clear()
        print("You restored {} mana!".format(mana))
        input("Press Enter to continue...")
        return True
    elif move_type == 4:
        clear()
        h.spend_mana(h.get_moves()[n][4])
        h.rage(n)
        print("You were consumed by rage! You now deal more damage!")
        input("Press Enter to continue...")
        return True
    else:
        return False


def execute_orc_move(n, move_type):
    if move_type == 0:
        o.spend_mana(o.get_moves()[n][4])
        damage = int(randrange(o.get_moves()[n][2], o.get_moves()[n][3], 1) *
                     o.get_level_attack_mult() * o.get_berserk_factor())
        items = h.get_equipped_items()
        for item in items:
            if item.get_amplifier_type() == 2:
                damage -= int(damage * item.get_amplifier())
        h.take_damage(damage)
        clear()
        print("You took {} damage!".format(damage))
        input("Press Enter to continue...")
    elif move_type == 1:
        o.spend_mana(o.get_moves()[n][4])
        healing = int(randrange(o.get_moves()[n][2], o.get_moves()[n][3], 1) * o.get_level_attack_mult())
        o.take_healing(healing)
        clear()
        print("The orc healed for {} health!".format(healing))
        input("Press Enter to continue...")
    elif move_type == 3:
        mana = int(randrange(o.get_moves()[n][2], o.get_moves()[n][3], 1))
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
        h.set_health(h.get_max_health())
        h.set_crit_chance(h.get_default_crit_chance())
        h.set_mana(h.get_max_mana())
        input("Press Enter to continue...")
    if not o.is_alive():
        clear()
        print("You were victorious!")
        input("Press Enter to continue...")
        h.give_gold(o.get_gold_reward())
        clear()
        print("You earned {} gold!".format(o.get_gold_reward()))
        input("Press Enter to continue...")
        clear()
        print("You earned {} experience!".format(o.get_exp_reward()))
        input("Press Enter to continue...")
        if h.give_experience(o.get_exp_reward()):
            clear()
            print("You leveled up to level {}!".format(h.get_level()))
            input("Press Enter to continue...")
        h.set_health(h.get_max_health())
        h.set_crit_chance(h.get_default_crit_chance())
        h.set_mana(h.get_max_mana())
    return 0


def fight():
    while h.is_alive() and o.is_alive():
        clear()
        print("{text:^40}".format(text="Lv.{level} {name}".format(level=o.get_level(),
                                                                  name=o.get_name())))
        print("{text:^40}".format(text="Health: {health}/{max_health}".format(health=o.get_health(),
                                                                              max_health=o.get_max_health())))
        print("{text:^40}\n".format(text="Mana: {mana}/{max_mana}".format(mana=o.get_mana(),
                                                                          max_mana=o.get_max_mana())))
        print("{text:^40}".format(text="Lv.{level} {name} the {nickname}".format(level=h.get_level(),
                                                                                 name=h.get_name(),
                                                                                 nickname=h.get_nickname())))
        print("{text:^40}".format(text="Health: {health}/{max_health}".format(health=h.get_health(),
                                                                              max_health=h.get_max_health())))
        print("{text:^40}\n".format(text="Mana: {mana}/{max_mana}".format(mana=h.get_mana(),
                                                                          max_mana=h.get_max_mana())))
        for move in h.get_moves():
            print("{id}. {move_name}   Mana Cost: {mana_cost}".format(id=move[1], move_name=move[0], mana_cost=move[4]))
        choice = int(input("Choose an action: "))
        if choice > 5 or choice < 1:
            clear()
            print("Invalid action!")
            input("Press Enter to continue...")
            continue
        if not h.get_mana() < h.get_moves()[choice - 1][4]:
            if not execute_hero_move(choice - 1, h.get_moves()[choice - 1][5]):
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
        execute_orc_move(orc_move - 1, o.get_moves()[orc_move - 1][5])
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
        h = Swordsman(hero_name, 110, hero_nickname, 1, 0, 100, 1.1, hero_class, 0, [])
    elif hero_class == 2:
        h = Healer(hero_name, 90, hero_nickname, 1, 0, 120, 0.9, hero_class, 0, [])
    elif hero_class == 3:
        h = Tank(hero_name, 130, hero_nickname, 1, 0, 90, 1.3, hero_class, 0, [])
    elif hero_class == 4:
        h = Mage(hero_name, 75, hero_nickname, 1, 0, 150, 0.75, hero_class, 0, [])
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
            clear()
            print("Unexpected error: Corrupted Save File! Please delete it and start over!")
            print("The game will now close")
            input("Press Enter to close the game...")
            exit()

while True:
    clear()
    print("Orc Fighter\n")
    print("1. Fight")
    print("2. Shop")
    print("3. Inventory")
    print("4. Delete Save")
    print("5. Save & Exit")
    print("6. Exit Without Saving")

    menu_choice = int(input('Please make a selection: '))
    if menu_choice == 1:
        clear()
        orc_level = int(input("Please choose an orc level to fight (Your level is {}): ".format(h.get_level())))
        orc_health = 100
        orc_gold = orc_level * 10
        if orc_gold < 0:
            orc_gold = 0
        for i in range(2, orc_level + 1, 1):
            orc_health += (int(i * 1.5))
        o = Orc("Orc", orc_health, float(randrange(100, 200, 1) / 100),
                orc_level, int(10 * (orc_level + 1) * (orc_level / 2)), 100, 1, orc_gold)
        fight()
    elif menu_choice == 2:
        while True:
            clear()
            print("Shop\n")
            print("1. Buy")
            print("2. Sell")
            print("3. Exit")
            main_shop_choice = int(input("Please make a selection: "))
            if main_shop_choice == 1:
                while True:
                    clear()
                    print("Items for your class: \n")
                    counter = 0
                    shop_items = []
                    for item in h.get_class_items():
                        if item not in h.get_items():
                            counter += 1
                            print(str(counter) + ". " + str(item) + "  Cost: " + str(item.get_cost()))
                            shop_items.append(item)
                    counter += 1
                    print(str(counter) + ". Exit")
                    print("\nYour Gold: {}".format(h.get_gold()))
                    shop_choice = int(input("\nPlease choose an item to buy (or exit the menu): "))
                    if shop_choice > counter or shop_choice < 1:
                        clear()
                        print("Invalid action!")
                        input("Press Enter to continue...")
                        continue
                    elif shop_choice == counter:
                        break
                    elif h.get_gold() < shop_items[shop_choice - 1].get_cost():
                        clear()
                        print("Not enough gold!")
                        input("Press Enter to continue...")
                        continue
                    else:
                        clear()
                        print("You spent {} gold to buy {}! It was automatically equipped!".format(shop_items[shop_choice - 1]
                                                                                                   .get_cost(),
                                                                                                   shop_items[shop_choice - 1]))
                        h.spend_gold(shop_items[shop_choice - 1].get_cost())
                        h.add_item(shop_items[shop_choice - 1])
                        h.equip_item(shop_items[shop_choice - 1].get_id())
                        input("Press Enter to continue...")
            elif main_shop_choice == 2:
                while True:
                    clear()
                    print("Your gold: {}\n".format(h.get_gold()))
                    print("Your items:")
                    counter = 0
                    sell_items = []
                    for item in h.get_items():
                        counter += 1
                        print(str(counter) + ". " + str(item) + "  Sell Price: " + str(int(item.get_cost() / 2)))
                        sell_items.append(item)
                    counter += 1
                    print(str(counter) + ". Exit")
                    sell_choice = int(input("\nPlease choose an item to sell (or exit the menu): "))
                    if sell_choice > counter or sell_choice < 1:
                        clear()
                        print("Invalid action!")
                        input("Press Enter to continue...")
                        continue
                    elif sell_choice == counter:
                        break
                    else:
                        clear()
                        h.unequip_item(sell_items[sell_choice - 1].get_id())
                        h.remove_item(sell_items[sell_choice - 1])
                        h.give_gold(int(sell_items[sell_choice - 1].get_cost() / 2))
                        print("You have sold your {} for {} gold!".format(sell_items[sell_choice - 1],
                                                                          int(sell_items[sell_choice - 1].get_cost() / 2)))
                        input("Press Enter to continue...")
            elif main_shop_choice == 3:
                break
            else:
                clear()
                print("Invalid action!")
                input("Press Enter to continue...")
                continue
    elif menu_choice == 3:
        while True:
            clear()
            print("Your gold: {}\n".format(h.get_gold()))
            print("Your items:")
            counter = 0
            inv_items = []
            for item in h.get_items():
                counter += 1
                if item in h.get_equipped_items():
                    print(str(counter) + ". " + str(item) + "  Equipped")
                else:
                    print(str(counter) + ". " + str(item) + "  Unequipped")
                inv_items.append(item)
            counter += 1
            print(str(counter) + ". Exit")
            inv_choice = int(input("\nPlease choose an item to equip/unequip (or exit the menu): "))
            if inv_choice > counter or inv_choice < 1:
                clear()
                print("Invalid action!")
                input("Press Enter to continue...")
                continue
            elif inv_choice == counter:
                break
            else:
                clear()
                if not inv_items[inv_choice - 1] in h.get_equipped_items():
                    clear()
                    h.equip_item(inv_items[inv_choice - 1].get_id())
                    print("You equipped {}!".format(inv_items[inv_choice - 1]))
                    input("Press Enter to continue...")
                else:
                    clear()
                    h.unequip_item(inv_items[inv_choice - 1].get_id())
                    print("You unequipped {}!".format(inv_items[inv_choice - 1]))
                    input("Press Enter to continue...")
    elif menu_choice == 4:
        clear()
        if path.exists("save.txt"):
            remove("save.txt")
            print("Your save file has been successfully deleted!")
            input("Press Enter to continue...")
        else:
            print("There was no save file to delete!")
            input("Press Enter to continue...")
    elif menu_choice == 5:
        with open("save.txt", "wt") as f:
            write_content = [h.get_name(), str(h.get_level()), h.get_nickname(), str(h.get_experience()),
                             str(h.get_classid()), str(h.get_gold())]
            for item in write_content:
                f.writelines(item + '\n')
            for item in h.get_items():
                f.writelines(str(item.get_id()) + '\n')
            f.close()
            clear()
            exit()
            # save is in this order: name, level, nickname, experience, class_id(1 - Swordsman, 2 - Healer,
            # 3 - Tank, 4 - Mage), gold, items(using class item ids, each one is on new line)
    elif menu_choice == 6:
        clear()
        exit()
    else:
        clear()
        print("Invalid Choice!")
        input("Press Enter to continue...")
        continue
