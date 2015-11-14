# !/usr/bin/env python
# !/usr/bin/env python
# coding: utf8

#from gluon import *
import collections
import data
import rules
import math


class Char(object):
    """
    Basic character class,
    handles database access
    """

    def __init__(self, db, char_id):
        """
        :param char_id: the character id from the database
        """
        self.db = db
        self.char_id = char_id
        self.name = None
        self.gender = None
        self.race = None
        self.attributes = {}
        self.skills = {}
        self.ware = []
        self.fixtures = []
        self.foci = []
        self.adept_powers = []
        self.items = []
        self.all_items = []
        self.damage = {}
        self.wounds = {}
        self.spells = []
        self.metamagic = []
        self.money = []
        self.xp = []
        self.load_char()

    def init_attributes(self):
        char_property_getter = CharPropertyGetter(self, 'base')
        for attribute in data.attributes_dict.keys():
            value = char_property_getter.get_attribute_value(attribute)
            self.attributes[attribute] = value
            self.db.char_attributes.bulk_insert([{'char': self.char_id, 'attribute': attribute, 'value': value}])

    def init_skills(self):
        for name, skill in data.skills_dict.items():
            self.db.char_skills.bulk_insert([{'char': self.char_id, 'skill': name, 'value': 0}])

    def load_char(self):
        """

        Load all character data from database
        """
        row = self.db.chars[self.char_id]
        self.name = row.name
        self.gender = row.gender
        self.race = row.race
        self.load_attributes()
        self.load_skills()
        self.load_ware()
        self.load_fixtures()
        self.load_damage()
        self.load_wounds()
        self.load_items()
        self.load_foci()
        self.load_spells()
        self.load_metamagic()
        self.load_adept_powers()
        self.load_xp()
        self.load_money()

    def load_xp(self):
        db_cx = self.db.char_xp
        for row in self.db(db_cx.char == self.char_id).select(db_cx.xp, db_cx.usage, db_cx.timestamp):
            self.xp.append([row.xp, row.usage, row.timestamp])

    def load_money(self):
        db_cm = self.db.char_money
        for row in self.db(db_cm.char == self.char_id).select(db_cm.money, db_cm.usage, db_cm.timestamp):
            self.money.append([row.money, row.usage, row.timestamp])
        for entry in self.xp:
            if entry[1] == 'money':
                self.money.append([entry[0]*(-1)/rules.money_to_xp if entry[0] > 1 else entry[0] *(-1) *rules.xp_to_money , 'xp', entry[2]])

    def load_spells(self):
        db_cs = self.db.char_spells
        for row in self.db(db_cs.char == self.char_id).select(db_cs.spell):
            self.spells.append(row.spell)

    def load_metamagic(self):
        db_cm = self.db.char_metamagic
        for row in self.db(db_cm.char == self.char_id).select(db_cm.metamagic):
            self.metamagic.append(row.metamagic)

    def load_attributes(self):
        """

        Load character attributes from database, if not present, use 30
        """
        db_ca = self.db.char_attributes
        if not self.db(db_ca.char == self.char_id).select().first():
            self.init_attributes()
        for row in self.db(db_ca.char == self.char_id).select(db_ca.attribute, db_ca.value):
            self.attributes[row.attribute] = row.value

    def load_skills(self):
        """

        Load char skills from database, if not present, use 0
        """
        db_cs = self.db.char_skills
        if not self.db(db_cs.char == self.char_id).select().first():
            self.init_skills()
        for row in self.db(db_cs.char == self.char_id).select(db_cs.skill, db_cs.value):
            self.skills[row.skill] = row.value

    def load_damage(self):
        db_cd = self.db.char_damage
        self.damage = {}
        for row in self.db(db_cd.char == self.char_id).select(db_cd.damagekind, db_cd.value):
            self.damage[row.damagekind] = row.value

    def load_wounds(self):
        db_cw = self.db.char_wounds
        self.wounds = collections.defaultdict(dict)
        for row in self.db(db_cw.char == self.char_id).select(db_cw.bodypart, db_cw.damagekind, db_cw.value):
            self.wounds[row.bodypart].update({row.damagekind: row.value})

    def load_ware(self):
        """

        Load character ware
        """
        db_cw = self.db.char_ware
        for row in self.db(db_cw.char == self.char_id).select(db_cw.ware, db_cw.id):
            self.ware.append(CharWare(self.db, row.ware, row.id, self))

    def load_fixtures(self):
        """

        Load character fixtures
        """
        db_cf = self.db.char_fixtures
        for row in self.db(db_cf.char == self.char_id).select(db_cf.fixture):
            self.fixtures.append(CharFixture(row.fixture, self))

    def load_adept_powers(self):
        db_cap = self.db.char_adept_powers
        for row in self.db(db_cap.char == self.char_id).select(db_cap.power):
            self.adept_powers.append(CharAdeptPower(self.db, row.power, self))

    def get_loadout(self):
        loadout = self.db(self.db.char_loadout.char == self.char_id).select(self.db.char_loadout.value).first()
        if loadout:
           self.loadout = loadout.value
        else:
            self.loadout = 0

    def load_items(self):
        db_ci = self.db.char_items
        for row in self.db(db_ci.char == self.char_id).select(db_ci.id, db_ci.item, db_ci.rating):
            self.all_items.append(Item(row.item, row.id, row.rating))
        else:
            self.get_loadout()
            for row in self.db((db_ci.char == self.char_id) & (db_ci.loadout.contains(self.loadout))).select(db_ci.id, db_ci.item, db_ci.rating):
                self.items.append(Item(row.item, row.id, row.rating))

    def load_foci(self):
        foci = [item.name for item in self.items if data.gameitems_dict[item.name].clas  == 'Focus']
        self.foci = [CharFocus(self.db, name, self) for name in foci]

    def write_attribute(self, attribute, value):
        db_ca = self.db.char_attributes
        self.db((db_ca.char == self.char_id) & (db_ca.attribute == attribute)).update(value=value)

    def write_skill(self, skill, value):
        db_cs = self.db.char_skills
        self.db((db_cs.char == self.char_id) & (db_cs.skill == skill)).update(value=value)

    def write_damage(self, kind, value):
        db_cd = self.db.char_damage
        if value:
            db_cd.update_or_insert((db_cd.char == self.char_id) & (db_cd.damagekind == kind),
                                   value=value,
                                   char = self.char_id,
                                   damagekind = kind)
        else:
            self.db((db_cd.char == self.char_id) & (db_cd.damagekind == kind)).delete()

    def write_wounds(self, number, bodypart, kind):
        db_cw = self.db.char_wounds
        if number:
            db_cw.update_or_insert((db_cw.char == self.char_id) & (db_cw.damagekind == kind) &
                                   (db_cw.bodypart == bodypart),
                                   value=number,
                                   char = self.char_id,
                                   damagekind = kind,
                                   bodypart = bodypart)
        else:
            self.db((db_cw.char == self.char_id) & (db_cw.damagekind == kind) & (db_cw.bodypart == bodypart)).delete()

    @staticmethod
    def write_ware(ware):
        ware.write()

    @staticmethod
    def delete_ware(ware):
        ware.delete()

    def delete_damage(self, damage, value):
        pass

    def ware_fix_power_effect(self, primary, secondary, value, func = None, modlevel = 'augmented'):
        for adept_power in self.adept_powers:
            for effect in adept_power.effects:
                if effect[0] == primary and effect[1] == secondary:
                    magic = CharPropertyGetter(self, 'stateful').get_attribute_value('Magic')
                    formula = effect[2].format(Value = adept_power.value, Magic = magic)
                    if not func:
                        value = eval('value {}'.format(formula))
                    else:
                        value = eval(func.format(formula))
        for ware in self.ware:
            for effect in ware.effects:
                if effect[0] == primary and effect[1] == secondary:
                    if not func:
                        value = eval('value {}'.format(effect[2]))
                    else:
                        value = eval(func.format(effect[2]))
        for fixture in self.fixtures:
            for effect in fixture.effects:
                if effect[0] == primary and effect[1] == secondary:
                    if not func:
                        value = eval('value {}'.format(effect[2]))
                    else:
                        value = eval(func.format(effect[2]))
        if modlevel in ('temporary', 'stateful'):
            for focus in self.foci:
                for effect in focus.effects:
                    if effect[0] == primary and effect[1] == secondary:
                        if not func:
                            value = eval('value {}'.format(effect[2].format(Rating=focus.rating)))
                        else:
                            value = eval(func.format(effect[2].format(Rating=focus.rating)))
        return value


class Item(object):
    def __init__(self, name, db_id, rating = None):
        self.name = name
        self.rating = rating

    def get_cost(self):
        ratingcost = 0
        if self.rating:
            cost = data.gameitems_dict[self.name].rating
            ratingcost = rules.price_by_rating(cost,self.rating)
        return data.gameitems_dict[self.name].cost + ratingcost

class Computer(object):
    def __init__(self, db, computer_id, char):
        self.db = db
        self.char = char
        self.computer_id = computer_id
        self.name = ''
        self.attributes = {}
        self.programmes = {}
        self.damage = []
        self.mode = None
        self.actions = data.matrix_actions_dict
        self.load_attributes()
        self.load_programmes()
        self.char_property_getter = CharPropertyGetter(self.char)

    def load_attributes(self):
        db_cc = self.db.char_computers
        row = self.db(db_cc.id == self.computer_id).select(db_cc.item,
                                                        db_cc.firewall,
                                                        db_cc.current_uplink,
                                                        db_cc.damage).first()
        self.attributes['Current Uplink'] = row.current_uplink
        self.attributes['Firewall'] = row.firewall
        self.damage = row.damage
        self.name = row.item.item
        self.attributes['System'] = data.computer_dict[self.name].System
        self.attributes['Processor'] = data.computer_dict[self.name].Processor
        self.attributes['Signal'] = data.computer_dict[self.name].Signal
        self.attributes['Uplink'] = data.computer_dict[self.name].Uplink

    def load_programmes(self):
        db_cg = self.db.char_items
        rows = self.db((db_cg.char == self.char.char_id) &
                      (db_cg.item in data.programmes_dict.keys())).select(db_cg.item,db_cg.rating)
        for row in rows:
            self.programmes[row.item] = row.rating

    def load_damage(self):
        db_cc = self.db.char_computers
        row = self.db(db_cc.id == self.computer_id).select(db_cc.damage).first()
        self.damage = row.damage

    def get_action_value(self, action):
        programme = self.actions[action].programme
        if programme:
            programme_value = self.programmes.get(programme,0)
            attribute = data.programmes_dict[programme].attribute
            attribute_value = self.attributes[attribute]
            skill = data.programmes_dict[programme].skill
            skill_value = self.char_property_getter.get_skilltest_value(skill)
            value = rules.matrix_action_rating(programme_value, attribute_value, skill_value)
        else:
            value = None
        return value


class CloseCombatWeapon(object):
    def __init__(self, name, char):
        self.char = char
        self.name = name
        self.char_property_getter = CharPropertyGetter(self.char)
        self.skill = ''
        self.skillmod = 0
        self.minstr = 0
        self.recoil = 0
        self.damage = 0
        self.penetration = 0
        self.get_attributes()

    def get_attributes(self):
        weapon_tuple = data.closecombatweapons_dict[self.name]._asdict()
        for key, value in weapon_tuple.items():
            setattr(self, key, value)
        for attribute in ('damage', 'penetration'):
            if isinstance(getattr(self, attribute), str):
                setattr(self, attribute,
                        round(eval(getattr(self, attribute).format(Strength=self.char_property_getter.get_attribute_value('Strength')))))

    def get_net_skill_value(self):
        minstr_mod = rules.weapon_minstr_mod(self.minstr, self.char_property_getter.get_attribute_value('Strength'))
        net_skill_value = self.char_property_getter.get_skill_value(self.skill) + self.skillmod - minstr_mod
        return net_skill_value

    def get_damage(self, cc_mod):
        damage = []
        skill = self.char_property_getter.get_skilltest_value(self.skill)
        minstr_mod = rules.weapon_minstr_mod(self.minstr, self.char_property_getter.get_attribute_value('Strength'))
        net_value = skill - minstr_mod - cc_mod + self.skillmod
        result = net_value
        if net_value > 0:
            damage.append((rules.weapondamage(self.damage, net_value), rules.damage_location()))
        return damage, {'minimum strength mod': minstr_mod, 'weapon skill mod': self.skillmod,
                        'skill': skill, 'other mods': cc_mod, 'result': result, 'difficulty': 0.}


class RangedWeapon(object):
    def __init__(self, name, char):
        self.char = char
        self.name = name
        self.char_property_getter = CharPropertyGetter(self.char)
        self.range = 0
        self.skill = ''
        self.skillmod = 0
        self.minstr = 0
        self.recoil = 0
        self.damage = 0
        self.penetration = 0

        self.get_attributes()

    def get_attributes(self):
        weapon_tuple = data.rangedweapons_dict[self.name]._asdict()
        for key, value in weapon_tuple.items():
            setattr(self, key, value)
        for attribute in ('damage', 'penetration', 'range'):
            if isinstance(getattr(self, attribute), str):
                setattr(self, attribute,
                        round(eval(getattr(self, attribute).format(Strength=self.char_property_getter.get_attribute_value('Strength')))))
        self.recoil = rules.recoil_by_strength(self.recoil, self.char_property_getter.get_attribute_value('Strength'), self.minstr)

    def get_shooting_difficulty(self, distance, magnification=1., burst = False):
        if burst == 'Wide Shot':
            wide_burst_bullets = self.shot
        elif burst == 'Wide Burst':
            wide_burst_bullets = self.burst
        elif burst == 'Wide Auto':
            wide_burst_bullets = self.auto
        else:
            wide_burst_bullets = 0
        return rules.shooting_difficulty(self.range, magnification, distance, 2, wide_burst_bullets)

    def get_net_skill_value(self, braced = False):
        if not braced:
            minstr_mod = rules.weapon_minstr_mod(self.minstr, self.char_property_getter.get_attribute_value('Strength'))
        else:
            min_str_mod = 0
        net_skill_value = self.char_property_getter.get_skilltest_value(self.skill) + self.skillmod - minstr_mod
        return net_skill_value

    def get_damage(self, shoot_mod, distance, magnification = 1., size = 2., braced = False, burst=False):
        damage = []
        range_mod = rules.shoot_rangemod(self.range, distance)
        sight_mod = rules.visible_perception_mod(size, distance, magnification)
        skill = self.char_property_getter.get_skilltest_value(self.skill)
        if not braced:
            minstr_mod = rules.weapon_minstr_mod(self.minstr, self.char_property_getter.get_attribute_value('Strength'))
        else:
            minstr_mod = 0
        if burst == 'Wide Shot':
            wide_burst_mod = self.shot
        elif burst == 'Wide Burst':
            wide_burst_mod = self.burst
        elif burst == 'Wide Auto':
            wide_burst_mod = self.auto
        else:
            wide_burst_mod = 0
        net_value = -rules.shoot_base_difficulty + skill - minstr_mod - range_mod - sight_mod - shoot_mod + self.skillmod - wide_burst_mod
        result = net_value
        if burst == 'Narrow Shot':
            bullets = self.shot
        elif burst == 'Narrow Burst':
            bullets = self.burst
        elif burst == 'Narrow Auto':
            bullets = self.auto
        else:
            bullets = 1
        while net_value >= 0 and bullets:
            damage.append(((rules.weapondamage(self.damage, net_value)), rules.damage_location()))
            net_value -= self.recoil
            bullets -= 1
        return damage, {'difficulty': rules.shoot_base_difficulty, 'weapon range mod': range_mod,
                        'sight range mod': sight_mod, 'minimum strength mod': minstr_mod,
                        'skill': skill, 'other mods': shoot_mod, 'result': result, 'wide burst mod': wide_burst_mod}


class Armor(object):
    def __init__(self, name):
        self.name = name

    def get_locations(self):
        return data.armor_dict[self.name].locations

    def get_max_agi(self):
        return data.armor_dict[self.name].maxagi

    def get_coordination_mult(self):
        return data.armor_dict[self.name].coordmult

    def get_protection(self, bodypart, typ = 'ballistic'):
        map_dict = {'ballistic': 0,
                    'impact': 1}
        locations = data.armor_dict[self.name].locations
        index = locations.index(bodypart) if bodypart in locations else None
        protection = 0
        if index is not None:
            protection = data.armor_dict[self.name].protections[index][map_dict[typ]]
        return protection

#class CharMatrix(Char):
#    def __init__(self, db, char, computer=None):
#        Char.__init__(self, db, char)
#        self.computer = Computer(computer)
#
#
#class CharAstral(Char):
#    def __init__(self, db, char):
#        """"
#
#        :param char: the character for witch to get the attribute
#        """
#        Char.__init__(self, db, char)
#
#
class Loadout(Char):
    def __init__(self, db, char):
        """"

        :param char: the character for witch to get the attribute
        """
        Char.__init__(self, db, char)


class SkillTree(object):
    def __init__(self):
        self.tree_dict = {}

    def load_data(self):
        pass

    def get_skill(self, name):
        pass


class Skill(object):
    def __init__(self, name, parent, attribmods):
        self.name = name
        self.parent = parent
        self.attribmods = attribmods


class Fixture(object):
    def __init__(self, name):
        self.name = name
        self.location = None
        self.relative_capacity = None
        self.absolute_capacity = None
        self.weight = None
        self.description = None
        self.cost = None
        self.effects = None
        self.load_basic_data()

    def load_basic_data(self):
        fixture = data.fixtures_dict[self.name]
        self.location = fixture.location
        self.relative_capacity = fixture.relative_capacity
        self.absolute_capacity = fixture.absolute_capacity
        self.weight = fixture.weight
        self.cost = fixture.cost
        self.effects = fixture.effects
        self.description = fixture.description

    def get_cost(self):
        return self.cost

class CharFixture(Fixture):
    def __init__(self, fixture_name, char):
        Fixture.__init__(self, fixture_name)
        self.char = char

    def get_capacity_dict(self):
        capacity = {}
        char_body = CharBody(self.char)
        for location in self.location:
            capacity[location] = (self.absolute_capacity +
                                  self.relative_capacity *
                                  char_body.bodyparts[location].get_attribute_absolute('Weight', 'augmented'))
        return capacity



class Ware(object):
    def __init__(self, db, name):
        self.db = db
        self.name = name
        self.kind = None
        self.essence = None
        self.part_weight = None
        self.additional_weight = None
        self.description = None
        self.basecost = None
        self.cost = None
        self.parts = None
        self.effects = None
        self.location = None
        self.capacity = None
        self.load_basic_data()

    def load_basic_data(self):
        ware_nt = data.ware_dict[self.name]
        self.kind = ware_nt.kind
        self.essence = ware_nt.essence
        self.part_weight = ware_nt.part_weight
        self.additional_weight = ware_nt.additional_weight
        self.description = ware_nt.description
        self.basecost = ware_nt.basecost
        self.effectcost = ware_nt.effectcost
        self.partcost = ware_nt.partcost
        self.parts = ware_nt.parts
        self.effects = ware_nt.effects
        self.location = ware_nt.location
        self.capacity = ware_nt.capacity

class CharWare(Ware):
    def __init__(self, db, ware_name, db_id, char):
        Ware.__init__(self, db, ware_name)
        self.db_id = db_id
        self.char = char
        self.stats = {}
        self.load_extra_data()
        #self.weight = self.calc_absolute_weight()

    def init_stats(self):
        char_property_getter = CharPropertyGetter(self.char, 'base')
        for name, attribute in data.attributes_dict.items():
            if attribute.kind == 'physical' or attribute.name == 'Weight':
                value = char_property_getter.get_attribute_value(attribute.name)
                self.db.char_ware_stats.bulk_insert([{'ware': self.db_id, 'stat': attribute.name, 'value': value}])
        essence_value = data.essence_by_ware[self.kind]
        self.db.char_ware_stats.bulk_insert([{'ware': self.db_id, 'stat': 'Essence', 'value': essence_value}])

    def load_extra_data(self):
        db_cws = self.db.char_ware_stats
        if not self.db(db_cws.ware == self.db_id).select().first():
            self.init_stats()
        for row in self.db(db_cws.ware == self.db_id).select(db_cws.stat, db_cws.value):
            self.stats[row.stat] = row.value

    def write(self):
        db_cw = self.db.char_ware
        if self.db_id is not None:
            self.db_id = db_cw.insert(char=self.char.char_id, ware=self.name)
        else:
            self.db(db_cw.id == self.db_id).update(char=self.char.char_id, ware=self.name)

    def delete(self):
        db_cw = self.db.char_ware
        self.db(db_cw.id == self.db_id).delete()

#    def calc_absolute_weight(self):
#        if '%' in str(self.additional_weight):
#            weight = getter_functions.CharPhysicalPropertyGetter(self.char, 'unaugmented').get_attribute_mod('weight')
#            weight *= float(self.additional_weight[:-1])
#        else:
#            weight = self.additional_weight
#        return weight

    def get_cost(self):
        essencemult = 1 - self.stats['Essence']/100.
        cost = rules.warecost(self.basecost, kind = self.kind)
        cost += rules.warecost(self.effectcost, essencemult=essencemult )
        if self.parts:
            char_property_getter = CharPropertyGetter(self.char, modlevel='base')
            size = char_property_getter.get_attribute_value('Size')
            weight_base = data.attributes_dict['Weight'].base
            size_base = data.attributes_dict['Size'].base
            weight = rules.calc_base_weight(weight_base, size, size_base)
            for part in self.parts:
                bodypart = char_property_getter.char_body.bodyparts[part].bodypart
                for attribute in ['Agility', 'Constitution', 'Coordination', 'Strength']:
                    base = 30.
                    if attribute == 'Agility':
                        agility_base = data.attributes_dict['Agility'].base
                        base = rules.calc_agility_base(agility_base, weight, weight_base)
                    elif attribute == 'Strength':
                        strength_base = data.attributes_dict['Strength'].base
                        size_racemod = data.races_dict[char_property_getter.char.race].Weight**(1/3.)
                        base = rules.calc_base_strength(strength_base, size*size_racemod, size_base, weight, weight_base)
                    value = self.stats[attribute]
                    frac = bodypart.get_fraction(attribute)
                    cost += frac * rules.warecost(self.partcost,
                                                  effectmult=value/base,
                                                  essencemult=essencemult,
                                                  kind=self.kind)
        return cost

    def get_essence_cost(self):
        cost = self.essence
        if self.parts:
            char_body = CharBody(self.char)
            for part in self.parts:
                cost += char_body.bodyparts[part].get_attribute_absolute('Essence', modlevel = 'basic')
        cost *= (1-self.stats['Essence']/100.)
        return cost

    def get_non_located_essence_cost(self):
        cost = self.essence
        cost *= (1-self.stats['Essence']/100.)
        return cost


class AdeptPower(object):
    def __init__(self, db, name):
        self.db = db
        self.name = name
        self.description = None
        self.cost = None
        self.effects = None
        self.formdescription = None
        self.load_basic_data()

    def load_basic_data(self):
        adept_powers_nt = data.adept_powers_dict[self.name]
        self.description = adept_powers_nt.description
        self.cost = adept_powers_nt.cost
        self.effects = adept_powers_nt.effects
        self.formdescription = adept_powers_nt.formdescription

class CharAdeptPower(AdeptPower):
    def __init__(self, db, adept_power_name, char):
        AdeptPower.__init__(self, db, adept_power_name)
        self.char = char
        self.value = None
        self.load_extra_data()

    def load_extra_data(self):
        db_cap = self.db.char_adept_powers
        for row in self.db((db_cap.char == self.char.char_id) & (db_cap.power == self.name)).select(db_cap.value):
            self.value = row.value

    def write(self):
        db_cap = self.db.char_adept_powers
        if self.db_id is not None:
            self.db_id = db_cap.insert(char=self.char.char_id, power=self.name, value=self.value)
        else:
            self.db((db_cap.char == self.char.char_id) & (db_cap.power == self.name)).update(char=self.char.char_id,
                                                                                            power=self.name,
                                                                                            value=self.value)
    def delete(self):
        db_cap = self.db.char_adept_powers
        self.db((db_cap.char == self.char.char_id) & (db_cap.power == self.name)).delete()

    def get_description(self):
        magic = CharPropertyGetter(self.char, 'augmented').get_attribute_value('Magic')
        formdesc = '{}: '.format(self.value)
        for entry in self.formdescription:
            formdesc += entry[0]
            formdesc += str(eval(entry[1].format(Magic = magic, Value = self.value)))
            formdesc += '  '
        return formdesc

#    def calc_absolute_weight(self):
#        if '%' in str(self.additional_weight):
#            weight = getter_functions.CharPhysicalPropertyGetter(self.char, 'unaugmented').get_attribute_mod('weight')
#            weight *= float(self.additional_weight[:-1])
#        else:
#            weight = self.additional_weight
#        return weight


class Focus(object):
    def __init__(self, db, name):
        self.db = db
        self.name = name
        self.effects = None
        self.load_basic_data()

    def load_basic_data(self):
        foci_nt = data.foci_dict[self.name]
        self.effects = foci_nt.effects


class CharFocus(Focus):
    def __init__(self, db, focus_name, char):
        Focus.__init__(self, db, focus_name)
        self.char = char
        self.rating = None
        self.load_extra_data()

    def load_extra_data(self):
        db_ci = self.db.char_items
        for row in self.db((db_ci.char == self.char.char_id) & (db_ci.item == self.name)).select(db_ci.rating):
            self.rating = row.rating


class Body(object):
    def __init__(self):
        self.bodyparts = {}
        for bodypart in data.bodyparts_dict:
            self.bodyparts[bodypart] = Bodypart(self, bodypart)
        for bodypart  in self.bodyparts.values():
            bodypart.set_children()


class CharBody():
    def __init__(self, char):
        self.char = char
        self.bodyparts = {}
        self.body = Body()
        self.init_body()
        self.place_ware()
        self.place_fixtures()

    def init_body(self):
        self.place_bodypart(self.body.bodyparts['Body'], None)
        for part in data.bodyparts_dict:
            part = self.body.bodyparts[part]
            self.bodyparts[part.name] = CharBodypart(self.char,self, part, None, None)

    def place_ware(self):
        for ware in self.char.ware:
            if ware.parts:
                for part in ware.parts:
                    self.place_bodypart(part, ware)

    def place_fixtures(self):
        for fixture in self.char.fixtures:
            for location in fixture.location:
                self.bodyparts[location].fixtures.append(fixture)

    def place_bodypart(self, part, ware):
        if isinstance(part, basestring):
            part = self.body.bodyparts[part]
        self.bodyparts[part.name] = CharBodypart(self.char, self, part, ware, None)
        for child in part.children:
            self.place_bodypart(child, ware)

    def get_bodypart_composition(self, name):
        pass

    def get_location_ware(self, name):
        pass

    def get_essence(self):
        pass

BodyFractions = collections.namedtuple('BodyFraction',
                                       ['Weight', 'Size', 'Essence', 'Agility',
                                        'Coordination', 'Strength', 'Constitution'])


class Bodypart(object):
    def __init__(self, body, name):
        self.body = body
        self.name = name
        self.template = None
        self.parent = None
        self.body_fractions = None
        self.children = []
        self.level = 0
        self.load_data()

    def load_data(self):
        bodypart_nt = data.bodyparts_dict[self.name]
        self.level = bodypart_nt.level
        self.template = bodypart_nt.template
        self.parent = self.body.bodyparts.get(bodypart_nt.parent, None)
        self.relative_body_fractions = BodyFractions(Weight=bodypart_nt.weightfrac,
                                                     Size=bodypart_nt.sizefrac,
                                                     Essence=bodypart_nt.essencefrac,
                                                     Agility=bodypart_nt.agilityfrac,
                                                     Coordination=bodypart_nt.coordinationfrac,
                                                     Strength=bodypart_nt.strengthfrac,
                                                     Constitution=bodypart_nt.constitutionfrac)
        if self.parent is None:
            self.body_fractions = self.relative_body_fractions
        else:
            self.body_fractions = BodyFractions(*[i*j for i,j in zip(self.relative_body_fractions, self.parent.body_fractions)])

    def set_children(self):
        self.children = [self.body.bodyparts[i.name] for i in data.bodyparts_dict.values() if i.parent == self.name]

    def get_fraction(self, attribute):
        return getattr(self.body_fractions, attribute)

    def get_kind(self):
        return 'unaugmented', 0., 0.


class CharBodypart():
    def __init__(self, char, char_body, bodypart, ware, fixtures):
        self.char_body = char_body
        self.char = char
        self.bodypart = bodypart
        self.ware = ware
        if fixtures:
            self.fixtures = fixtures
        else:
            self.fixtures = []
        self.wounds = char.wounds.get(bodypart.name, {})
        self.attributes = {}

    def get_capacity(self):
        capacity = 0
        if self.ware and self.ware.kind == 'cyberware':
            weight = self.get_attribute_absolute('Weight', 'augmented')
            capacity = weight * self.ware.capacity if self.ware.capacity else 0
        return capacity

    def get_used_capacity(self):
        used = 0
        if self.fixtures:
            weight = self.get_attribute_absolute('Weight', 'augmented')
            for fixture in self.fixtures:
                used += fixture.absolute_capacity + weight*fixture.relative_capacity
        for child in self.bodypart.children:
            used += self.char_body.bodyparts[child.name].get_used_capacity()
        return used

    def get_kind(self):
        if self.ware:
            if self.ware.kind == 'cyberware':
                return self.ware.kind, 1., 0.
            elif self.ware.kind == 'bioware':
                return self.ware.kind, 0., 1.
        elif self.bodypart.children:
            child_char_bodyparts = [self.char_body.bodyparts[child.name] for child in self.bodypart.children]
            weights = [part.get_attribute_absolute('Weight', modlevel='augmented') for part in child_char_bodyparts]
            kinds = [part.get_kind() for part in child_char_bodyparts]
            cyberweight = sum([weights[i]*kind[1] for i,kind in enumerate(kinds)])
            bioweight = sum([weights[i]*kind[2] for i,kind in enumerate(kinds)])
            cyberfrac = cyberweight/sum(weights)
            biofrac = bioweight/sum(weights)
            if  cyberfrac > 0.5:
                kind = 'cyberware'
            elif biofrac > 0.5:
                kind = 'bioware'
            else:
                kind = 'unaugmented'
            return kind, cyberfrac, biofrac
        else:
            return self.bodypart.get_kind()

    def get_attribute_absolute(self, attribute, modlevel='stateful'):
        value = self.attributes.get((attribute, modlevel))
        if value:
            return value
        fraction = self.bodypart.get_fraction(attribute)
        if not fraction:
            return 0
        if self.bodypart.children:
            child_char_bodyparts = [self.char_body.bodyparts[child.name] for child in self.bodypart.children]
            value = sum([part.get_attribute_absolute(attribute, modlevel) for part in child_char_bodyparts])
            # calculate armor modifications
            if modlevel in ('stateful', 'temporary'):
                char_property_getter = CharPropertyGetter(self.char, modlevel = modlevel)
                if attribute == 'Agility':
                    max_agis = []
                    for armor in char_property_getter.get_armor(self.bodypart.name):
                        max_agis.append(armor.get_max_agi())
                        value /= fraction
                        value = rules.get_armor_agility(value, max_agis)
                        value *= fraction
                if attribute == 'Coordination':
                    coord_mults = []
                    for armor in char_property_getter.get_armor(self.bodypart.name):
                        coord_mults.append(armor.get_coordination_mult())
                    value = rules.get_armor_coordination(value, coord_mults)
            if modlevel == 'stateful':
                if self.wounds and attribute not in ('Size', 'Weight', 'Constitution', 'Essence'):
                    weight = self.get_attribute_relative('Weight')
                    constitution = self.get_attribute_relative('Constitution')
                    value = rules.woundeffect(value, sum(self.wounds.values()), weight, constitution)
            return value
        else:
            if attribute == 'Essence':
                value = 100.
            else:
                value = self.char.attributes[attribute]
            if modlevel in ('augmented', 'temporary', 'stateful'):
                if self.ware:
                    value = self.ware.stats[attribute]
                if attribute != 'Magic':
                    value = self.char.ware_fix_power_effect('attributes', attribute, value, modlevel=modlevel)
            if modlevel == 'stateful':
                if self.wounds and attribute not in ('Size', 'Weight', 'Constitution', 'Essence'):
                    weight = self.get_attribute_relative('Weight')
                    constitution = self.get_attribute_relative('Constitution')
                    value = rules.woundeffect(value, sum(self.wounds.values()), weight, constitution)
            value *= fraction
            self.attributes[(attribute, modlevel)] = value
            return value

    def get_life(self):
        if self.bodypart.children:
            child_char_bodyparts = [self.char_body.bodyparts[child.name] for child in self.bodypart.children]
            return sum([part.get_life() for part in child_char_bodyparts])
        else:
            kind, cyberfraction, biofraction = self.get_kind()
            weight = self.get_attribute_relative('Weight')
            constitution = self.get_attribute_relative('Constitution')
            fraction = self.bodypart.get_fraction('Weight')
            life = fraction * rules.life(weight, constitution) * (1.-cyberfraction)
            return life

    def get_woundlimit(self, modlevel = 'stateful'):
        constitution = self.get_attribute_relative('Constitution', modlevel)
        weight = self.get_attribute_relative('Weight', 'temporary')
        woundlimit = rules.woundlimit(weight, constitution)
        return woundlimit

    def get_wounds_incapacitated_thresh(self, modlevel = 'stateful'):
        constitution = self.get_attribute_relative('Constitution', modlevel)
        weight = self.get_attribute_relative('Weight', 'temporary')
        thresh = rules.wounds_for_incapacitated_thresh(weight, constitution)
        return thresh

    def get_wounds_destroyed_thresh(self, modlevel = 'stateful'):
        constitution = self.get_attribute_relative('Constitution', modlevel)
        weight = self.get_attribute_relative('Weight', 'temporary')
        thresh = rules.wounds_for_destroyed_thresh(weight, constitution)
        return thresh

    def get_attribute_relative(self, attribute, modlevel = 'stateful'):
        absolute_value = self.get_attribute_absolute(attribute, modlevel)
        fraction = self.bodypart.get_fraction(attribute)
        return absolute_value/fraction if fraction else 0


modlevels = ['base', 'unaugmented', 'augmented', 'temporary', 'stateful']
interfaces = ['basic', 'ar', 'cold-sim', 'hot-sim']


class CharPropertyGetter():
    def __init__(self, char, modlevel='stateful'):
        """"
        :param modlevel: the modlevel: ['base', 'unaugmented', 'augmented', 'temporary', 'stateful']
        """
        self.char = char
        self.modlevel = modlevel
        self.char_body = CharBody(self.char)
        self.attributes = {}
        self.skills = {}
        self.stats = {}
        self.maxlife = {}

    def get_bodypart_table(self):
        attributes = ['Essence', 'Agility', 'Constitution', 'Coordination', 'Strength', 'Weight']
        table = [['Name'] + attributes + ['Ware', 'Woundlimit', 'Wounds']]
        for bodypartname in data.bodyparts_dict:
            templist = []
            bodypart = self.char_body.bodyparts[bodypartname]
            level = bodypart.bodypart.level
            templist.append('<b style="margin-left:{}em;">{}</b>'.format(level*1, bodypartname))
            for attribute in attributes:
                augmented = int(round(bodypart.get_attribute_relative(attribute, modlevel='augmented')))
                stateful = int(round(bodypart.get_attribute_relative(attribute, modlevel='stateful')))
                frac = round(bodypart.bodypart.get_fraction(attribute),2)
                templist.append('{}/{}/{}'.format(augmented, stateful, frac))
            ware = bodypart.ware.name if bodypart.ware else ''
            kind = bodypart.get_kind()[0]
            templist.append('{}/{}'.format(kind, ware))
            woundlimit = int(round(bodypart.get_woundlimit()))
            templist.append(woundlimit)
            wounds = int(sum([i for i in  bodypart.wounds.values()]))
            templist.append(wounds)
            table.append(templist)
        return table

    def get_skill_xp_cost(self, skill):
        parent = data.skills_dict[skill].parent
        base_value = 0
        if parent:
            base_value = self.get_skill_value(parent)
        value = self.get_skill_value(skill)
        base_value_xp = rules.get_skill_xp_cost(base_value)
        value_xp = rules.get_skill_xp_cost(value)
        result = (value_xp - base_value_xp) * data.skills_dict[skill].expweight
        if result < 0:
            result = 0
        return result

    def get_attribute_xp_cost(self, attribute):
        factor = data.attributes_dict[attribute].factor
        signmod = data.attributes_dict[attribute].signmod
        base = CharPropertyGetter(self.char, 'base').get_attribute_value(attribute)
        value = CharPropertyGetter(self.char, 'unaugmented').get_attribute_value(attribute)
        result = rules.exp_cost_attribute(attribute, value, base, factor, signmod)
        return result

    def get_spell_xp_cost(self):
        return sum([rules.get_spell_xp_cost() for i in self.char.spells])

    def get_metamagic_xp_cost(self):
        return sum([rules.get_metamagic_xp_cost() for i in self.char.metamagic])

    def get_attribute_value(self, attribute):
        """
        Calculate a specific attribute of the given character

        :param attribute: the attribute to get
        :returns: the value of the requested attribute
        :rtype: float
        """
        value = self.attributes.get(attribute)
        # use value if already calculated
        if value:
            return value
        # base modlevel returns the basic average attribute value of a given gender/race combination
        if self.modlevel == 'base':
            value = data.attributes_dict[attribute].base
            if attribute == 'Weight':
                size = CharPropertyGetter(self.char, 'unaugmented').get_attribute_value('Size')
                size_base = data.attributes_dict['Size'].base
                value = rules.calc_base_weight(value, size, size_base)
            elif attribute in ['Strength', 'Agility']:
                size = CharPropertyGetter(self.char, 'unaugmented').get_attribute_value('Size')
                size_base = data.attributes_dict['Size'].base
                weight = CharPropertyGetter(self.char, 'unaugmented').get_attribute_value('Weight')
                weight_base = data.attributes_dict['Weight'].base
                if attribute == 'Strength':
                    value = rules.calc_base_strength(value, size, size_base, weight, weight_base)
                elif attribute == 'Agility':
                    value = rules.calc_agility_base(value, weight, weight_base)
            if self.char.gender and self.char.race:
                value *= getattr(data.gendermods_dict[self.char.gender], attribute)
                value *= getattr(data.races_dict[self.char.race], attribute)
        # unaugmented modlevel includes basic attribute values without any modifiers
        elif self.modlevel == 'unaugmented':
            if attribute == 'Essence':
                value = 100.
            else:
                value = self.char.attributes[attribute]
        # augmented modlevel includes permanent modifications including cyberware, bioware, adept powers and more
        # temporary modlevel includes drugs, spells, encumbrance
        # stateful modlevel includes damage
        elif self.modlevel in ('augmented', 'temporary', 'stateful'):
            # calculate body part contribution to attribute
            if attribute == 'Weight':
                #implicitly includes wounds
                value = self.char_body.bodyparts['Body'].get_attribute_absolute(attribute, self.modlevel)
            elif attribute == 'Essence' or data.attributes_dict[attribute].kind == 'physical':
                #implicitly includes wounds
                value = self.char_body.bodyparts['Body'].get_attribute_absolute(attribute, self.modlevel)
            else:
                value = self.char.attributes[attribute]
            #subtract Essence from non located ware
            if attribute == 'Essence':
                for ware in self.char.ware:
                    essence_cost = ware.get_non_located_essence_cost()
                    essence_cost = self.char.ware_fix_power_effect('Essence Cost', ware.location, essence_cost, modlevel=self.modlevel)
                    value -= essence_cost
            elif attribute == 'Charisma':
                    essence = self.get_attribute_value('Essence')
                    value *= rules.essence_charisma_mult(essence)
            elif attribute == 'Magic':
                    essence = self.get_attribute_value('Essence')
                    value *= rules.essence_magic_mult(essence)
            # add ware effects to attribute
            if attribute not in ('Constitution', 'Strength', 'Agility', 'Coordindation', 'Weight', 'Size'):
                value = self.char.ware_fix_power_effect('attributes', attribute, value, modlevel=self.modlevel)
            if self.modlevel in ('stateful', 'temporary'):
                pass
            if self.modlevel == 'stateful' and attribute not in ('Size', 'Weight', 'Constitution', 'Essence', 'Magic'):
                value *= self.get_damagemod('relative')
            # store calculated value
            self.attributes[attribute] = value
        return value

    def get_attribute_mod(self, attribute):
        """

        :param attribute: the attribute to get
        """
        value = self.get_attribute_value(attribute)
        if attribute == 'Essence':
            base = 100.
        else:
            base = data.attributes_dict[attribute].base
        return rules.attrib_mod(value, base)

    def get_attribute_test_value(self, attribute):

        value = self.get_attribute_mod(attribute) + rules.attrib_mod_norm
        return value

    def get_skill_value(self, skill, base = False):
        """

        :param skill: the skill to get
        """
        if not base:
            value = self.skills.get(skill)
            if value:
                return value
        if self.modlevel == 'base':
            value = self.char.skills[skill]
        if self.modlevel in ('unaugmented', 'augmented','temporary','stateful'):
            value = self.char.skills.get(skill,0)
            parent = data.skills_dict[skill].parent
            if parent:
                parent_value = self.get_skill_value(parent, base=True)
                if value < parent_value:
                    value = parent_value
        if self.modlevel in ('augmented','temporary','stateful'):
            value = self.char.ware_fix_power_effect('skills', skill, value, modlevel=self.modlevel)
        if self.modlevel in ('temporary','stateful'):
            pass
        if not base:
            if self.modlevel == 'stateful':
                value += self.get_damagemod('absolute')
            self.skills[skill] = value
        return value

    def get_skilltest_value(self, skill):
        """

        :param skill: the skill to get
        """
        value = self.get_skill_value(skill)
        mod = 0
        skill_attribmods = data.skills_attribmods_dict[skill]
        for attribute in data.attributes_dict.keys():
            weight = getattr(skill_attribmods, attribute, None)
            if weight:
                mod += weight * self.get_attribute_mod(attribute)
        value += mod
        return value


    def get_armor(self, bodypart = None):
        armor = [item.name for item in self.char.items if data.gameitems_dict[item.name].clas == 'Armor']
        armor = [Armor(name) for name in armor]
        if bodypart:
            armor = [i for i in armor if bodypart in i.get_locations()]
        return armor


    def get_protection(self, bodypart, typ):
        protection = []
        for armor in self.get_armor():
            protection.append(armor.get_protection(bodypart, typ))
        protection.append(self.char.ware_fix_power_effect(typ + ' armor', bodypart, 0, func = '(value**2 + {}**2)**0.5', modlevel=self.modlevel))
        protection = rules.get_stacked_armor_value(protection)
        return protection

    def get_ranged_weapons(self):
        weapons = [item.name for item in self.char.items if data.gameitems_dict[item.name].clas  == 'Ranged Weapon']
        weapons = [RangedWeapon(name, self.char) for name in weapons]
        return weapons

    def get_close_combat_weapons(self):
        weapons = [item.name for item in self.char.items if data.gameitems_dict[item.name].clas  == 'Close Combat Weapon']
        weapons = [CloseCombatWeapon(name, self.char) for name in weapons]
        return weapons

    def get_maxlife(self, bodypart = 'Body'):
        value = self.maxlife.get(bodypart)
        if value:
            return value
        value = self.char_body.bodyparts['Body'].get_life()
        if self.modlevel in ('augmented', 'temporary', 'stateful'):
            value = self.char.ware_fix_power_effect('stats', 'life', value, modlevel=self.modlevel)
        self.maxlife[bodypart] = value
        return value

    def get_damagemod(self, kind):
        """
        kind = ['absolute', 'relative']

        """
        totaldamage = sum([i for i in self.char.damage.values()])
        if not totaldamage:
            totaldamage = 0
        statname = 'Pain Resistance'
        pain_resistance = 0
        pain_resistance = self.char.ware_fix_power_effect('stats', statname, pain_resistance, func = 'value + (1-value) * {}', modlevel=self.modlevel)
        max_life = self.get_maxlife()
        life = max_life - max(0, totaldamage - pain_resistance * max_life)
        if kind == 'relative':
            damagemod = rules.lifemod_relative(life, max_life)
        elif kind == 'absolute':
            damagemod = rules.lifemod_absolute(life, max_life)
        else:
            damagemod = 0
        return damagemod


    def get_reaction(self):
        """


        """
        statname = 'Reaction'
        value = self.stats.get(statname)
        if value:
            return value
        if self.modlevel == 'base':
            value = 0
        if self.modlevel in ('unaugmented', 'augmented','temporary','stateful'):
            value = rules.physical_reaction(self.get_attribute_mod('Agility'),
                                              self.get_attribute_mod('Intuition'))
        if self.modlevel in ('augmented','temporary','stateful'):
            value = self.char.ware_fix_power_effect('stats', statname, value, modlevel=self.modlevel)
        if self.modlevel in ('temporary','stateful'):
            pass
        self.stats[statname] = value
        return value

    def get_actionmult(self):
        """

        """
        statname = 'Action Multiplier'
        value = self.stats.get(statname)
        if value:
            return value
        if self.modlevel == 'base':
            value = 0
        if self.modlevel in ('unaugmented', 'augmented','temporary','stateful'):
            value = rules.physical_actionmult(self.get_attribute_mod('Agility'),
                                              self.get_attribute_mod('Coordination'),
                                              self.get_attribute_mod('Intuition'))
        if self.modlevel in ('augmented','temporary','stateful'):
            value = self.char.ware_fix_power_effect('stats', statname, value, modlevel=self.modlevel)
        if self.modlevel in ('temporary','stateful'):
            pass
        self.stats[statname] = value
        return value

    def get_actioncost(self, kind):
        actionmult = self.get_actionmult()
        cost = rules.action_cost(kind, actionmult)
        return cost

    def get_psycho_thresh(self):
        essence = self.get_attribute_value('Essence')
        thresh = rules.essence_psycho_thresh(essence)
        return thresh

    def get_total_exp(self):
        """

        """
        xp = {}
        xp['Attributes'] = 0
        for attribute in data.attributes_dict:
            xp['Attributes']  += self.get_attribute_xp_cost(attribute)
        xp['Skills'] = 0
        for skill in data.skills_dict:
            xp['Skills'] += self.get_skill_xp_cost(skill)
        xp['Spells'] = self.get_spell_xp_cost()
        xp['Metamagic'] = self.get_metamagic_xp_cost()
        return xp

    def get_total_cost(self):
        cost = {}
        warecost = 0
        for ware in self.char.ware:
            warecost += ware.get_cost()
        cost['Ware'] = warecost
        fixturecost = 0
        for fixture in self.char.fixtures:
            fixturecost += fixture.get_cost()
        cost['Fixtures'] = fixturecost
        itemcost = 0
        for item in self.char.all_items:
            itemcost += item.get_cost()
        cost['Items'] = itemcost
        return cost

    def get_spomod_max(self):
        logic = self.get_attribute_value('Logic')
        spomod_max = rules.spomod_max(logic)
        return spomod_max

    def get_drain_resist(self):
        willpower_mod = self.get_attribute_mod('Willpower')
        magic_mod = self.get_attribute_mod('Magic')
        drain_resist = rules.drain_resist(willpower_mod, magic_mod)
        return drain_resist

    def get_money(self):
        return sum([i[0] for i in self.char.money]) + rules.starting_money

    def get_xp(self):
        return sum([i[0] for i in self.char.xp]) + rules.starting_xp

    def get_power_cost(self):
        cost = 0
        for power in self.char.adept_powers:
            cost += power.cost if power.cost != 'X' else power.value
        return cost

class LoadoutPropertyGetter(Loadout):
    def __init__(self,db, char):
        """"
        :param char: the character for witch to get the attribute
        """
        Loadout.__init__(self, db, char)


class CharPhysicalPropertyGetter(CharPropertyGetter):
    def __init__(self, char, modlevel='stateful', bodypart='all'):
        """"
        :param char: the character for witch to get the attribute
        :param modlevel: the modlevel: ['unaugmented', 'augmented', 'temporary', 'stateful']
        :param bodypart: the bodypart(s) that are used calculating the attributes
        """
        CharPropertyGetter.__init__(self, char, modlevel)
        self.bodypart = bodypart

    def get_jump_distance(self, movement):
        weight = self.get_attribute_value('Weight')
        size = self.get_attribute_value('Size')
        strength = self.get_attribute_value('Strength')
        if movement:
            distance = rules.jumplimit(weight, strength, size)[1]
        else:
            distance = rules.jumplimit(weight, strength, size)[0]
        return distance

    def get_jump_height(self, movement):
        weight = self.get_attribute_value('Weight')
        size = self.get_attribute_value('Size')
        strength = self.get_attribute_value('Strength')
        if movement:
            distance = rules.jumplimit(weight, strength, size)[3]
        else:
            distance = rules.jumplimit(weight, strength, size)[2]
        return distance

    def get_speed(self):
        weight = self.get_attribute_value('Weight')
        size = self.get_attribute_value('Size')
        strength = self.get_attribute_value('Strength')
        agility = self.get_attribute_value('Agility')
        return rules.speed(agility, weight, strength, size)

    def get_reaction(self):
        """


        """
        statname = 'Physical Reaction'
        value = self.stats.get(statname)
        if value:
            return value
        if self.modlevel == 'base':
            value = 0
        if self.modlevel in ('unaugmented', 'augmented','temporary','stateful'):
            value = rules.physical_reaction(self.get_attribute_mod('Agility'),
                                              self.get_attribute_mod('Intuition'))
        if self.modlevel in ('augmented','temporary','stateful'):
            value = self.char.ware_fix_power_effect('stats', statname, value, modlevel=self.modlevel)
        if self.modlevel in ('temporary','stateful'):
            pass
        self.stats[statname] = value
        return value

    def get_actionmult(self):
        """

        """
        statname = 'Physical Action Multiplyer'
        value = self.stats.get(statname)
        if value:
            return value
        if self.modlevel == 'base':
            value = 0
        if self.modlevel in ('unaugmented', 'augmented','temporary','stateful'):
            value = rules.physical_actionmult(self.get_attribute_mod('Agility'),
                                              self.get_attribute_mod('Coordination'),
                                              self.get_attribute_mod('Intuition'))
        if self.modlevel in ('augmented','temporary','stateful'):
            value = self.char.ware_fix_power_effect('stats', statname, value, modlevel=self.modlevel)
        if self.modlevel in ('temporary','stateful'):
            pass
        self.stats[statname] = value
        return value

class CharMatrixPropertyGetter(CharPropertyGetter):
    def __init__(self, char, modlevel='stateful', interface='ar'):
        """"

        :param char: the character for witch to get the attribute
        :param modlevel: the modlevel: ['unaugmented', 'augmented', 'temporary', 'stateful']
        :param interface: the matrix access interface: ['basic', 'ar', 'cold-sim', 'hot-sim']
        """
        CharPropertyGetter.__init__(self, char, modlevel)
        self.interface = interface

    def get_attribute_value(self, attribute):

        conversion_dict = {'Strength': 'Processing',
                           'Agility': 'Uplink',
                           'Body': 'Firewall',
                           'Coordination': 'Logic',
                           'Weight': 75,
                           'Size': 1.75}
        converted_attribute = attribute
        if attribute in conversion_dict:
            converted_attribute = conversion_dict[attribute]
        if isinstance(converted_attribute, str):
            value = CharPropertyGetter.get_attribute_value(self, converted_attribute)
        else:
            value = converted_attribute
        return value

    def get_reaction(self):
        """


        """
        statname = 'Matrix Reaction'
        value = self.stats.get(statname)
        if value:
            return value
        if self.modlevel == 'base':
            value = 0
        if self.modlevel in ('unaugmented', 'augmented','temporary','stateful'):
            value = rules.matrix_reaction(self.get_attribute_mod('Agility'),
                                              self.get_attribute_mod('Intuition'))
        if self.modlevel in ('augmented','temporary','stateful'):
            value = self.char.ware_fix_power_effect('stats', statname, value, modlevel=self.modlevel)
        if self.modlevel in ('temporary','stateful'):
            pass
        self.stats[statname] = value
        return value


class CharAstralPropertyGetter(CharPropertyGetter):
    def __init__(self, char, modlevel):
        """"

        :param char: the character for witch to get the attribute
        :param modlevel: the modlevel: ['unaugmented', 'augmented', 'temporary', 'stateful']
        """
        CharPropertyGetter.__init__(self, char, modlevel)

    def get_attribute_value(self, attribute):

        conversion_dict = {'Strength': 'Charisma',
                           'Agility': 'Logic',
                           'Body': 'Willpower',
                           'Coordination': 'Intuition',
                           'Weight': 'Magic',
                           'Size': 'Magic'}
        converted_attribute = attribute
        if attribute in conversion_dict:
            converted_attribute = conversion_dict[attribute]
        if isinstance(converted_attribute, str):
            value = CharPropertyGetter.get_attribute_value(self, converted_attribute)
        else:
            value = converted_attribute
        return value

    def get_reaction(self):
        """


        """
        statname = 'Astral Reaction'
        value = self.stats.get(statname)
        if value:
            return value
        if self.modlevel == 'base':
            value = 0
        if self.modlevel in ('unaugmented', 'augmented','temporary','stateful'):
            value = rules.astral_reaction(self.get_attribute_mod('Agility'),
                                              self.get_attribute_mod('Intuition'))
        if self.modlevel in ('augmented','temporary','stateful'):
            value = self.char.ware_fix_power_effect('stats', statname, value, modlevel=modlevel)
        if self.modlevel in ('temporary','stateful'):
            pass
        self.stats[statname] = value
        return value


class CharPropertyPutter():
    def __init__(self, char):
        self.char = char

    def first_aid(self, test_value):
        char_property_getter = CharPropertyGetter(self.char, modlevel='stateful')
        max_life = char_property_getter.get_maxlife()
        damage = char_property_getter.char.damage.get('physical', 0)
        damagepercent = damage/float(maxlife)
        healing_mod = rules.healing_mod()
        test_value -= healing_mod
        healed_damage = min(damage, rules.first_aid(test_value)*damagepercent*max_life)
        self.heal_damage(healed_damage, 'physical')
        return 'Healed {} physical damage'.format(healed_damage)

    def rest(self, total_time, medic_test, die_roll):
        timedict = {'m': 1./24./60., 's': 1/24./60./60., 'h': 1/24., 'd': 1, 'w': 7,}
        result = 'Heal Roll: {}\n'.format(die_roll)
        if isinstance(total_time, str):
            splits = total_time.split(',')
            total_time = 0
            for i in splits:
                value, id = float(i.strip()[:-1]), i.strip()[-1]
                total_time += value * timedict.get(id.lower(), 0)
        total_wound_time = total_time
        char_property_getter = CharPropertyGetter(self.char, modlevel='stateful')
        max_life = char_property_getter.get_maxlife()
        test = die_roll + char_property_getter.get_attribute_mod('Constitution')
        test += medic_test if medic_test > 0 else 0
        for damage_kind in sorted(data.damagekinds_dict.values(), key = lambda x: x.priority):
            damage = char_property_getter.char.damage.get(damage_kind.name, 0)
            if damage:
                damagepercent = float(damage)/max_life
                healing_time = rules.healingtime(damagepercent, damage_kind.healing_time, test)
                if total_time >= healing_time:
                    total_time -= healing_time
                    self.heal_damage(damage, damage_kind.name)
                    result += 'Healed all {} {} damage in {} hours\n'.format(damage, damage_kind.name, healing_time * 24.)
                else:
                    damage = rules.damage_heal_after_time(damage, total_time, healing_time)
                    self.heal_damage(damage, damage_kind.name)
                    result += 'Healed {} {} damage in {} hours\n'.format(damage, damage_kind.name, total_time * 24.)
                    break
        wounds = char_property_getter.char.wounds
        for location, wounds_by_location in wounds.items():
            for damage_kind, wound_num in wounds_by_location.items():
                base_time = data.damagekinds_dict[damage_kind].healing_time
                healing_time = rules.healingtime_wounds(wound_num, base_time, test)
                if total_wound_time < healing_time:
                    wound_num = rules.wound_heal_after_time(wound_num, total_wound_time, healing_time)
                    result += 'Healed {} {} wounds at {} in {} hours\n'.format(wound_num, damage_kind, location, total_wound_time * 24.)
                else:
                    result += 'Healed all {} {} wounds at {} in {} hours\n'.format(wound_num, damage_kind, location, healing_time * 24.)
                self.heal_wounds(wound_num, location, damage_kind)
        return result

    def heal_wounds(self, healed_wounds, location, damage_kind=None):
        char_property_getter = CharPropertyGetter(self.char, modlevel='stateful')
        if not damage_kind:
            location, damage_kind = location.split(',')
        wounds = char_property_getter.char.wounds.get(location, {}).get(damage_kind,0)
        wounds = wounds - healed_wounds
        if wounds < 0:
            wounds = 0
        self.char.write_wounds(wounds, location, damage_kind)

    def heal_damage(self, healed_damage, damage_kind):
        char_property_getter = CharPropertyGetter(self.char, modlevel='stateful')
        damage = char_property_getter.char.damage.get(damage_kind, 0)
        damage = damage - healed_damage
        if damage < 0:
            damage = 0
        self.char.write_damage(damage_kind, damage)

    def put_damage(self, value, penetration, bodypart='Body', kind='physical', typ='ballistic',
                   percent=False, resist=False, resistroll=None, wounding = True):
        charpropertygetter = CharPropertyGetter(self.char, 'stateful')
        if kind in ['drain stun', 'drain physical']:
            percent = True
            typ = 'direct'
            resist = 'drain'
            bodypart = 'Body'
            wounding = False
        if not typ or typ == 'direct':
            armor = 0
        else:
            armor = charpropertygetter.get_protection(bodypart, typ)
        if percent:
            value = charpropertygetter.get_maxlife(bodypart)*value/100.
        if resist:
            if resist == 'drain':
                attribute_mod = charpropertygetter.get_drain_resist()
            else:
                attribute_mod = charpropertygetter.get_attribute_mod(resist)
            value = rules.resist_damage(value, attribute_mod, resistroll, 0)
        damage = float(max(0, value - max(0, armor-penetration)))
        bodykind, cyberfraction, biofraction = charpropertygetter.char_body.bodyparts[bodypart].get_kind()
        max_life = charpropertygetter.get_maxlife()
        woundlimit = charpropertygetter.char_body.bodyparts[bodypart].get_woundlimit()
        destroy_thresh = charpropertygetter.char_body.bodyparts[bodypart].get_wounds_destroyed_thresh()
        calc_wounds = float('inf')
        wounds = 0
        if wounding:
            wounds = int(damage/woundlimit)
            calc_wounds = wounds + 1
            old_wounds = self.char.wounds.get(bodypart, 0)
            if old_wounds:
                old_wounds =  old_wounds.get(kind, 0)
            else:
                old_wounds = 0
            if bodykind != 'cyberware' or kind in ('physical'):
                wounds = min(wounds, destroy_thresh-old_wounds)
                calc_wounds = min(calc_wounds, destroy_thresh-old_wounds)
                if wounds:
                    new_wounds = wounds + old_wounds
                    self.char.write_wounds(new_wounds, bodypart, kind)
        if cyberfraction != 1.:
            damage = min(damage, woundlimit*(calc_wounds))
            if not percent:
                damage *= (1.-cyberfraction)
            old_damage = self.char.damage.get(kind, 0)
            new_damage = old_damage + damage
            new_damage = min(new_damage, 2*max_life)
            self.char.write_damage(kind, new_damage)
        result = 'damage: {}, wounds: {}'.format(damage, wounds)
        if resistroll:
            result += '; resistroll:{}'.format(resistroll)
        return result


if __name__ == '__main__':
    body = Body()
