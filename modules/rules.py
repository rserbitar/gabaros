#!/usr/bin/env python
# coding: utf8
#from gluon.html import *
#from gluon.http import *
#from gluon.validators import *
#from gluon.sqlhtml import *
from collections import OrderedDict
from math import log, e, atan
from scipy.special import erfinv, erf
from random import gauss
# request, response, session, cache, T, db(s)
# must be passed and cannot be imported!


double_attrib_mod_val = 10
attrib_mod_norm = 30
subskill_exp = 0.25
subskill_norm = 1 / 3.
skill_exp = 1.5
baselife = 100.
baseweight = 75.
baseagility = attrib_mod_norm
baseconstitution = attrib_mod_norm
baseintuition = attrib_mod_norm
baselogic = attrib_mod_norm
basemagic = attrib_mod_norm
baseuplink = attrib_mod_norm
wound_exp = 200.
cyberhalf = 20
shoot_base_difficulty = 20
spell_xp_cost = 200
money_to_xp = 1/60.
xp_to_money = 40.
starting_money = 150000
starting_xp = 10000

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


def die_roll():
    return gauss(0,10)


def attrib_mod(attribute, base):
    if not attribute:
        return float('-infinity')
    else:
        return double_attrib_mod_val * log(attribute / base) / log(2)


def calc_base_weight(weight_base, size, size_base):
    return (float(size) / size_base) ** 3 * weight_base


def calc_base_strength(strength_base, size, size_base, weight, weight_base):
    return (2 * (float(size) / size_base) ** 2 + (float(weight) / weight_base) ** (2 / 3.)) * strength_base / 3


def calc_agility_base(agility_base, weight, weight_base):
    return (float(weight) / weight_base) ** (-1 / 3.) * agility_base


def get_skill_xp_cost(value):
    return (2**abs(value/10.)-1)*25


def get_attrib_xp_cost(attrib):
    val = (attrib)/30.
    if val >= 1:
        sign = 1
    else:
        sign = -1
        val = 1./val
    return (2**abs(val-1)-1)*1000*sign


def exp_cost_attribute(attribute, value, base, factor, signmod):
    if value == 0:
        return 0
    val = float(value)/base
    if val >= 1:
        sign = 1
    else:
        sign = -1 * signmod
        val = 1./val
    val = (val -1)
    val = (2**val-1)*factor*sign
    if val < -factor/2.:
        val = -factor/2.
    if attribute == 'Magic':
        val += factor
    return val


def get_spell_xp_cost():
    return spell_xp_cost

def calc_charisma_degrade(cyberindex):
    return 1 / (1. + (cyberindex / cyberhalf) ** 2)


def life(weight, constitution):
    return (weight/baseweight) ** (2 / 3.) * constitution / baseconstitution * baselife


def woundlimit(weight, constitution):
    percent = 5 * (erf((1.0123 ** constitution ** 0.4))) - 4.21
    lifeval = life(weight, constitution)
    return percent *lifeval


def wounds_for_incapacitated_thresh(weight, constitution):
    return 3


def wounds_for_destroyed_thresh(weight, constitution):
    return 5


def woundeffect(attribute, wounds, weight, constitution):
    return attribute * (0.5)**(wounds * wounds_for_incapacitated_thresh(weight, constitution)/3.)


def action_cost(kind, actionmult):
    action_cost_dict = {'Free': 5,
                        'Simple': 10,
                        'Complex': 20}
    return round(action_cost_dict.get(kind, 20) * actionmult ,0)

def physical_actionmult(agility_mod, coordination_mod, intuition_mod):
    return 2**((agility_mod+coordination_mod+intuition_mod)/-60.)


def matrix_actionmult(uplink_mod, logic_mod, intuition_mod):
    return 2**((uplink_mod + logic_mod + intuition_mod)/-60.)


def astral_actionmult(magic_mod, charisma_mod, intuition_mod):
    return 2**((magic_mod + charisma_mod + intuition_mod)/-60.)


def physical_reaction(agility_mod, intuition_mod):
    return (agility_mod + intuition_mod) / 2.


def matrix_reaction(logic_mod, uplink_mod):
    return (logic_mod + uplink_mod) / 2.


def astral_reaction(intuition_mod, magic_mod):
    return (intuition_mod + magic_mod) / 2.


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
    result = [0.8 * strength * weight ** (-0.7) * size / 1.75,
              3 * strength * weight ** (-0.75) * size / 1.75,
              0.5 * strength * weight ** (-0.8) * size / 1.75,
              1.5 * strength * weight ** (-0.9) * size / 1.75]
    return result


#speed depending on agility, weight, strength and size
def speed(agility, weight=75., strength=30., size=1.75):
    speed = (agility / 30.) ** 0.2
    speed *= 4. ** min(0, (-weight ** (2 / 3.) / strength * 30. / 75 ** (2 / 3.) + 1))
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


def lifemod_absolute(life, maxlife):
    return log(max(1, maxlife / float(life)))/log(2)*-10

def lifemod_relative(life, maxlife):
    return max(1, maxlife / float(life))**(1/3.)

#def warecostmult(effectmult=1, charmodmult=1, weightmult=1, kind="cyberware"):
#    mult = 2.5 ** (effectmult - 1.)
#    mult /= (charmodmult - 0.3) ** 2.2 * 2.191716170991387
#    if kind == "bioware":
#        mult *= (0.6 * atan(4 * (charmodmult - 1.1 + (effectmult - 1) / 3.)) + 1.23)
#    return mult


def warecost(cost, effectmult = 1, essencemult = 1., kind = 'cyberware'):
    finalcost = 0
    if kind == 'cyberware':
        finalcost = cost * 5**(effectmult-1.) * 10**(1./essencemult-1.)
    elif kind == 'bioware':
        finalcost = cost * 7**(effectmult-1.) * 5**(1./essencemult-1)
    return finalcost


#def warecost(basecost, cost, attributes, effectsmult, charmodmult=1, weightmult=1, kind='cyber'):
#    return basecost + sum([attributes[i] * warecostmult(effectsmult[i], charmodmult, weightmult, kind)
#                           for i in range(len(attributes))]) * 5000 + cost * warecostmult(1, charmodmult, weightmult,
#                                                                                          kind)

def essence_charisma_mult(essence):
    mult = max(0, 0.5 + essence/200.)
    return mult

def essence_magic_mult(essence):
    mult = max(0,essence/100.)
    return mult

def essence_psycho_thresh(essence):
    return log(1./(1-(essence/100.)))/log(2)*10+10 if essence < 100 else float('inf')


def spomod_max(logic):
    return logic/2.


def weapondamage(damage, testresult):
    if testresult > 60:
        testresult = 60
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


def bleedingdamage_per_round(wounds, woundlimit):
    return wounds ** 3 * woundlimit / 20.


# healing time in days
def healingtime(damagepercent, base_healtime):
    return damagepercent ** 1.5 * base_healtime


def healing_mod(damagepercent):
    return damagepercent ** 1.5 * 30


def damage_heal_after_time(damage, days, healtime):
    return damage * (days / healtime) ** 1.5


def resist_damage(damage, attribute_mod, roll, resistmod = 0):
    resist = attribute_mod - resistmod + roll
    return damage * 2 ** (-resist / 10.)


def drain_resist(willpower_mod, magic_mod):
    return (willpower_mod + magic_mod)/2.


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


def distance_modifier(distance):
    return log(distance)/log(2.)*10 -30


def size_modifier(size):
    return log(size)/log(2.)*-10 -20


def visible_perception_mod(size, distance, zoom):
    distance_mod = distance_modifier(distance)
    size_mod = size_modifier(size*zoom)
    return distance_mod + size_mod


def percept_time(time):
    return log(time) / log(2) * 10


def percept_intens_sens(sensitivity, intensity, background):
    return min(0, intensity + sensitivity)


def percept_blind(sensitivity, background):
    return -min(0, background + sensitivity)


def shooting_difficulty(weaponrange, magnification, distance, size=2.):
    sightmod = visible_perception_mod(size, distance, magnification)
    rangemod = shoot_rangemod(weaponrange, distance)
    return shoot_base_difficulty + sightmod + rangemod

def shoot_rangemod(weaponrange, distance):
    if distance < 1:
        distance = 1
    rangemod = log(distance / float(weaponrange)) / log(2) * 10
    if rangemod < 0:
        rangemod = 0
    return rangemod


def weapon_minstr_mod(minimum_strength, strength):
    return max(0, log(minimum_strength/strength)/log(2) * 20)


def matrix_action_rating(program_rating, matrix_attribute, skill):
    return (matrix_attribute + program_rating) / 4. + skill/2.


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


def cost_by_rating(cost, basecost, rating):
    return 5**(rating/10.)/125. * cost + basecost


def firewall_rating(time, skill, system, users):
    #time in hours per week
    return log(skill ** 3 / (system + 50) ** 3 * time / 8. / users) * 10 + skill - 50


def square_add(values):
     return sum([i**2 for i in values])**0.5


def negative_square_add(values):
    return (1./sum([(1./i)**2 for i in values]))**0.5


def get_armor_agility(agility, max_agility):
    if isinstance(max_agility, list):
        max_agility = negative_square_add(max_agility)
    return min(agility, max_agility)


def get_armor_coordination(coordination, coordination_multiplier):
    if isinstance(coordination_multiplier, list):
        coordination_multiplier = reduce(lambda x, y: x * y, [1] + coordination_multiplier)
    return coordination * coordination_multiplier


def get_stacked_armor_value(values):
    return square_add(values)

def scale(x):
    2**(x/10.)

def price_by_rating(baseprice, rating):
    return (1+(2**(rating/10.)))/9.*baseprice

def contact_costs(loyalty, rating):
    return 2**((loyalty/30.)**2+(30/30.)**2)*50

def contacts_free_value(charisma):
    return charisma*charisma
