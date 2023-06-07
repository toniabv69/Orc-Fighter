import pygame


class WeaponButton:
    def __init__(self, weapon_number: int, x: int, y: int, size_x: int, size_y: int,
                 inner: pygame.Rect, outer: pygame.Rect):
        self._WeaponNumber = weapon_number
        self._X = x
        self._Y = y
        self._SizeX = size_x
        self._SizeY = size_y
        self._Inner = inner
        self._Outer = outer

    def get_weapon_number(self):
        return self._WeaponNumber

    def get_pos(self):
        return self._X, self._Y

    def get_size(self):
        return self._SizeX, self._SizeY

    def get_inner(self):
        return self._Inner

    def get_outer(self):
        return self._Outer
