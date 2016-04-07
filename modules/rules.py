#!/usr/bin/env python
# coding: utf8
#from gluon.html import *
#from gluon.http import *
#from gluon.validators import *
#from gluon.sqlhtml import *
from collections import OrderedDict
from math import log, e, atan
from math import erf
from random import gauss, random
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
metamagic_xp_cost = 400
money_to_xp = 1/(50*2**0.5)
xp_to_money = 50/(2**0.5)
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


gas_vent_recoil = 2/3.


def die_roll():
    return gauss(0,10)


def attrib_mod(attribute, base):
    if not attribute or attribute < 0:
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


def get_spell_xp_cost(spells):
    return  (2**(len(spells)/10.)-1)*spell_xp_cost/(2**0.1-1)


def get_metamagic_xp_cost(magics):
    return (2**(len(magics)/2.)-1)*metamagic_xp_cost/(2**0.5-1)


def calc_charisma_degrade(cyberindex):
    return 1 / (1. + (cyberindex / cyberhalf) ** 2)


def life(weight, constitution):
    return (weight/baseweight) ** (2 / 3.) * constitution / baseconstitution * baselife


def woundlimit(weight, constitution):
    percent = 5 * (erf((1.0123 ** constitution ** 0.4))) - 4.21
    lifeval = life(weight, constitution)
    return percent *lifeval


def wounds_for_incapacitated_thresh(weight, constitution, bodypart):
    wounds = 3
    if bodypart.lower() == 'body':
        wounds *= 7
    return wounds


def wounds_for_destroyed_thresh(weight, constitution, bodypart):
    wounds = 5
    if bodypart.lower() == 'body':
        wounds *= 7
    return wounds

    
def woundeffect(attribute, wounds, weight, constitution, bodypart):
    return attribute * (0.5)**(wounds * wounds_for_incapacitated_thresh(weight, constitution, bodypart)/3.)


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
    #load = erfinv(1 - percent) ** (1 / 1.5) * 5
    load = 0
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
    if life <= 0:
        return -float('inf')
    return log(max(1, maxlife / float(life)))/log(2)*-10

def lifemod_relative(life, maxlife):
    if life <= 0:
        return 0
    return min(1, float(life)/maxlife)**(1/3.)

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
    return log(1./(1-(essence/100.)))/log(2)*10+5 if essence < 100 else float('inf')


def spomod_max(logic):
    return logic/2.


def damage_location():
    value = random()
    result = 'Body'
    if value < .05:
        result = 'Head'
    elif value < .40:
        result = 'Upper Torso'
    elif value < .60:
        result = 'Lower Torso'
    elif value < .70:
        result = 'Right Arm'
    elif value < .80:
        result = 'Left Arm'
    elif value < .9:
        result = 'Right Leg'
    elif value < 1:
        result = 'Left Leg'
    return result


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
def healingtime(damagepercent, base_healtime, test):
    return damagepercent ** 1.5 * base_healtime / scale(test)


def healingtime_wounds(wounds, base_healtime, test):
    return wounds**2 * base_healtime/2. / scale(test)


def damage_heal_after_time(damage, days, healtime):
    return damage * (days / healtime) ** 1.5


def wound_heal_after_time(wounds, days, healtime):
    return int(wounds * (days / healtime) ** 1.5)


def healing_mod(damagepercent):
    return damagepercent ** 2. * 30


def firt_aid(test_value):
    if test_value > 0:
        healed = 0.05*scale(test_value)
    elif test_value > -10:
        healed = 0
    else:
        healed = -0.05*scale(-test_value+10)
    return healed


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


def shooting_difficulty(weaponrange, magnification, distance, size=2., wide_burst_bullets=0):
    sightmod = visible_perception_mod(size, distance, magnification)
    rangemod = shoot_rangemod(weaponrange, distance)
    bulletmod = wide_burst_bullets
    return shoot_base_difficulty + sightmod + rangemod + wide_burst_bullets

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
    return negative_square_avg([(matrix_attribute + program_rating) / 2, skill])


def processor_cost(processor, volume):
    return 11**(processor/10.-log(volume)/5.)/200.


def uplink_cost(uplink, volume):
    return 6**(uplink/10.+log(volume)/10.+1.)/2.


def signal_cost(signal, volume):
    return 20**(signal/10.-log((volume)**(1/3.))/3.-2.5)


def size_cost(volume):
    return volume * 1000


def system_cost(system, processor):
    result = 0
    if system > processor:
        result = 6**(((system**10+processor**10)/2.)**(1/10.)/10.)*2
    elif system <= processor:
        result = 6**((system+processor)/20.)*2
    return result

#def system_cost2(system, processor):
#   return  6**((system+processor)/20.)*2.

def maintain_cost(size):
    return size ** 1.5 * 100


def deck_cost(processor, system, uplink, signal, volume):
    cprocessor = processor_cost(processor, volume)
    csystem = system_cost(system, processor)
    cuplink = uplink_cost(uplink, volume)
    cvolume = size_cost(volume)
    csignal = signal_cost(signal, volume)
    return cprocessor, csystem, cuplink, csignal, cvolume, sum([cprocessor, csystem, csignal, cuplink, cvolume])


def cost_by_rating(cost, basecost, rating):
    if cost and rating:
        cost = 5**(rating/10.)/125. * cost + basecost
    else:
        cost = basecost
    return cost


def firewall_rating(time, skill, system, users):
    #time in hours per week
    return log(skill ** 3 / (system + 50) ** 3 * time / 8. / users) * 10 + skill - 50


def negative_square_avg(values):
    result = float('inf')
    if not all(values):
        result = 0
    elif values:
        result = (1./sum([(1./i)**2 for i in values]))**0.5
        result *= len(values)**0.5
    return result


def square_avg(values):
     return sum([i**2 for i in values])**0.5/len(values)**0.5


def square_add(values):
     return sum([i**2 for i in values])**0.5


def negative_square_add(values):
    result = float('inf')
    if values:
        result = (1./sum([(1./i)**2 for i in values]))**0.5
    return result


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
    return 2**(x/10.)


def price_by_rating(baseprice, rating):
    return (1+(2**(rating/10.)))/9.*baseprice


def contact_costs(loyalty, rating):
    return 2**((loyalty/30.)**2+(30/30.)**2)*50


def contacts_free_value(charisma):
    return charisma*charisma


def recoil_by_strength(recoil, strength, min_strength):
    return recoil/(strength/min_strength)


def get_sin_cost(rating, permit_mult):
    return 2000*5**(rating/10.-3)*permit_mult
