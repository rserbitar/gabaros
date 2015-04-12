# !/usr/bin/env python
# coding: utf8

#from gluon import *
import collections
import data
import rules


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
        self.adept_powers = []
        self.items = []
        self.damage = {}
        self.wounds = {}
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
        self.load_damage()
        self.load_wounds()
        self.load_items()

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
        self.get_loadout()
        db_ci = self.db.char_items
        for row in self.db((db_ci.char == self.char_id) & (db_ci.loadout.contains(self.loadout))).select(db_ci.id, db_ci.item, db_ci.rating):
            self.items.append([row.id, row.item, row.rating])


    def write_attribute(self, attribute, value):
        db_ca = self.db.char_attributes
        self.db((db_ca.char == self.char_id) & (db_ca.attribute == attribute)).update(value=value)

    def write_skill(self, skill, value):
        db_cs = self.db.char_skills
        self.db((db_cs.char == self.char_id) & (db_cs.skill == skill)).update(value=value)

    def write_damage(self, damage, value):
        pass

    @staticmethod
    def write_ware(ware):
        ware.write()

    @staticmethod
    def delete_ware(ware):
        ware.delete()

    def delete_damage(self, damage, value):
        pass


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
        rows = self.db((db_cg.id == self.char) &
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


class Weapon(object):
    def __init__(self, name, char):
        self.char = char
        self.name = name
        self.char_property_getter = CharPropertyGetter(self.char)
        self.get_attributes()

    def get_attributes(self):
        self.skill = data.rangedweapons_dict[self.name].skill
        self.skillmod = data.rangedweapons_dict[self.name].skillmod
        self.damage = data.rangedweapons_dict[self.name].damage
        self.damagetype = data.rangedweapons_dict[self.name].damagetype
        self.penetration = data.rangedweapons_dict[self.name].penetration
        self.range = data.rangedweapons_dict[self.name].range
        self.shot = data.rangedweapons_dict[self.name].shot
        self.burst = data.rangedweapons_dict[self.name].burst
        self.auto = data.rangedweapons_dict[self.name].auto
        self.minstr = data.rangedweapons_dict[self.name].minstr
        self.recoil = data.rangedweapons_dict[self.name].recoil
        self.mag = data.rangedweapons_dict[self.name].mag
        self.magtype = data.rangedweapons_dict[self.name].magtype
        self.top = data.rangedweapons_dict[self.name].top
        self.under = data.rangedweapons_dict[self.name].under
        self.barrel = data.rangedweapons_dict[self.name].barrel
        self.special = data.rangedweapons_dict[self.name].special

    def get_shooting_difficulty(self, distance, magnification=1.):
        return rules.shooting_difficulty(self.range, magnification, distance)

    def get_net_skill_value(self):
        minstr_mod = rules.weapon_minstr_mod(self.minstr, self.char_property_getter.get_attribute_value('Strength'))
        net_skill_value = self.char_property_getter.get_skill_value(self.skill) + self.skillmod - minstr_mod
        return net_skill_value

    def get_damage(self, shoot_mod, distance, bullets = 1, magnification = 1., size = 1.):
        damage = []
        range_mod = rules.shoot_rangemod(self.range, distance)
        sight_mod = rules.visible_perception_mod(size, distance, magnification)
        skill = self.char_property_getter.get_skill_value(self.skill)
        minstr_mod = rules.weapon_minstr_mod(self.minstr, self.char_property_getter.get_attribute_value('Strength'))
        net_value = -rules.shoot_base_difficulty + skill - minstr_mod - range_mod - sight_mod - shoot_mod
        result = net_value
        while net_value >= 0 and bullets:
            damage.append(rules.weapondamage(self.damage, net_value))
            net_value -= self.recoil
            bullets -= 1
        return damage, {'difficulty': rules.shoot_base_difficulty, 'weapon range mod': range_mod,
                        'sight range mod': sight_mod, 'minimum strength mod': minstr_mod,
                        'skill': skill, 'other mods': shoot_mod, 'result': result}


class Armor(object):
    def __init__(self, name, char):
        self.char = char
        self.name = name

    def get_max_agi(self):
        return data.armor_dict[self.name].maxagi

    def get_coordination_mult(self):
        return data.armor_dict[self.name].coordmult

    def get_protection(self, bodypart, kind = 'ballistic'):
        map_dict = {'ballistic': 0,
                    'impact': 1}
        index = data.armor_dict[self.name].locations.index(bodypart)
        return data.armor_dict[self.name].protections[index][map_dict[kind]]

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


class Ware(object):
    def __init__(self, db, name):
        self.db = db
        self.name = name
        self.kind = None
        self.charismamod = None
        self.part_weight = None
        self.additional_weight = None
        self.description = None
        self.basecost = None
        self.cost = None
        self.parts = None
        self.effects = None
        self.location = None
        self.load_basic_data()

    def load_basic_data(self):
        ware_nt = data.ware_dict[self.name]
        self.kind = ware_nt.kind
        self.charismamod = ware_nt.charismamod
        self.part_weight = ware_nt.part_weight
        self.additional_weight = ware_nt.additional_weight
        self.description = ware_nt.description
        self.basecost = ware_nt.basecost
        self.cost = ware_nt.cost
        self.parts = ware_nt.parts
        self.effects = ware_nt.effects
        self.location = ware_nt.location


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

    def init_body(self):
        self.place_bodypart(self.body.bodyparts['Body'], None)

    def place_ware(self):
        for ware in self.char.ware:
            if ware.parts:
                for part in ware.parts:
                    self.place_bodypart(part, ware)

    def place_bodypart(self, part, ware):
        if isinstance(part, basestring):
            part = self.body.bodyparts[part]
        self.bodyparts[part.name] = CharBodypart(self.char, self, part, ware)
        for child in part.children:
            self.place_bodypart(child, ware)

    def get_bodypart_composition(self, name):
        pass

    def get_location_ware(self, name):
        pass


BodyFractions = collections.namedtuple('BodyFraction',
                                       ['Weight', 'Size', 'Charisma', 'Agility',
                                        'Coordination', 'Strength', 'Constitution'])


class Bodypart(object):
    def __init__(self, body, name):
        self.body = body
        self.name = name
        self.template = None
        self.parent = None
        self.body_fractions = None
        self.children = []
        self.load_data()

    def load_data(self):
        bodypart_nt = data.bodyparts_dict[self.name]
        self.template = bodypart_nt.template
        self.parent = self.body.bodyparts.get(bodypart_nt.parent, None)
        self.relative_body_fractions = BodyFractions(Weight=bodypart_nt.weightfrac,
                                                     Size=bodypart_nt.sizefrac,
                                                     Charisma=bodypart_nt.charismafrac,
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
        return 'unaugmented'


class CharBodypart():
    def __init__(self, char, char_body, bodypart, ware):
        self.char_body = char_body
        self.char = char
        self.bodypart = bodypart
        self.ware = ware
        self.wounds = char.wounds.get(bodypart.name, {})
    def get_kind(self):
        if self.ware:
            return self.ware.kind
        else:
            return self.bodypart.get_kind()

    def get_attribute_absolute(self, attribute, modlevel='stateful'):
        if self.bodypart.children:
            child_char_bodyparts = [self.char_body.bodyparts[child.name] for child in self.bodypart.children]
            value = sum([part.get_attribute_absolute(attribute, modlevel) for part in child_char_bodyparts])
            if modlevel == 'stateful':
                if self.wounds and attribute not in ('Size', 'Weight', 'Constitution'):
                    value = rules.woundeffect(value, sum(self.wounds.values()))
            return value
        else:
            value = self.char.attributes[attribute]
            if modlevel in ('augmented', 'temporary', 'stateful'):
                if self.ware:
                    value = self.ware.stats[attribute]
            if modlevel == 'stateful':
                if self.wounds and attribute not in ('Size', 'Weight', 'Constitution'):
                    value = rules.woundeffect(value, sum((self.wounds.values())))
            fraction = self.bodypart.get_fraction(attribute)
            return value*fraction

    def get_life(self):
        if self.bodypart.children:
            child_char_bodyparts = [self.char_body.bodyparts[child.name] for child in self.bodypart.children]
            return sum([part.get_life() for part in child_char_bodyparts])
        else:
            weight = self.get_attribute_relative('Weight')
            constitution = self.get_attribute_relative('Constitution')
            fraction = self.bodypart.get_fraction('Weight')
            life = fraction * rules.life(weight, constitution)
            return life

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
        self.maxlife = None

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
            value = self.char.attributes[attribute]
        # augmented modlevel includes permanent modifications including cyberware, bioware, adept powers and more
        # temporary modlevel includes drugs, spells, encumbrance
        # stateful modlevel includes damage
        elif self.modlevel in ('augmented', 'temporary', 'stateful'):
            # calculate body part contribution to attribute
            if attribute == 'Weight':
                #implicitly includes wounds
                value = self.char_body.bodyparts['Body'].get_attribute_absolute(attribute, self.modlevel)
            elif data.attributes_dict[attribute].kind == 'physical':
                #implicitly includes wounds
                value = self.char_body.bodyparts['Body'].get_attribute_absolute(attribute, self.modlevel)
            else:
                value = self.char.attributes[attribute]
            # add adept power effects
            for adept_power in self.char.adept_powers:
                if adept_power.effect[0] == 'attributes' and adept_power.effect[1] == attribute:
                        magic = self.get_attribute_value('Magic')
                        formula = adept_power.effect[2].format(Value = adept_power.value, Magic = magic)
                        value = eval('value {}'.format(formula))
            # add ware effects to attribute
            for ware in self.char.ware:
                for effect in ware.effects:
                    if effect[0] == 'attributes' and effect[1] == attribute:
                        value = eval('value {}'.format(effect[2]))
            # calculate armor modifications
            if self.modlevel in ('stateful'):
                if attribute == 'Agility':
                    for armor in self.get_armor():
                        value = min(value, armor.get_max_agi())
                if attribute == 'Coordination':
                    for armor in self.get_armor():
                        value *= armor.get_coordination_mult()
        # store calculated value
        if self.modlevel == 'stateful':
            value *= self.get_damagemod('relative')
        self.attributes[attribute] = value
        return value

    def get_attribute_mod(self, attribute):
        """

        :param attribute: the attribute to get
        """
        value = self.get_attribute_value(attribute)
        base = data.attributes_dict[attribute].base
        return rules.attrib_mod(value, base)

    def get_attribute_test_value(self, attribute):

        value = self.get_attribute_mod(attribute) + 30
        return value

    def get_skill_value(self, skill):
        """

        :param skill: the skill to get
        """
        value = self.skills.get(skill)
        if value:
            return value
        if self.modlevel == 'base':
            value = self.char.skills[skill]
        if self.modlevel in ('unaugmented', 'augmented','temporary','stateful'):
            value = self.char.skills.get(skill,0)
            parent = data.skills_dict[skill].parent
            if parent:
                parent_value = self.get_skill_value(parent)
                if value < parent_value:
                    value = parent_value
        if self.modlevel in ('augmented','temporary','stateful'):
            for adept_power in self.char.adept_powers:
                if adept_power.effect[0] == 'skills' and adept_power.effect[1] == skill:
                        magic = self.get_attribute_value('Magic')
                        formula = adept_power.effect[2].format(Value = adept_power.value, Magic = magic)
                        value = eval('value {}'.format(formula))
            for ware in self.char.ware:
                for effect in ware.effects:
                    if effect[0] == 'skills' and effect[1] == skill:
                        value = eval('value {}'.format(effect[2]))
        if self.modlevel in ('temporary','stateful'):
            pass
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
            weight = getattr(skill_attribmods, attribute)
            if weight:
                mod += weight * self.get_attribute_mod(attribute)/2.
        value += mod
        return value


    def get_armor(self):
        armor = [name for id, name, rating in self.char.items if data.gameitems_dict[name].clas == 'Armor']
        armor = [Armor(name, self.char) for name in armor]
        return armor

    def get_weapons(self):
        weapons = [name for id, name, rating in self.char.items if data.gameitems_dict[name].clas == 'Ranged Weapon']
        weapons = [Weapon(name, self.char) for name in weapons]
        return weapons

    def get_maxlife(self):
        value = self.maxlife
        if value:
            return value
        if self.modlevel == 'base':
            weight = self.get_attribute_value('Weight')
            constitution = self.get_attribute_value('Constition')
            value = rules.life(weight, constitution)
        elif self.modlevel == 'unaugmented':
            pass
        elif self.modlevel in ('augmented', 'temporary', 'stateful'):
            value = self.char_body.bodyparts['Body'].get_life()
            for ware in self.char.ware:
                for effect in ware.effects:
                    if effect[0] == 'stats' and effect[1] == 'life':
                        value = eval('value {}'.format(effect[2]))
        self.maxlife = value
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
        for ware in self.char.ware:
            for effect in ware.effects:
                if effect[0] == 'stats' and effect[1] == statname:
                    pain_resistance += (1- pain_resistance)* eval('value {}'.format(effect[2]))
        for power in self.char.adept_powers:
            for effect in power.effects:
                if effect[0] == 'stats' and effect[1] == statname:
                    pain_resistance += (1- pain_resistance)* eval('value {}'.format(effect[2]))
        max_life = self.get_maxlife()
        if kind == 'relative':
            damagemod = rules.lifemod_relative(max_life - max(0, totaldamage - pain_resistance * max_life), max_life)
        elif kind == 'absolute':
            damagemod = rules.lifemod_absolute(max_life - max(0, totaldamage - pain_resistance * max_life), max_life)
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
            for ware in self.char.ware:
                for effect in ware.effects:
                    if effect[0] == 'stats' and effect[1] == statname:
                        value = eval('value {}'.format(effect[2]))
            for power in self.char.adept_powers:
                for effect in power.effects:
                    if effect[0] == 'stats' and effect[1] == statname:
                        value = eval('value {}'.format(effect[2]))
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
            for ware in self.char.ware:
                for effect in ware.effects:
                    if effect[0] == 'stats' and effect[1] == statname:
                        value = eval('value {}'.format(effect[2]))
            for power in self.char.adept_powers:
                for effect in power.effects:
                    if effect[0] == 'stats' and effect[1] == statname:
                        value = eval('value {}'.format(effect[2]))
        if self.modlevel in ('temporary','stateful'):
            pass
        self.stats[statname] = value
        return value


    def get_actioncost(self, kind):
        actionmult = self.get_actionmult()
        cost = rules.action_cost(kind, actionmult)
        return cost


    def get_total_exp(self):
        """


        """
        pass


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
        pass

    def get_jump_height(self, movement):
        pass

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
            for ware in self.char.ware:
                for effect in ware.effects:
                    if effect[0] == 'stats' and effect[1] == statname:
                        value = eval('value {}'.format(effect[2]))
            for power in self.char.adept_powers:
                for effect in power.effects:
                    if effect[0] == 'stats' and effect[1] == statname:
                        value = eval('value {}'.format(effect[2]))
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
            for ware in self.char.ware:
                for effect in ware.effects:
                    if effect[0] == 'stats' and effect[1] == statname:
                        value = eval('value {}'.format(effect[2]))
            for power in self.char.adept_powers:
                for effect in power.effects:
                    if effect[0] == 'stats' and effect[1] == statname:
                        value = eval('value {}'.format(effect[2]))
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

    def get_drain_resistance(self):
        pass

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
            for ware in self.char.ware:
                for effect in ware.effects:
                    if effect[0] == 'stats' and effect[1] == statname:
                        value = eval('value {}'.format(effect[2]))
            for power in self.char.adept_powers:
                for effect in power.effects:
                    if effect[0] == 'stats' and effect[1] == statname:
                        value = eval('value {}'.format(effect[2]))
        if self.modlevel in ('temporary','stateful'):
            pass
        self.stats[statname] = value
        return value


if __name__ == '__main__':
    body = Body()