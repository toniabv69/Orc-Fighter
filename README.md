# Orc-Fighter
A little game I made about fighting orcs!

Notes:
- As it turned out - the game executable was getting detected as a false positive.
- The save file is easily editable - the name, level, nickname and experience are stored in .txt format.
- This project was actually born from my Python OOP introduction homework!
- The class information was posted here because I'm too lazy to implement a description menu in the game :P

Changelog:

- v1.0:
Added basic moves and calculations for heroes and orcs.
Added critical hits.
Added basic text GUI.

- v1.1:
Added mana system.
Added character classes:

Swordsman:
- has slightly more HP
- has default mana.
- has more attack but less healing.
- has special move Ultimate Slash which costs more mana but deals more damage.

Healer:
- has slightly less HP
- has some more mana.
- has less attack but more healing.
- has special move Ultimate Regen which costs more mana but heals more health.

Tank:
- has way more HP
- has slightly less mana.
- has slightly less attack but slightly more healing.
- has special move Ultimate Rage which costs a lot of mana but increases his attacks for the enitre rest of the fight.

Mage:
- has way less HP
- has way more mana
- has more attack but slightly less healing.
- has both Ultimate Attack and Ultimate Regen, with Ultimate Attack behaving the same as Ultimate Slash.
- only class which can't deal critical hits.

- v1.2:
Added shop and gold system.
Added item system, where the items are unique to each class. They work kinda like the bytes from FNaF World - multiple items can be equipped at a time, even when they are of the same type. They will also not be purchaseable and will be permanently equipped (this will most likely be changed in a future update).

- v1.3:
Added buy and sell menus to shop.
Added weapon type checking, now only one weapon of each type can be equipped at a time (you can tell the weapon type from the second word of the name).
Added A-10 Thunderbolt, exclusive to the mage. It gets summoned in by the mage to help with attacking, that's why it's exclusive.

This file will be updated in the future if I decide to make any more updates.
