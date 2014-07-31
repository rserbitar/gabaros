# !/usr/bin/env python
# coding: utf8
import basic


class CharPropertySetter(basic.Char):
    def __init__(self, char):
        """"
        :param char: the character for witch to get the attribute
        """

        basic.Char.__init__(self, char)

    def set_attribute(self, attribute, payexp=True):
        """

        :param attribute: the attribute to set
        :param payexp: weather to pay experience points
        """
        pass

    def set_skill(self, skill, payexp=True):
        """

        :param skill: the skill to set
        :param payexp: weather to pay experience points
        """
        pass

    def apply_damage(self, damage, kind):
        """

        :param damage: the ammount of damage, if 'x%' percent damage is used
        :param kind: the damage kind
        """
        pass

    def heal_damage(self, time, treatment):
        """

        :param time:
        :param treatment:
        """
        pass