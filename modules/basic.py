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
        self.damage = []
        self.load_char()
        self.load_attributes()
        self.load_skills()
        self.load_ware()
        self.load_damage()

    def init_attributes(self):
        char_property_getter = CharPropertyGetter(self, 'base')
        for attribute in data.attributes_dict.keys():
            value = char_property_getter.get_attribute_value(attribute)
            self.db.char_attributes.bulk_insert([{'char': self.char_id, 'attribute': attribute, 'value': value}])

    def init_skills(self):
        for name, skill in data.skills_dict.items():
            self.db.char_skills.bulk_insert([{'char': self.char_id, 'skill': name, 'value': 0}])

    def load_char(self):
        row = self.db.chars[self.char_id]
        self.name = row.name
        self.gender = row.gender
        self.race = row.race

    def load_attributes(self):
        """

        Load character attributes, if not present, use 30
        """
        db_ca = self.db.char_attributes
        if not self.db(db_ca.char == self.char_id).select().first():
            self.init_attributes()
        for row in self.db(db_ca.char == self.char_id).select(db_ca.attribute, db_ca.value):
            self.attributes[row.attribute] = row.value

    def load_skills(self):
        """

        Load char skills, if not present, use 0
        """
        db_cs = self.db.char_skills
        if not self.db(db_cs.char == self.char_id).select().first():
            self.init_skills()
        for row in self.db(db_cs.char == self.char_id).select(db_cs.skill, db_cs.value):
            self.skills[row.skill] = row.value

    def load_damage(self):
        pass

    def load_ware(self):
        """

        Load character ware
        """
        db_cw = self.db.char_ware
        for row in self.db(db_cw.char == self.char_id).select(db_cw.ware, db_cw.id):
            self.ware.append(CharWare(self.db, row.ware, row.id, self))

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


class Cyberdeck(object):
    def __init__(self, cyberdeck):
        """
        :param cyberdeck: the cyberdeck id from the database
        """
        self.cyberdeck = cyberdeck
        self.attributes = {}
        self.programms = {}
        self.damage = []
        self.mode = None

    def load_attributes(self):
        pass

    def load_damage(self):
        pass

    def load_programms(self):
        pass

    def write_attribute(self, attribute, value):
        pass

    def write_program(self, programme, value):
        pass

    def write_damage(self, damage, value):
        pass

    def delete_program(self, programme, value):
        pass

    def delete_damage(self, damage, value):
        pass

    def get_attribute(self, attribute):
        pass

    def get_programms(self):
        pass

    def add_program(self, programm):
        pass

    def remove_program(self, program):
        pass

    def get_mode(self):
        pass

    def set_mode(self, mode):
        pass

    def write_mode(self, mode):
        pass


class CharMatrix(Char):
    def __init__(self, db, char, cyberdeck=None):
        """"

        :param char: the character for witch to get the attribute
        :param cyberdeck: the cyberdeck the character is using for his matrix persona
        """
        Char.__init__(self, db, char)
        self.cyberdeck = Cyberdeck(cyberdeck)


class CharAstral(Char):
    def __init__(self, db, char):
        """"

        :param char: the character for witch to get the attribute
        """
        Char.__init__(self, db, char)


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

    def load_data(self):
        ware_nt = data.ware_dict(self.name)
        self.kind = ware_nt.kind
        self.charismamod = ware_nt.charismamod
        self.part_weight = ware_nt.weight
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
        self.load_data()
        #self.weight = self.calc_absolute_weight()

    def init_stats(self):
        char_property_getter = CharPropertyGetter(self.char, 'base')
        for name, attribute in data.attributes_dict.items():
            if attribute.kind == 'physical':
                value = char_property_getter.get_attribute_value(attribute.name)
                self.db.char_ware_stats.bulk_insert([{'ware': self.db_id, 'stat': attribute.name, 'value': value}])

    def load_data(self):
        db_cws = self.db.char_ware_stats
        if not self.db(db_cws.ware == self.db_id).select().first():
            self.init_stats()
        for row in self.db(db_cws.id == self.db_id).select(db_cws.stat, db_cws.value):
            self.stats[row.stat] = row.value

    def write(self):
        db_cw = self.db.char_ware
        if self.db_id is not None:
            self.db_id = db_cw.insert(char=self.char.char_id, ware=self.ware_name)
        else:
            self.db(db_cw.id == self.db_id).update(char=self.char.char_id, ware=self.ware_name)

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


class Body(object):
    def __init__(self):
        self.bodyparts = {}

    def get_bodypart(self, name):
        return self.bodyparts[name]

    def set_bodypart(self, name, bodypart):
        self.bodypart[name] = bodypart


class CharBody():
    def __init__(self, char):
        self.char = char
        self.body = Body()
        self.init_body()
        self.place_ware()

    def init_body(self):
        pass

    def place_ware(self):
        for ware in self.char.ware:
            if ware.parts:
                for part in ware.parts:
                    self.place_bodypart(part, ware)

    def place_bodypart(self, part, ware):
        self.body.set_bodypart(part, CharBodypart(part, ware.stats, ware))
        for child in self.body.get_bodypart(part).children:
            self.place_bodypart(child, ware)

    def get_bodypart_composition(self, name):
        pass

    def get_location_ware(self, name):
        pass


BodyFractions = collections.namedtuple('BodyFraction',
                                       ['Weight', 'Charisma', 'Agility', 'Coordination', 'Strength', 'Constitution'])


class Bodypart(object):
    def __init__(self, name):
        self.name = name
        self.template = None
        self.parent = None
        self.body_fractions = None
        self.children = None
        self.load_data()

    def load_data(self):
        bodypart_nt = data.bodyparts_dict(self.name)
        self.template = bodypart_nt.template
        self.parent = bodypart_nt.parent
        self.body_fractions = BodyFractions(weight=bodypart_nt.weightfrac, charisma=bodypart_nt.charismafrac,
                                            agility=bodypart_nt.agilityfrac, coordination=bodypart_nt.coordinationfrac,
                                            strength=bodypart_nt.strengthfrac,
                                            constitution=bodypart_nt.constitutionfrac)
        self.children = [i.name for i in data.bodyparts_dict.values() if i.parent == self.name]

    def get_fraction(self, attribute):
        return getattr(self.body_fractions, attribute)

    def get_kind(self):
        return 'unaugmented'


class CharBodypart(Bodypart):
    def __init__(self, name, stats, ware):
        Bodypart.__init__(self, name)
        self.ware = ware
        self.stats = stats

    def get_kind(self):
        if self.ware:
            return self.ware.kind
        else:
            return Bodypart.get_kind()

    def get_attribute(self, attribute):
        value = [i[2] for i in self.stats if i[0] == 'attributes' and i[1] == attribute][0]
        fraction = self.get_fraction()
        return value, fraction

modlevels = ['base', 'unaugmented', 'augmented', 'temporary', 'stateful']
interfaces = ['basic', 'ar', 'cold-sim', 'hot-sim']


class CharPropertyGetter():
    def __init__(self, char, modlevel='stateful'):
        """"
        :param modlevel: the modlevel: ['unaugmented', 'augmented', 'temporary', 'stateful']
        """
        self.char = char
        self.modlevel = modlevel

    def get_attribute_value(self, attribute):
        """

        :param attribute: the attribute to get
        """
        value = None
        if self.modlevel == 'base':
            value = data.attributes_dict[attribute].base
            if attribute == 'Weight':
                size = self.get_attribute_value('Size')
                size_base = data.attributes_dict['Size'].base
                value = rules.calc_base_weight(value, size, size_base)
            elif attribute in ['Strength', 'Agility']:
                size = self.get_attribute_value('Size')
                size_base = data.attributes_dict['Size'].base
                weight = self.get_attribute_value('Weight')
                weight_base = data.attributes_dict['Weight'].base
                if attribute == 'Strength':
                    value = rules.calc_base_strength(value, size, size_base, weight, weight_base)
                elif attribute == 'Agility':
                    value = rules.calc_agility_base(value, weight, weight_base)
            if self.char.gender and self.char.race:
                value *= getattr(data.gendermods_dict[self.char.gender], attribute)
                value *= getattr(data.races_dict[self.char.race], attribute)
        elif self.modlevel == 'unaugmented':
            value = self.char.attributes[attribute]
        return value

    def get_attribute_mod(self, attribute):
        """

        :param attribute: the attribute to get
        """
        value = self.get_attribute_value(attribute)
        base = data.attributes_dict[attribute].base
        return rules.attrib_mod(value, base)

    def get_skill_value(self, skill):
        """

        :param skill: the skill to get
        """
        value = None
        if self.modlevel == 'unaugmented':
            value = self.char.skills[skill]
        return value

    def get_skilltest_value(self, skill):
        """

        :param skill: the skill to get
        """
        value = self.get_skill_value(skill)
        mod = 0
        skill_attribmods = data.skills_attribmods_dict[skill]
        for attribute in data.attributes_dict.keys():
            weight = skill_attribmods.get(attribute)
            if weight:
                mod += weight * self.get_attribute_mod(attribute)
        return value + mod

    def get_armor(self, kind='ballistic'):
        """

        :param kind:
        """
        pass

    def get_damagemod(self):
        """


        """
        pass

    def get_initiative(self):
        """


        """
        pass

    def get_total_exp(self):
        """


        """
        pass


class LoadoutPropertyGetter(Loadout):
    def __init__(self, char):
        """"
        :param char: the character for witch to get the attribute
        """
        Loadout.__init__(self, char)


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

    def get_initiative(self):
        pass


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

        conversion_dict = {'Strength': 'Logic',
                           'Agility': 'Intuition',
                           'Body': 'Willpower',
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

    def get_initiative(self):
        pass


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

    def get_initiative(self):
        pass
