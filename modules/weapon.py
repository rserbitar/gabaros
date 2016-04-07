#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gluon import *
from collections import namedtuple, OrderedDict
import rules

class Weapon():

    def __init__(self):
        self.name = ''
        self.skill = ''

        self.minimum_strength = 0
        self.hands = 0

        self.damage = 0
        self.damage_type = ''
        self.penetration = 0

        self.range = 0

        self.shot = 0
        self.burst = 0
        self.auto = 0
        self.recoil = 0

        self.magazine_size = 0
        self.magazine_kind = 0
        self.size = 0
        self.visible_stealth = 0
        self.scan_stealth = 0

        self.weight = 0
        self.cost = 0

    def basic_by_strength(self, strength):
        self.shot = 1
        self.burst = 3
        self.auto = 8

        self.damage = strength/3.
        self.penetration = strength/1.8
        self.range = strength*2.
        self.calc_rest()


    def calc_rest(self):
        self.weight = ((self.damage/12. * self.penetration/20.)**0.5 * 2 +
                       (self.damage / 12. * self.penetration / 20.) ** 0.5 * max(self.auto, self.burst)/8. * 0.5 +
                       (self.damage / 12. * self.penetration / 20. * self.range/72.)**(1/3.)*1.)
        self.minimum_strength = self.weight/3.5*36

    def __repr__(self):
        result =  """Weapon:
Damage:             {},
Penetration:        {},
Range:              {}m,
Weight:             {}kg,
Mininum Strength:   {}
""".format(self.damage,
           self.penetration,
           self.range,
           self.weight,
           self.minimum_strength)
        return result



