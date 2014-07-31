#!/usr/bin/env python
# coding: utf8
#from gluon.html import *
#from gluon.http import *
#from gluon.validators import *
#from gluon.sqlhtml import *
from collections import OrderedDict
from math import log, e, atan
from scipy.special import erfinv, erf
# request, response, session, cache, T, db(s)
# must be passed and cannot be imported!


double_attrib_mod_val = 20
attrib_mod_norm = 30
subskill_exp = 0.25
subskill_norm = 1 / 3.
skill_exp = 1.5
baselife = 100 / 75 ** (2 / 3.)
wound_exp = 200.
cyberhalf = 20

movement_mods = OrderedDict([
    ('standing', 0),
    ('crouching', 5),
    ('walking', -5),
    ('running', -10),
    ('sprinting', -20),
    ('crouch walking', 0),
    ('crawling', -20),
])

lighting_conditions = ['clear', 'badly lit office', 'streetlight', 'city glow', 'moonlight', 'starlight',
                       'overcast moonless night']
particle_conditions = ['clear', 'drizzle', 'light rain', 'heavy rain', 'thunderstorm', 'light fog (100m)',
                       'medium fog (50m)', 'heavy fog (10m)', 'light smoke', 'heavy smoke']


def attrib_mod(attribute, base):
    if not attribute:
        return float('-infinity')
    else:
        return double_attrib_mod_val * log(attribute / base) / log(2) + attrib_mod_norm


def calc_base_weight(weight_base, size, size_base):
    return (float(size) / size_base) ** 3 * weight_base


def calc_base_strength(strength_base, size, size_base, weight, weight_base):
    return (2 * (float(size) / size_base) ** 2 + (float(weight) / weight_base) ** (2 / 3.)) * strength_base / 3


def calc_agility_base(agility_base, weight, weight_base):
    return (float(weight) / weight_base) ** (-1 / 3.) * agility_base


def subskill_factor(percentage):
    return subskill_norm * ((1 / percentage) ** subskill_exp - 1) + 1


def exp_cost_skill(toval, fromval=float('-infinity'), factor=1):
    if fromval > toval:
        return 0
    if fromval == float('-infinity'):
        start = 0
    else:
        start = 1.5 ** (fromval / 10.) * factor * 100
    end = 1.5 ** (toval / 10.) * factor * 100
    return end - start


def exp_cost_attribute(value, base, factor=10000):
    if factor > 0:
        a = 1.8
        b = 2
    else:
        a = 2
        b = 1.8
    if value - base >= 0:
        if not base:
            amount = float('infinity') * factor
        else:
            amount = (b ** (float(value) / base) - b) * factor
    else:
        if not value:
            amount = float('-infinity') * factor
        else:
            amount = -(a ** (float(base) / value) - a) * factor
    return amount


def calc_charisma_degrade(cyberindex):
    return 1 / (1. + (cyberindex / cyberhalf) ** 2)


def life(weight, constitution):
    return weight ** (2 / 3.) * constitution / 30. * baselife


def woundlimit(weight, constitution):
    percent = 5 * (erf((1.05 ** constitution ** 0.2))) - 4.25
    return percent * life(weight, constitution)


def physical_initiative(intuition, intuitionbase, agility, agilitybase):
    intu = attrib_mod(intuition, intuitionbase)
    agil = attrib_mod(agility, agilitybase)
    return (intu + agil) / 2.


def physical_reaction(coordination, coordinationbase, agility, agilitybase):
    coord = attrib_mod(coordination, coordinationbase)
    agil = attrib_mod(agility, agilitybase)
    return (coord + agil) / 2. - attrib_mod_norm


def matrix_initiative(intuition, intuitionbase, processor, processorbase):
    intuition = attrib_mod(intuition, intuitionbase)
    processor = attrib_mod(processor, processorbase)
    return (intuition + processor) / 2.


def matrix_reaction(logic, logicbase, uplink, uplinkbase):
    logic = attrib_mod(logic, logicbase)
    uplink = attrib_mod(uplink, uplinkbase)
    return (logic + uplink) / 2. - attrib_mod_norm


def astral_initiative(intuition, intuitionbase, magic, magicbase):
    intu = attrib_mod(intuition, intuitionbase)
    magic = attrib_mod(magic, magicbase)
    return (intu + magic) / 2.


def astral_reaction(logic, logicbase, magic, magicbase):
    logic = attrib_mod(logic, logicbase)
    magic = attrib_mod(magic, magicbase)
    return (logic + magic) / 2. - attrib_mod_norm


#load modifier on speed/agility depending on load, strength, and weight
def loadeffect(load, strength=30, weight=75):
    mod = (strength - weight ** (2 / 3.))
    if mod < 1:
        mod = 1
    load /= mod
    percent = 1 - erf((load / 5.) ** 1.5)
    return percent


def loadeffect_inv(percent, strength=30, weight=75):
    load = erfinv(1 - percent) ** (1 / 1.5) * 5
    mod = (strength - weight ** (2 / 3.))
    if mod < 1:
        mod = 1
    load *= mod
    return load


#standing horizontal jump
#running horizontal jump
#standing vertical jump
#running vertical jump
def jumplimit(weight, strength, size):
    result = [0.8 * strength * weight ** (-0.7) * size / 1.75, 3 * strength * weight ** (-0.75) * size / 1.75,
              0.5 * strength * weight ** (-0.8) * size / 1.75, 1.5 * strength * weight ** (-0.9) * size / 1.75]
    return result


#speed depending on agility, weight, strength and size
def speed(agility, weight=75., strength=30., size=1.75):
    speed = (agility / 30) ** 0.2
    speed *= 4 ** min(0, (-weight ** (2 / 3.) / strength * 30 / 75 ** (2 / 3.) + 1))
    speed *= size / 1.75 * 1.5
    return [speed, speed * 3, speed * 5]


#speed depending on load carried
def loadspeed(agility, weight, strength, size, load):
    effect = loadeffect(load, strength, weight)
    loadspeed = speed(agility * effect, weight, strength, size)
    loadspeed = [i * effect for i in loadspeed]
    return loadspeed


# calculate ral awareness/time cost per action
def combatresource_by_attribute(value, attribute, frac, attribute2):
    if value == -1:
        cost = 10
    elif value == -2:
        cost = "variable"
    elif value == -3:
        cost = "feet only"
    elif value is None:
        cost = None
    else:
        cost = round(max(30 / attribute, 30 / frac / attribute2) * value, 2)
    return cost


def lifemod(life, maxlife):
    return (maxlife / float(life)) * (-10) + 10


#def warecostmult(effectmult=1, charmodmult=1, weightmult=1, kind="cyberware"):
#    mult = 2.5 ** (effectmult - 1.)
#    mult /= (charmodmult - 0.3) ** 2.2 * 2.191716170991387
#    if kind == "bioware":
#        mult *= (0.6 * atan(4 * (charmodmult - 1.1 + (effectmult - 1) / 3.)) + 1.23)
#    return mult

def warecostmult(effectmult=1, charmodmult=1, weightmult=1, kind="cyberware"):
    if kind == 'cyberware':
        mult = 3 ** (effectmult - 1.)
        mult *= 1 / charmodmult ** 2
    if kind == "bioware":
        mult = 5 ** (effectmult - 1.)
        mult *= 1 / charmodmult ** 1
    return mult


def warecost(basecost, cost, attributes, effectsmult, charmodmult=1, weightmult=1, kind='cyber'):
    return basecost + sum([attributes[i] * warecostmult(effectsmult[i], charmodmult, weightmult, kind)
                           for i in range(len(attributes))]) * 5000 + cost * warecostmult(1, charmodmult, weightmult,
                                                                                          kind)


def weapondamage(damage, testresult):
    if testresult > 50:
        testresult = 50
    if testresult > 0:
        result = damage * 2 ** (testresult / 10.)
    else:
        result = 0
    return result


def auto_fire_damage(basedamage, recoil, testresult, numbullets=float('inf')):
    damage = []
    while testresult >= 0 and numbullets >= 1:
        damage += [weapondamage(basedamage, testresult)]
        testresult -= recoil
        numbullets -= 1
    return damage


def armor_reduction(agility, coordination, maxagi=[], coordmult=[]):
    agility = min([agility] + maxagi)
    coordination *= reduce(lambda x, y: x * y, [1] + coordmult)
    return agility, coordination


def bleedingdamage_per_round(wounds, woundlimit):
    return wounds ** 3 * woundlimit / 20.


# healing time in days
def healingtime(damagepercent, base_healtime):
    return damagepercent ** 1.5 * base_healtime


def healing_mod(damagepercent):
    return damagepercent ** 1.5 * 30


def damage_heal_after_time(damage, days, healtime):
    return damage * (days / healtime) ** 1.5


def resist_drain(drain, willpower, resistbonus, roll):
    resist = log(willpower / 30) / log(2) * 10 + resistbonus + roll
    return drain * 2 ** (-resist / 10.)


def summoning_services(force, resistroll, skill, summonroll):
    forcemod = attrib_mod(force, 30)
    result = (skill + summonroll - forcemod - resistroll) / 10.
    if result > 0:
        result = 1 + int(result / 10.)
    else:
        result = 0
    return result


def summoning_drain(force):
    return force


def visible_perception_mod(size, distance, zoom):
    return abs(log(2 * zoom * size / distance) / log(2)) * -10


def percept_time(time):
    return log(time) / log(2) * 10


def percept_intens_sens(sensitivity, intensity, background):
    return min(0, intensity + sensitivity)


def percept_blind(sensitivity, background):
    return -min(0, background + sensitivity)


def shooting_difficulty(weaponrange, magnification, distance, size=1.):
    sightmod = visible_perception_mod(size, distance, magnification)
    rangemod = log(distance / float(weaponrange)) / log(2) * -10
    if rangemod > 0:
        rangemod = 0
    return - 40 - sightmod - rangemod


def matrix_action_rating(program_rating, matrix_attribute, skill):
    return (matrix_attribute + program_rating) / 2. + skill


def processor_cost(proc, size):
    return 2 ** ((proc + 50) / 4. - log(size) / log(5) - 1) * 0.004


def uplink_cost(up, size):
    return 2 ** ((up + 50) / 5.5 - log(size) / log(30) - 1) * 0.3


def size_cost(size):
    return size * 10000


def system_cost(system, processor):
    return 2 ** ((system + 50) / 6.5) * (processor + 50 + 5) ** 1.5 * 0.006


def maintain_cost(size):
    return size ** 1.5 * 100


def deck_cost(processor, system, uplink, size):
    cprocessor = processor_cost(processor, size)
    csystem = system_cost(system, processor)
    cuplink = uplink_cost(uplink, size)
    csize = size_cost(size)
    return cprocessor, csystem, cuplink, csize, sum([cprocessor, csystem, cuplink, csize])


def program_cost(rating):
    return 1.2 ** rating / 2.37


def firewall_rating(time, skill, system, users):
    #time in hours per week
    return log(skill ** 3 / (system + 50) ** 3 * time / 8. / users) * 10 + skill - 50