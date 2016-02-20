#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from collections import namedtuple, OrderedDict
import rules

def spirit_scaling(force):
    return 2**((force-30)/20.)*30

spirit_stats = [
    ['class_', 'charisma', 'intuition', 'logic', 'willpower', 'base_skills', 'standard_skills', 'exceptional_skills', 'powers', 'optional_powers'],
    ['creation', 1.25, 1, 0.8, 1, ['Orientation', 'Athletics', 'Acrobatics', 'Metamagic'], ['Assensing', 'Astral Combat', 'Unarmed Combat'], [],
     ['Concealment', 'Protection'], ['Skill: Counterspelling', 'Innate Spell: Creation', 'Metamagic: Shielding']],
    ['destruction', 0.8, 1, 1, 1.25, ['Orientation', 'Atheletics', 'Assensing', 'Metamagic'], ['Unarmed Combat', 'Acrobatics'], ['Astral Combat'],
     ['Ranged Attack'], ['Innate Spell: Destruction', 'Metmamagic: Transfusion']],
    ['detection', 1, 1.25, 1, 0.8, ['Athletics', 'Acrobatics', 'Astral Combat', 'Metamagic'], ['Orientation'], ['Assensing'],
     ['Search', 'Enlightenment'], ['Skill: Judge Person', 'Innate Spell: Detection', 'Metmamagic: Divination']],
    ['manipulation', 1, 0.8, 1.25, 1, ['Orientation', 'Athletics', 'Unarmed Combat', 'Acrobatics', 'Metamagic'], ['Assensing', 'Astral Combat'], [],
     ['Movement', 'Confusion'], ['Skill: Stealth', 'Skill: Interaction', 'Skill: Discussion','Innate Spell: Manipulation', 'Metmamagic: Masking', 'Metmamagic: Flexible Signature']]
]

spirit_stats_nt = namedtuple('spirit_stat', ['id'] + spirit_stats[0])
spirit_stats_dict = OrderedDict([(entry[0], spirit_stats_nt(*([i] + entry))) for i, entry in enumerate(spirit_stats[1:])])

manifestation_stats = [
    ['class_', 'agility', 'constitution', 'coordination', 'strength', 'size', 'weight', 'life', 'armor', 'damage', 'penetration', 'powers', 'physical_powers'],
    ['ethereal', 90, 1, 1, 0.5, 0.8, 0.05, 0.1, 1, 0, 0, ['Ethereal', 'Vulnerabiliy to Magic Weapons'], ['Aura']],
    ['fluid', 60, 1, 1, 1, 1, 1., 0.5, 1.5, 0.5, 0.5, ['Fluid', 'Sensitivity to Magic Weapons'], ['Engulf']],
    ['solid', 30, 1, 1, 1.5, 1.2, 1.5, 1, 2, 1, 1, ['Structureless'], ['Increased Armor']],
]

manifestation_stats_nt = namedtuple('manifestation_stat', ['id'] + manifestation_stats[0])
manifestation_stats_dict = OrderedDict([(entry[0], manifestation_stats_nt(*([i] + entry))) for i, entry in enumerate(manifestation_stats[1:])])

class Spirit(object):

    def __init__(self, force, class_, manifestation):
        self.force = force
        self.class_ = class_
        self.manifestation = manifestation
        self.agility = manifestation_stats_dict[manifestation].agility
        self.strength = manifestation_stats_dict[manifestation].strength * spirit_scaling(force)
        self.coordination = manifestation_stats_dict[manifestation].coordination * spirit_scaling(force)
        self.constitution = manifestation_stats_dict[manifestation].constitution * spirit_scaling(force)
        self.size = manifestation_stats_dict[manifestation].size * force**0.5 * 1.75 / (30)**0.5
        self.weight = manifestation_stats_dict[manifestation].weight * rules.calc_base_weight(rules.baseweight, self.size, 1.75)
        self.logic = spirit_stats_dict[class_].logic * spirit_scaling(force)
        self.intuition = spirit_stats_dict[class_].intuition * spirit_scaling(force)
        self.willpower = spirit_stats_dict[class_].willpower * spirit_scaling(force)
        self.charisma = spirit_stats_dict[class_].charisma * spirit_scaling(force)
        self.magic = self.force
        self.armor = manifestation_stats_dict[manifestation].armor * spirit_scaling(force)
        self.life = spirit_scaling(force)/30.*100 * manifestation_stats_dict[manifestation].life
        self.base_skill = self.force
        self.skills = {}
        self.damage = spirit_scaling(force) * 20 * manifestation_stats_dict[manifestation].damage
        self.penetration = spirit_scaling(force) * 10 * manifestation_stats_dict[manifestation].penetration
        for skill in spirit_stats_dict[class_].base_skills:
            self.skills[skill] = self.force * 0.75
        for skill in spirit_stats_dict[class_].standard_skills:
            self.skills[skill] = self.force
        for skill in spirit_stats_dict[class_].exceptional_skills:
            self.skills[skill] = self.force * 1.25
        self.metamagic = []
        self.powers = ['Manifestation', 'Immunity to Drugs and Toxins'] + spirit_stats_dict[class_].powers + manifestation_stats_dict[manifestation].powers
        self.optional_powers = spirit_stats_dict[class_].optional_powers
        self.physical_powers = manifestation_stats_dict[manifestation].physical_powers
