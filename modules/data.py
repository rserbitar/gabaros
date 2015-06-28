#!/usr/bin/env python
# coding: utf8
# from gluon import *

#!/usr/bin/env python
# coding: utf8
# request, response, session, cache, T, db(s)
# must be passed and cannot be imported!

from collections import namedtuple, OrderedDict


def replace_stars(data):
    for i, v in enumerate(data):
        for i2, v2 in enumerate(v):
            if isinstance(v2, str) and "*" in v2:
                data[i][i2] = v2.replace("*", data[i][data[0].index("parent")])


converted = ['attributes', 'bodyparts', 'stats', 'skill_attribmods']

states = ["Physical Damage",
          "Stun Damage",
          "Head Wounds",
          "Upper Body Wounds",
          "Lower Body Wounds",
          "Left Arm Wounds",
          "Right Arm Wounds",
          "Left Leg Wounds",
          "Right Leg Wounds",
          "Stunned",
          "Unconscious"]

permits = [
    ["name", "cost_multiplier"],
    ['none', 1],
    ['security', 2],
    ['military', 5]
]

permits_nt = namedtuple('permits', ['id'] + permits[0])
permits_dict = OrderedDict([(entry[0], permits_nt(*([i] + entry))) for i, entry in enumerate(permits[1:])])

damagekinds = [
    ["name", "healing_time", "description", "priority"],
    ["fatigue", 1 / 2.4, "Damage gained by physical exertion", 1],
    ["stun", 10, "Bruises,...", 10],
    ["physical", 600, "", 100],
    ["drain stun", 5, "Drain Stun", 5],
    ["drain physical", 200, "Drain Physical", 50]
]

damagekinds_nt = namedtuple('damagekind', ['id'] + damagekinds[0])
damagekinds_dict = OrderedDict([(entry[0], damagekinds_nt(*([i] + entry))) for i, entry in enumerate(damagekinds[1:])])

statclasses = [
    ["name", "parent"],
    ["Char", None],
    ["Item", None],
    ["Attributes", "Char"],
    ["Ware", "Item"],
    ["Cyberware", "Ware"],
    ["Bioware", "Ware"],
    ["Nanoware", "Ware"],
    ["Genetech", "Ware"],
    ["Weapon", "Item"],
    ["Ranged Weapon", "Weapon"],
    ["Melee Weapon", "Weapon"],
    ["Armor", "Item"],
    ["Sensor", "Item"],
    ["Cyberdeck", "Item"]
]

stats = [
    ["name", "clas", "parent", "type"],
    ["Action Costs", "Char", None, "float"],
    ["Awareness Costs", "Char", "Action Costs", "float"],
    ["Time Costs", "Char", "Action Costs", "float"],
    ["Physical Awareness", "Char", "Awareness Costs", "float"],
    ["Physical Time", "Char", "Time Costs", "float"],
    ["Move Awareness", "Char", "Physical Awareness Costs", "float"],
    ["Move Time", "Char", "Physical Time Costs", "float"],
    ["Shift Awareness", "Char", "Physical Awareness Costs", "float"],
    ["Shift Time", "Char", "Physical Time Costs", "float"],
    ["Meta Awareness", "Char", "Awareness Costs", "float"],
    ["Meta Time", "Char", "Time Costs", "float"],
    ["General Awareness", "Char", "Awareness Costs", "float"],
    ["General Time", "Char", "Time Costs", "float"],
    ["Combat Awareness", "Char", "Physical Awareness Costs", "float"],
    ["Combat Time", "Char", "Physical Time Costs", "float"],
    ["Melee Combat Awareness", "Char", "Combat Awareness", "float"],
    ["Melee Combat Time", "Char", "Combat Time", "float"],
    ["Ranged Combat Awareness", "Char", "Combat Awareness", "float"],
    ["Ranged Combat Time", "Char", "Combat Time", "float"],
    ["Astral Awareness", "Char", "Awareness Costs", "float"],
    ["Astral Time", "Char", "Time Costs", "float"],
    ["Matrix Awareness", "Char", "Awareness Costs", "float"],
    ["Matrix Time", "Char", "Time Costs", "float"],
    ["Name", "Char", None, "str"],
    ["Streetname", "Char", None, "str"],
    ["Date of Birth", "Char", None, "date"],
    ["Skintone", "Char", None, "str"],
    ["Eyecolor", "Char", None, "str"],
    ["Hairstyle", "Char", None, "str"],
    ["Haircolor", "Char", None, "str"],
    ["Loadout", "Char", None, "int"],
    ["Woundlimit", "Char", None, "float"],
    ["Life", "Char", None, "float"],
    ["Carriing Capacity", "Char", None, "float"],
    ["Initiative", "Char", None, "float"],
    ["Reaction", "Char", None, "float"],
    ["Physical Initiative", "Char", "Initiative", "float"],
    ["Physical Reaction", "Char", "Reaction", "float"],
    ["Matrix Initiative", "Char", "Initiative", "float"],
    ["Matrix Reaction", "Char", "Reaction", "float"],
    ["Astral Initiative", "Char", "Initiative", "float"],
    ["Astral Reaction", "Char", "Reaction", "float"],
    ["Legality", "Item", None, "float"],
    ["Visible Stealth Rating", "Item", None, "float"],
    ["Scan Stealth Rating", "Item", None, "float"],
    ["Ballistic Armor", "Armor", None, "float"],
    ["Impact Armor", "Armor", None, "float"],
    ["Shielding", "Armor", None, "float"],
    ["Insulation", "Armor", None, "float"],
    ["Agility Cap", "Armor", None, "float"],
    ["Coordination Multiplier", "Armor", None, "float"],
    ["Damage", "Weapon", None, "float"],
    ["Damagetype", "Weapon", None, "str"],
    ["Penetration", "Weapon", None, "float"],
    ["Range", "Weapon", None, "float"],
    ["Single Shot Rate", "Weapon", None, "integer"],
    ["Burst Shot Rate", "Weapon", None, "integer"],
    ["Auto Shot Rate", "Weapon", None, "integer"],
]

stats_nt = namedtuple('stat', ['id'] + stats[0])
stats_dict = OrderedDict([(entry[0], stats_nt(*([i] + entry))) for i, entry in enumerate(stats[1:])])

races = [
    ["name", "Size", "Weight", "Agility", "Constitution", "Coordination", "Strength", "Charisma", "Intuition", "Logic",
     "Willpower", "Magic", "Edge", "xpcost"],
    ["Human", 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 0],
    ["Troll", 1.33, 1.33, 0.9, 1.33, 0.67, 1.1, 0.83, 1.33, 0.67,
     0.67, 1, 1, 0],
    ["Orc", 1.1, 1.33, 1.2, 1.33, 1, 1.2, 0.67, 1.17, 0.67,
     1.33, 1, 1, 0],
    ["Elf", 1.1, 0.8, 1.40, 0.9, 1.17, 0.8, 1.17, 1, 1,
     1, 1, 1, 0],
    ["Dwarf", 0.75, 1.4, 0.8, 1.33, 1.17, 1.5, 1, 1, 1,
     1.33, 1, 1, 0],
]

races_nt = namedtuple('race', ['id'] + races[0])
races_dict = OrderedDict([(entry[0], races_nt(*([i] + entry))) for i, entry in enumerate(races[1:])])

gendermods = [
    ["name", "Size", "Weight", "Agility", "Constitution", "Coordination", "Strength", "Charisma", "Intuition", "Logic",
     "Willpower", "Magic", "Edge"],
    ["Male", 1.05, 1, 1, 1, 1, 1.05, 0.9, 1, 1, 1, 1, 1],
    ["Female", 0.95, 1, 1, 1, 1, 0.95, 1.1, 1, 1, 1, 1, 1],
]

gendermods_nt = namedtuple('gendermod', ['id'] + gendermods[0])
gendermods_dict = OrderedDict([(entry[0], gendermods_nt(*([i] + entry))) for i, entry in enumerate(gendermods[1:])])

attributes = [
    ["name", "base", "description", "factor", "signmod", "kind"],
    ["Size", 1.75, "size of a character in meteres", 5000, -1, "special"],
    ["Weight", 75, "weight of the character in kg", 2000, -1, "special"],
    ["Agility", 30, "speed of muscle movement, dexterity of limbs..", 1000, 1, "physical"],
    ["Constitution", 30, "ability to endure fatigue, bodily toughness, resitance to poinson and disease", 1000, 1,
     "physical"],
    ["Coordination", 30, "ability to coordinate agility and strength", 1000, 1, "physical"],
    ["Strength", 30, "raw physical strength", 1000, 1, "physical"],
    ["Charisma", 30, "empathy, ability to influence others", 1000, 1, "mental"],
    ["Intuition", 30, "unconsciousness thinking, ability to recognize patterns", 1000, 1, "mental"],
    ["Logic", 30, "raw mental processing power", 1000, 1,  "mental"],
    ["Willpower", 30, "ability to resist temptations and influence of others", 1000, 1, "mental"],
    ["Magic", 30, "the ability to channel magic", 2000, 1, "special"],
    ["Edge", 30, "luck, the ability to excel in dangerous situations", 1000, 1, "special"],
]

attributes_nt = namedtuple('attribute', ['id'] + attributes[0])
attributes_dict = OrderedDict([(entry[0], attributes_nt(*([i] + entry))) for i, entry in enumerate(attributes[1:])])

skills = [
    ["name", "parent", "expweight"],
    ["Combat", None, 8.44],
    ["Armed Combat", "Combat", 2.25],
    ["Impact Weapons", "Armed Combat", 1],
    ["Piercing Weapons", "Armed Combat", 1],
    ["Slashing Weapons", "Armed Combat", 1],
    ["Unarmed Combat", "Combat", 1.5],
    ["Brawling", "Unarmed Combat", 1],
    ["Wrestling", "Unarmed Combat", 1],
    ["Thrown Weapons", "Combat", 2.25],
    ["Aerodynamics", "Thrown Weapons", 1],
    ["Axes", "Thrown Weapons", 1],
    ["Balls", "Thrown Weapons", 1],
    ["Ranged Weapons", "Combat", 5.25],
    ["Archery", "Ranged Weapons", 1],
    ["Pistols", "Ranged Weapons", 1],
    ["Automatics", "Ranged Weapons", 1],
    ["Long Rifle", "Ranged Weapons", 1],
    ["Indirect Fire", "Ranged Weapons", 1],
    ["Launch Weapons", "Ranged Weapons", 1],
    ["Spray Weapons", "Ranged Weapons", 1],
    ["Physical", None, 8.44],
    ["Acrobatics", "Physical", 2.5],
    ["Balance", "Acrobatics", 1],
    ["Dodge", "Acrobatics", 1],
    ["Athletics", "Physical", 2.],
    ["Climbing", "Athletics", 0.5],
    ["Jumping", "Athletics", 0.5],
    ["Lifting", "Athletics", 0.5],
    ["Running", "Athletics", 0.5],
    ["Swimming", "Athletics", 0.5],
    ["Carouse", "Physical", 0.75],
    ["Perform", "Physical", 1.5],
    ["Dancing", "Perform", 1],
    ["Singing", "Perform", 1],
    ["Stealth", "Physical", 2.25],
    ["Hideing", "Stealth", 1],
    ["Shadowing", "Stealth", 1],
    ["Sneaking", "Stealth", 1],
    ["Sleight of Hand", "Physical", 2.25],
    ["Lockpicking", "Sleight of Hand", 1],
    ["Pickpocketing", "Sleight of Hand", 1],
    ["Quickdrawing", "Sleight of Hand", 1],
    ["Processing", None, 7.31],
    ["Art", "Processing", 1.5],
    ["Painting", "Art", 1],
    ["Sculpting", "Art", 1],
    ["Composure", "Processing", 1.5],
    ["Mental Composure", "Composure", 1],
    ["Physical Composure", "Composure", 1],
    ["Memory", "Processing", 1],
    ["Navigation", "Processing", 2.25],
    ["Orientation", "Navigation", 1],
    ["Land", "Navigation", 0.5],
    ["Sea", "Navigation", 0.5],
    ["Space", "Navigation", 0.5],
    ["Air", "Navigation", 0.5],
    ["Perception", "Processing", 2.25],
    ["Aural", "Perception", 1],
    ["Olfactorial", "Perception", 0.5],
    ["Tactile", "Perception", 0.5],
    ["Visual", "Perception", 1],
    ["Judge Person", "Processing", 2.25],
    ["Guess Intentions", 'Judge Person', 1],
    ["Detect Deceit", "Judge Person", 1],
    ["Interrogation", "Judge Person", 1],
    ["Empathy", None, 6.75],
    ["Act", "Empathy", 1.5],
    ["Theatrical", "Act", 1],
    ["Impersonation", "Act", 1],
    ["Animal Controll", "Empathy", 1.5],
    ["Animal Training", "Animal Controll", 1],
    ["Animal Riding", "Animal Controll", 1],
    ["Discussion", "Empathy", 2.25],
    ["Convince", "Discussion", 1],
    ["Instruction", "Discussion", 1],
    ["Negotiation", "Discussion", 1],
    ["Interaction", "Empathy", 3.75],
    ["Deception", "Interaction", 1],
    ["Intimidation", "Interaction", 1],
    ["Leadership", "Interaction", 1],
    ["Persuasion", "Interaction", 1],
    ["Oratory", "Interaction", 1],
    ["Magic", None, 4.86],
    ["Askenning", "Magic", 1],
    ["Sorcery", "Magic", 2.25],
    ["Spellcasting", "Sorcery", 1],
    ["Counterspelling", "Sorcery", 1],
    ["Ritual Magic", "Sorcery", 1],
    ["Invocation", "Magic", 2.25],
    ["Binding", "Invocation", 1],
    ["Banishing", "Invocation", 1],
    ["Summoning", "Invocation", 1],
    ["Alchemy", "Magic", 1],
    ["Matrix", None, 5.63],
    ["Computers", "Matrix", 3],
    ["Data Search", "Computers", 1],
    ["Programming", "Computers", 1],
    ["Computer Use", "Computers", 2],
    ["Hacking", "Matrix", 4.5],
    ["Cracking", "Hacking", 2],
    ["Cybercombat", "Hacking", 1],
    ["Decryption", "Hacking", 1],
    ["Security", "Hacking", 2],
    ["Technical", None, 7.88],
    ["Chemistry", "Technical", 1.5],
    ["Toxins", "Chemistry", 1],
    ["Demolitions", "Chemistry", 1],
    ["Electronics", "Technical", 3],
    ["Maglocks", "Electronics", 1],
    ["Sensors", "Electronics", 1],
    ["Optical Computers", "Electronics", 1],
    ["Electronic Warfare", "Electronics", 1],
    ["Mechanics", "Technical", 2.25],
    ["Locks", "Mechanics", 1],
    ["Weapons", "Mechanics", 1],
    ["Traps", "Mechanics", 1],
    ["Medics", "Technical", 2.25],
    ["Cybernetics", "Medics", 1],
    ["Extended Care", "Medics", 1],
    ["First Aid", "Medics", 1],
    ["Social", "Technical", 1.5],
    ["Disguise", "Social", 1],
    ["Forgery", "Social", 1],
    ['Locomotion', None, 6.19],
    ['Vehicle Mechanics', 'Locomotion', 3],
    ["Ground Vehicle Mechanics", "Vehicle Mechanics", 1],
    ["Airborne Vehicle Mechanics", "Vehicle Mechanics", 1],
    ["Spacecraft Mechanics", "Vehicle Mechanics", 1],
    ["Watercraft Mechanics", "Vehicle Mechanics", 1],
    ["Pilot", "Locomotion", 5.25],
    ["Airplane", "Pilot", 1],
    ["Hovercraft", "Pilot", 1],
    ["Helicopter", "Pilot", 1],
    ["Submarine", "Pilot", 1],
    ["Thrust", "Pilot", 1],
    ["Watercraft", "Pilot", 1],
    ["Wheeled", "Pilot", 1],
]

skills_nt = namedtuple('skill', ['id'] + skills[0])
skills_dict = OrderedDict([(entry[0], skills_nt(*([i] + entry))) for i, entry in enumerate(skills[1:])])

skill_attribmods = [['skill', 'Agility', 'Constitution', 'Coordination', 'Strength', 'Weight',
                     'Charisma', 'Intuition', 'Logic', 'Willpower', 'Magic', 'Size'],
                    ["Combat", 0.25, 0, 0.25, 0, 0, 0, 0.25, 0, 0, 0, 0],
                    ["Armed Combat", 1., 0, 0.25, 0, 0, 0, 0.5, 0, 0, 0, 0],
                    ["Impact Weapons", 1., 0, 0.25, 0, 0, 0, 0., 0, 0, 0, 0],
                    ["Piercing Weapons", 1., 0, 0.25, 0, 0, 0, 0.5, 0, 0, 0, 0],
                    ["Slashing Weapons", 1., 0, 0.25, 0, 0, 0, 0.25, 0, 0, 0, 0],
                    ["Unarmed Combat", 1., 0, 0.5, 0, 0, 0, 0.5, 0, 0, 0, 0],
                    ["Brawling", 1., 0, 0.25, 0, 0, 0, 0.5, 0, 0, 0, 0],
                    ["Wrestling", 1., 0, 0.75, 0, 0, 0, 0.5, 0, 0, 0, 0],
                    ["Thrown Weapons", 0.5, 0, 0.75, 0, 0, 0, 0.25, 0, 0, 0, 0],
                    ["Aerodynamics", 0.5, 0, 0.5, 0, 0, 0, 0.5, 0, 0, 0, 0],
                    ["Axes", 0.5, 0, 1., 0, 0, 0, 0.25, 0, 0, 0, 0],
                    ["Balls", 0.25, 0, 0.5, 0, 0, 0, 0.25, 0, 0, 0, 0],
                    ["Ranged Weapons", 0.25, 0, 0.75, 0, 0, 0, 0.25, 0, 0, 0, 0],
                    ["Archery", 0.5, 0, 0.5, 0, 0, 0, 0.5, 0, 0, 0, 0],
                    ["Pistols", 0.125, 0, 0.5, 0, 0, 0, 0.125, 0, 0, 0, 0],
                    ["Automatics", 0, 0, 0.5, 0, 0, 0, 0.25, 0, 0, 0, 0],
                    ["Long Rifle", 0, 0, 0.25, 0, 0, 0, 0.5, 0, 0, 0, 0],
                    ["Indirect Fire", 0, 0, 0.25, 0, 0, 0, 0.25, 0.25, 0, 0, 0],
                    ["Launch Weapons", 0, 0, 0, 0, 0, 0, 0.25, 0.25, 0, 0, 0],
                    ["Spray Weapons", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    ["Physical", 1., 0, 1., 0, 0, 0, 0, 0, 0, 0, 0],
                    ["Acrobatics", 1.5, 0, 0.5, 1, -1, 0, 0, 0, 0, 0, 0],
                    ["Balance", 1.5, 0, 0.5, 0, 0, 0, 0, 0, 0, 0, 0],
                    ["Dodge", 1.5, 0, 0, 0, 0, 0, 0.5, 0, 0, 0, 0],
                    ["Athletics", 0.5, 0, 0.5, 1, -1, 0, 0, 0, 0, 0, 0],
                    ["Climbing", 0, 0.5, 0.5, 1.5, -1.5, 0, 0, 0, 0, 0, 0],
                    ["Jumping", 0.5, 0, 0.5, 0.5, 0, 0, 0, 0, 0, 0, 0],
                    ["Lifting", 0, 0.5, 0.5, 0, 0, 0, 0, 0, 0, 0, 0],
                    ["Running", 0, 1, 0.25, 1, -1, 0, 0, 0, 0, 0, 0],
                    ["Swimming", 0, 1, 0.25, 1, -1, 0, 0, 0, 0, 0, 0],
                    ["Carouse", 0, 1.5, 0, 0, 0.5, 0, 0, 0, 0, 0, 0],
                    ["Perform", 0, 0, 0, 0.25, 0, 1., 0, 0, 0, 0, 0],
                    ["Dancing", 0, 0, 0, 0.5, 0, 0.5, 0, 0, 0, 0, 0],
                    ["Singing", 0, 0, 0, 0.25, 0, 0.75, 0, 0, 0, 0, 0],
                    ["Stealth", 0, 0, 1.25, 0, 0, 0, 0.25, 0, 0, 0, 0],
                    ["Hideing", 0, 0, 0.5, 0, 0, 0, 0.5, 0, 0, 0, 0],
                    ["Shadowing", 0, 0, 0.75, 0, 0, 0, 0.75, 0, 0, 0, 0],
                    ["Sneaking", 0, 0, 1.5, 0, 0, 0, 0, 0, 0, 0, 0],
                    ["Sleight of Hand", 0.5, 0, 0.75, 0, 0, 0, 0, 0, 0, 0, 0],
                    ["Lockpicking", 0.5, 0, 0.75, 0, 0, 0, 0, 0, 0, 0, 0],
                    ["Pickpocketing", 0.5, 0, 0.5, 0, 0, 0, 0.25, 0, 0, 0, 0],
                    ["Quickdrawing", 0.75, 0, 0.25, 0, 0, 0, 0, 0, 0, 0, 0],
                    ["Processing", 0, 0, 0, 0, 0, 0, 1.5, 0, 0, 0, 0],
                    ["Art", 0, 0, 1., 0, 0, 0, 0.5, 0, 0, 0, 0],
                    ["Painting", 0, 0, 1., 0, 0, 0, 0.5, 0, 0, 0, 0],
                    ["Sculpting", 0, 0, 1., 0, 0, 0, 0.5, 0, 0, 0, 0],
                    ["Composure", 0, 0, 0.5, 0, 0, 0, 0., 0, 1.5, 0, 0],
                    ["Mental Composure", 0, 0, 0, 0, 0, 0, 0., 0, 2, 0, 0],
                    ["Physical Composure", 0, 0, 1.0, 0, 0, 0, 0., 0, 1., 0, 0],
                    ["Memory", 0, 0, 0, 0, 0, 0, 0.5, 0.5, 0.5, 0, 0],
                    ["Navigation", 0, 0, 0, 0, 0, 0, 0.5, 0.5, 0, 0, 0],
                    ["Orientation", 0, 0, 0, 0, 0, 0, 1., 0.25, 0, 0, 0],
                    ["Land", 0, 0, 0, 0, 0, 0, 0.5, 0.5, 0, 0, 0],
                    ["Sea", 0, 0, 0, 0, 0, 0, 0.5, 0.5, 0, 0, 0],
                    ["Space", 0, 0, 0, 0, 0, 0, 0.5, 0.5, 0, 0, 0],
                    ["Air", 0, 0, 0, 0, 0, 0, 0.5, 0.5, 0, 0, 0],
                    ["Perception", 0, 0, 0, 0, 0, 0, 1.25, 0, 0, 0, 0],
                    ["Aural", 0, 0, 0, 0, 0, 0, 1.25, 0, 0, 0, 0],
                    ["Olfactorial", 0, 0, 0, 0, 0, 0, 1.25, 0, 0, 0, 0],
                    ["Tactile", 0, 0, 0, 0, 0, 0, 1.25, 0, 0, 0, 0],
                    ["Visual", 0, 0, 0, 0, 0, 0, 1.25, 0, 0, 0, 0],
                    ["Askenning", 0, 0, 0, 0, 0, 0, 0.5, 0, 0, 1., 0],
                    ["Judge Person", 0, 0, 0, 0, 0, 0, .75, 0.25, 0, 0, 0],
                    ["Guess Intentions", 0, 0, 0, 0, 0, 0, .5, 0.5, 0, 0, 0],
                    ["Detect Deceit", 0, 0, 0, 0, 0, 0, .5, 0.5, 0, 0, 0],
                    ["Interrogation", 0, 0, 0, 0, 0, 0, .25, 0.75, 0, 0, 0],
                    ["Empathy", 0, 0, 0, 0, 0, 1.5, 0, 0, 0, 0, 0],
                    ["Act", 0, 0, 0.5, 0, 0, 1., 0, 0, 0, 0, 0],
                    ["Theatrical", 0, 0, 0.25, 0, 0, 1., 0, 0.25, 0, 0, 0],
                    ["Impersonation", 0, 0, 0, 0, 0, 1., 0.5, 0, 0, 0, 0],
                    ["Animal Controll", 0, 0, 0, 0, 0, 1., 0.25, 0, 0, 0, 0],
                    ["Animal Training", 0, 0, 0, 0, 0, 1., 0.5, 0, 0, 0, 0],
                    ["Animal Riding", 0, 0, 0.5, 0, 0, 0.5, 0.5, 0, 0, 0, 0],
                    ["Discussion", 0, 0, 0, 0, 0, 1.5, 0, 0.5, 0, 0, 0],
                    ["Convince", 0, 0, 0, 0, 0, 1.0, 0, 1.0, 0, 0, 0],
                    ["Instruction", 0, 0, 0, 0, 0, 0.5, 0, 1.0, 0, 0, 0],
                    ["Negotiation", 0, 0, 0, 0, 0, 0.5, 0, 0.5, 1.0, 0, 0],
                    ["Interaction", 0, 0, 0, 0, 0, 1.0, 0.25, 0, 0, 0, 0],
                    ["Deception", 0, 0, 0, 0, 0, 1.5, 0.5, 0, 0, 0, 0],
                    ["Intimidation", 0, 0, 0, 0, 0, 1., 0, 0, 0, 1.0, 0],
                    ["Leadership", 0, 0, 0, 0, 0, 1.5, 0.5, 0, 0, 0, 0],
                    ["Persuasion", 0, 0, 0, 0, 0, 1.5, 0.25, 0.25, 0, 0, 0],
                    ["Oratory", 0, 0, 0, 0, 0, 1.5, 0, 0.5, 0, 0, 0],
                    ["Magic", 0, 0, 0, 0, 0, 0, 0, 0, 0, 2., 0],
                    ["Sorcery", 0, 0, 0, 0, 0, 0, 0.25, 0.75, 0, 1., 0],
                    ["Spellcasting", 0, 0, 0, 0, 0, 0, 0.25, 0.75, 0, 1., 0],
                    ["Counterspelling", 0, 0, 0, 0, 0, 0, 0.25, 0.75, 0, 1., 0],
                    ["Ritual Magic", 0, 0, 0, 0, 0, 0, 0., 1., 0, 1., 0],
                    ["Invocation", 0, 0, 0, 0, 0, 1., 0, 0, 0, 1., 0],
                    ["Binding", 0, 0, 0, 0, 0, 0.5, 0, 0, 0.5, 1., 0],
                    ["Banishing", 0, 0, 0, 0, 0, 0.5, 0, 0, 0.5, 1., 0],
                    ["Summoning", 0, 0, 0, 0, 0, 1., 0, 0, 0, 1., 0],
                    ["Alchemy", 0, 0, 0, 0, 0, 0, 0, 1., 0, 0.5, 0],
                    ["Matrix", 0, 0, 0, 0, 0, 0, 0., 1., 0, 0., 0],
                    ["Computers", 0, 0, 0, 0, 0, 0, 0., 1., 0, 0., 0],
                    ["Data Search", 0, 0, 0, 0, 0, 0, 0., 1., 0, 0., 0],
                    ["Programming", 0, 0, 0, 0, 0, 0, 0., 1., 0, 0., 0],
                    ["Computer Use", 0, 0, 0, 0, 0, 0, 0., 1., 0, 0., 0],
                    ["Hacking", 0, 0, 0, 0, 0, 0, 0., 1., 0, 0., 0],
                    ["Cracking", 0, 0, 0, 0, 0, 0, 0., 1., 0, 0., 0],
                    ["Cybercombat", 0, 0, 0, 0, 0, 0, 0., 1., 0, 0., 0],
                    ["Decryption", 0, 0, 0, 0, 0, 0, 0., 1., 0, 0., 0],
                    ["Security", 0, 0, 0, 0, 0, 0, 0., 1., 0, 0., 0],
                    ["Technical", 0, 0, 0, 0, 0, 0, 0., 1., 0, 0., 0],
                    ["Chemistry", 0, 0, 0.35, 0, 0, 0, 0, 1., 0, 0., 0],
                    ["Toxins", 0, 0, 0.25, 0, 0, 0, 0, 1., 0, 0., 0],
                    ["Demolitions", 0, 0, 0.5, 0, 0, 0, 0, 0.75, 0, 0., 0],
                    ["Electronics", 0, 0, 0.5, 0, 0, 0, 0, 0.75, 0, 0., 0],
                    ["Maglocks", 0, 0, 0.5, 0, 0, 0, 0, 0.75, 0, 0., 0],
                    ["Sensors", 0, 0, 0.5, 0, 0, 0, 0, 0.75, 0, 0., 0],
                    ["Optical Computers", 0, 0, 0.5, 0, 0, 0, 0, 0.75, 0, 0., 0],
                    ["Electronic Warfare", 0, 0, 0, 0, 0, 0, 0, 1., 0, 0., 0],
                    ["Mechanics", 0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 0., 0],
                    ["Locks", 0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 0., 0],
                    ["Weapons", 0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 0., 0],
                    ["Traps", 0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 0., 0],
                    ["Medics", 0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 0., 0],
                    ["Cybernetics", 0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 0., 0],
                    ["Extended Care", 0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 0., 0],
                    ["First Aid", 0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 0., 0],
                    ["Social", 0, 0, 0.5, 0, 0, 0, 0.5, 0, 0, 0., 0],
                    ["Disguise", 0, 0, 0.5, 0, 0, 0, 0.5, 0, 0, 0., 0],
                    ["Forgery", 0, 0, 0.5, 0, 0, 0, 0, 0.75, 0, 0., 0],
                    ["Locomotion", 0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 0., 0],
                    ["Vehicle Mechanics", 0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 0., 0],
                    ["Ground Vehicle Mechanics", 0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 0., 0],
                    ["Airborne Vehicle Mechanics", 0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 0., 0],
                    ["Spacecraft Mechanics", 0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 0., 0],
                    ["Watercraft Mechanics", 0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 0., 0],
                    ["Pilot", 0, 0, 0.5, 0, 0, 0, 0.5, 0, 0, 0., 0],
                    ["Airplane", 0, 0, 0.5, 0, 0, 0, 0.5, 0, 0, 0., 0],
                    ["Hovercraft", 0, 0, 0.5, 0, 0, 0, 0.5, 0, 0, 0., 0],
                    ["Helicopter", 0, 0, 0.5, 0, 0, 0, 0.5, 0, 0, 0., 0],
                    ["Submarine", 0, 0, 0.5, 0, 0, 0, 0.5, 0, 0, 0., 0],
                    ["Thrust", 0, 0, 0.5, 0, 0, 0, 0.5, 0, 0, 0., 0],
                    ["Watercraft", 0, 0, 0.5, 0, 0, 0, 0.5, 0, 0, 0., 0],
                    ["Wheeled", 0, 0, 0.5, 0, 0, 0, 0.5, 0, 0, 0., 0],
]

skill_attribmods_nt = namedtuple('skill_attribmod', ['id'] + skill_attribmods[0])
skills_attribmods_dict = OrderedDict(
    [(entry[0], skill_attribmods_nt(*([i] + entry))) for i, entry in enumerate(skill_attribmods[1:])])

actions = [
    ["name", "category", "cost", "reaction"],
    ["Walk", "move", 'No', False],
    ["Run", "move", 'No', False],
    ["Sprint", "move", 'Complex', False],
    ["Jump", "move", 'Simple', False],
    ["Climb", "move", 'Complex', False],
    ["Swim", "move", 'Complex', False],
    ["Crouch Walk", 'move', 'No', False],
    ["Crawl", "move", 'Complex', False],
    ["Jump for Cover", "move", 'Simple',  True],

    ["Crouch", "shift", 'Free', False],
    ["Stand", "shift", 'Simple', False],
    ["Stand Up", "shift", 'Complex', False],
    ["Jump Up", "shift", 'Simple', False],
    ["Drop Down", "shift", 'Free', True],
    ["Get Down", "shift", 'Simple', False],
    ["Turn", "shift", 'Free', False],
    ["Peek", "shift", 'Free', False],
    ["Duck Back", "shift", 'Free', True],
    ["Take Cover", "shift", 'Simple', False],

    ["Interrupt", "meta", 'Free', False],
    ["Postpone", "meta", 'Free', False],
    ["Delay", "meta", 'Complex', False],
    ["Overwatch", "meta", 'Complex', False],

    ["Melee Attack", "melee combat", 'Complex', False],
    ["Parry", "melee combat", 'Free', True],

    ["Single Shot", "ranged combat", 'Simple', False],
    ["Fast Shots", "ranged combat", 'Complex', False],
    ["Burst Shot", "ranged combat", 'Simple', False],
    ["Full Auto Shot", "ranged combat", 'Complex', False],
    ["Brace Weapon", "ranged combat", 'Simple', False],
    ["Throw Weapon", "ranged combat", 'Simple', False],
    ["Evasive Actions", "ranged combat", 'Simple', False],

    ["Target", "ranged combat", 'Free', False],
    ["Sight", "ranged combat", 'Free', False],
    ["Aim", "ranged combat", 'Simple', False],

    ["Evade", "combat", 'Free', False],
    ["Draw Weapon", "combat", 'Simple', False],
    ["Reload", "combat", 'Complex', False],

    ["Observe", "general", 'Complex', False],

    ["Cast", "astral", 'Complex', False],

    ["Sustain", "astral", 'No', False],

    ["Matrix Action", "matrix", 'Complex', False],
]

matrix_attributes = [
    ["name", "description"],
    ["Processor", "Raw processing power"],
    ["System", "System quality"],
    ["Firewall", "Ability to resist illegal action"],
    ["Uplink", "Maximal bandwidth and latency"],
    ["Signal", "Strength of wireless signal"],
]

programmes = [
    ["name", "skill", "attribute"],
    ["Search", "Data Search", "Processor"],
    ["Stealth", "Cracking", "System"],
    ["Scan", "Electronic Warfare", "Signal"],
    ["Analyze", "Computer Use", "System"],
    ["Access", "Computer Use", "System"],
    ["Exploit", "Cracking", "System"],
    ["Crypt", "Computer Use", "System"],
    ["Break", "Decryption", "Processor"],
    ["Edit", "Computer Use", "System"],
    ["Control", "Computer Use", "System"],
    ["Find", "Computer Use", "Uplink"],
    ["Corrupt", "Cybercombat", "Processor"],
]

programmes_nt = namedtuple('programme', ['id'] + programmes[0])
programmes_dict = OrderedDict([(entry[0], programmes_nt(*([i] + entry))) for i, entry in enumerate(programmes[1:])])

matrix_actions = [
    ["name", "programme", "prerequisite"],
    ["Find Node", "Find", "AID"],
    ["Find Wireless Node", "Scan", ""],
    ["Find Process", "Find", "Node Access"],
    ["Find File", "Find", "Node Access"],
    ["Find Stream", "Find", "Node Access"],
    ["Find Wireless Stream", "Scan", ""],
    ["Analyze Node", "Analyze", "Found Node"],
    ["Analyze Process", "Analyze", "Found Process"],
    ["Analyze File", "Analyze", "Found File"],
    ["Analyze Stream", "Analyze", "Found Stream"],
    ["Access Node", "Access", "Found Node"],
    ["Access Process", "Access", "Found Process"],
    ["Access File", "Access", "Found File"],
    ["Access Stream", "Access", "Found Stream"],
    ["Encrypt File", "Crypt", "File Access"],
    ["Decrypt File", "Crypt", "File Access, Key"],
    ["Break File", "Break", "File Access"],
    ["Encrypt Stream", "Crypt", "Stream Access"],
    ["Decrypt Stream", "Crypt", "Stream Access, Key"],
    ["Break Stream", "Break", "Stream Access"],
    ["Edit Account", "Edit", "Node Access"],
    ["Edit Subscription List", "Edit", "Node Access"],
    ["Edit Log", "Edit", "Node Access"],
    ["Edit Process Account", "Edit", "Process Access"],
    ["Edit File", "Edit", "File Access"],
    ["Edit Stream", "Edit", "Stream Access"],
    ["Start Process", "Control", "Node Access"],
    ["Stop Process", "Control", "Node Access"],
    ["Shutdown Node", "Control", "Node Access"],
    ["Change Alarm Status", "Edit", "Node Access"],
    ["Create File", "Control", "Node Access"],
    ["Delete File", "Control", "Found File"],
    ["Control Process", "Control", "Process Access"],
    ["Change Stream Path", "Control", "Relay Node Access"],
    ["Terminate Stream", "Control", "Relay Node Access"],
    ["Slow Node", "Corrupt", "Found Node"],
    ["Crash Node", "Corrupt", "Found Node"],
    ["Slow Process", "Corrupt", "Found Process"],
    ["Crash Process", "Corrupt", "Found Process"],
    ["Corrupt File", "Corrupt", "Found File"],
    ["Corrupt Stream", "Corrupt", "Found Stream"],
    ["Jam Stream", "Scan", "Found Stream in Signal Range"],
    ["Exploit", "Exploit", "None"]
]

matrix_actions_nt = namedtuple('matrix_action', ['id'] + matrix_actions[0])
matrix_actions_dict = OrderedDict(
    [(entry[0], matrix_actions_nt(*([i] + entry))) for i, entry in enumerate(matrix_actions[1:])])

main_bodyparts = ['Head', 'Upper Body', 'Lower Body', 'Left Arm', 'Right Arm', 'Left Leg', 'Right Leg']

bodyparts = [
    ["name", "template", "parent", "level", "weightfrac", "sizefrac", "essencefrac",
     "agilityfrac", "coordinationfrac", "strengthfrac", "constitutionfrac"],
    ["Body", "human", None, 0, 1., 1., 1, 1., 1., 1., 1., ],
    ["Head", "human", "Body", 1, 1 / 11., 1/11., 0.25, 0., 0.1, 0., 0.1, ],
    ["Vertebrae", "human", "Head", 2, 0.2, 0.2, 0.5, 0., 0., 0., 0., ],
    ["Eyes", "human", "Head", 2, 0.05, 0.05, 0.15, 0., 0., 0., 0., ],
    ["Ears", "human", "Head", 2, 0.05, 0.05, 0.1, 0., 1., 0., 0., ],
    ["Olfactory System", "human", "Head", 2, 0.05, 0.05, 0.05, 0., 0., 0., 0., ],
    ["Tongue", "human", "Head", 2, 0.05, 0.05, 0.05, 0., 0., 0., 0., ],
    ["Skull Shell", "human", "Head", 2, 0.6, 0.6, 0.15, 0., 0., 0., 1., ],
    ["Upper Body", "human", "Body", 1, 2 / 11., 2/11., 0.15, 0.15, 0.0, 0.2, 0.3, ],
    ["Lungs", "human", "Upper Body", 2, 0.1, 0.1, 0.1, 0., 0., 0.0, 0.3, ],
    ["Heart", "human", "Upper Body", 2, 0.1, 0.1, 0.2, 0., 0., 0.0, 0.2, ],
    ["* Muscles", "human", "Upper Body", 2, 0.3, 0.3, 0.3, 0.4, 0.2, 0.9, 0.3, ],
    ["* Bones", "human", "Upper Body", 2, 0.5, 0.5, 0.2, 0., 0., 0.1, 0.2, ],
    ["* Nerves", "human", "Upper Body", 2, 0., 0., 0.1, 0.6, 0.8, 0., 0., ],
    ["* Skin", "human", "Upper Body", 2, 0., 0., 0.1, 0., 0., 0., 0., ],
    ["Lower Body", "human", "Body", 1, 2 / 11., 2/11., 0.15, 0.05, 0.0, 0.05, 0.1, ],
    ["Intestines", "human", "Lower Body", 2, 0.4, 0.4, 0.3, 0.0, 0.0, 0.0, 0.3, ],
    ["* Muscles", "human", "Lower Body", 2, 0.3, 0.3, 0.3, 0.4, 0.2, 0.9, 0.2, ],
    ["* Bones", "human", "Lower Body", 2, 0.3, 0.3, 0.2, 0., 0., 0.1, 0.5, ],
    ["* Nerves", "human", "Lower Body", 2, 0., 0, 0.1, 0.6, 0.8, 0., 0., ],
    ["* Skin", "human", "Lower Body", 2, 0., 0., 0.1, 0., 0., 0., 0., ],
    ["Left Arm", "human", "Body", 1, 1 / 11., 1/11., 0.125, 0.2, 0.35, 0.225, 0.1, ],
    ["* Muscles", "human", "Left Arm", 2, 0.6, 0.6, 0.4, 0.4, 0.2, 0.9, 0.5, ],
    ["* Bones", "human", "Left Arm", 2, 0.4, 0.4, 0.2, 0., 0., 0.1, 0.5, ],
    ["* Nerves", "human", "Left Arm", 2, 0., 0., 0.3, 0.6, 0.8, 0., 0., ],
    ["* Skin", "human", "Left Arm", 2, 0., 0., 0.1, 0., 0., 0., 0., ],
    ["Right Arm", "human", "Body", 1, 1 / 11., 1/11., 0.125, 0.2, 0.35, 0.225, 0.1, ],
    ["* Muscles", "human", "Right Arm", 2, 0.6, 0.6, 0.4, 0.4, 0.2, 0.9, 0.5, ],
    ["* Bones", "human", "Right Arm", 2, 0.4, 0.4, 0.2, 0., 0., 0.1, 0.5, ],
    ["* Nerves", "human", "Right Arm", 2, 0., 0., 0.3, 0.6, 0.8, 0., 0., ],
    ["* Skin", "human", "Right Arm", 2, 0., 0., 0.1, 0., 0., 0., 0., ],
    ["Left Leg", "human", "Body", 1, 2 / 11., 2/11., 0.1, 0.2, 0.1, 0.15, 0.15, ],
    ["* Muscles", "human", "Left Leg", 2, 0.6, 0.6, 0.4, 0.4, 0.2, 0.9, 0.5, ],
    ["* Bones", "human", "Left Leg", 2, 0.4, 0.4, 0.2, 0., 0., 0.1, 0.5, ],
    ["* Nerves", "human", "Left Leg", 2, 0., 0., 0.3, 0.6, 0.8, 0., 0., ],
    ["* Skin", "human", "Left Leg", 2, 0., 0., 0.1, 0., 0., 0., 0., ],
    ["Right Leg", "human", "Body", 1, 2 / 11., 2/11., 0.1, 0.2, 0.1, 0.15, 0.15, ],
    ["* Muscles", "human", "Right Leg", 2, 0.6, 0.6, 0.4, 0.4, 0.2, 0.9, 0.5, ],
    ["* Bones", "human", "Right Leg", 2, 0.4, 0.4, 0.2, 0., 0., 0.1, 0.5, ],
    ["* Nerves", "human", "Right Leg", 2, 0., 0., 0.3, 0.6, 0.8, 0., 0., ],
    ["* Skin", "human", "Right Leg", 2, 0., 0., 0.1, 0., 0., 0., 0., ],
]

bodyparts_nt = namedtuple('bodypart', ['id'] + bodyparts[0])
replace_stars(bodyparts)
bodyparts_dict = OrderedDict([(entry[0], bodyparts_nt(*([i] + entry))) for i, entry in enumerate(bodyparts[1:])])


#Legality: AAA: 10, AA: 20, A: 30, B: 40, C: 50, D: 60, E: 70, Z: Any
gameitems = [
    ["name", "clas", "availability", "cost", "weight", "vis_stealth", "scan_stealth", "legality", 'rating'],
    ["Combat Knife", "Close Combat Weapon", 0, 50, 0.25, 40, 20, 20, False],
    ["Sword", "Close Combat Weapon", 10, 200, 0.7, 40, 20, 50, False],
    ["Scimitar", "Close Combat Weapon", 15, 300, 0.6, 40, 20, 50, False],
    ["Rapier", "Close Combat Weapon", 15, 300, 0.5, 40, 20, 30, False],
    ["Hammer", "Close Combat Weapon", 0, 100, 2.5, 40, 20, 25, False],
    ["Spear", "Close Combat Weapon", 20, 300, 1.0, 40, 20, 50, False],
    ["Snap Blades", "Close Combat Weapon", 10, 500, 0.5, 40, 20, 40, False],
    ["Mono Whip", "Close Combat Weapon", 60, 10000, 0.2, 40, 20, 80, False],
    ["Chainsaw", "Close Combat Weapon", 10, 2000, 3.0, 40, 20, 60, False],
    ["Axe", "Close Combat Weapon", 20, 100, 2.0, 40, 20, 40, False],
    ["Baton", "Close Combat Weapon", 0, 50, 0.5, 40, 20, 20, False],
    ["Katana", "Close Combat Weapon", 15, 500, 1.2, 40, 20, 60, False],
    ["Light Pistol", "Ranged Weapon", 0, 200, 0.6, 40, 20, 20, False],
    ["Heavy Pistol", "Ranged Weapon", 5, 500, 2.0, 30, 15, 30, False],
    ["Machine Pistol", "Ranged Weapon", 25 , 600, 1.5, 30, 15, 40, False],
    ["Sub-Machine-Gun", "Ranged Weapon", 15, 800, 3.0, 20, 10, 50, False],
    ["Shotgun", "Ranged Weapon", 5, 600, 4.0, 30, 15, 40, False],
    ["Battle Rifle", "Ranged Weapon", 35, 2000, 4.0, 20, 10, 65, False],
    ["Assault Rifle", "Ranged Weapon", 25, 1000, 3.5, 20, 10, 60, False],
    ["Sniper Rifle", "Ranged Weapon", 50, 10000, 3.5, 20, 10, 70, False],
    ["Light MG", "Ranged Weapon", 40,   5000, 6.5, 20, 10, 70, False],
    ["Medium MG", "Ranged Weapon", 50, 10000, 10.0, 20, 10, 75, False],
    ["Heavy MG", "Ranged Weapon", 60, 25000, 30.0, 20, 10, 80, False],
    ["Assault Cannon", "Ranged Weapon", 60, 15000, 15.0, 20, 10, 80, False],
    ["Bow", "Ranged Weapon", 10, 500, 0.0, 20, 10, 40, False],
    ["Orc Bow", "Ranged Weapon", 20, 1000, 30.0, 20, 10, 45, False],
    ["Troll Bow", "Ranged Weapon", 30, 2000, 30.0, 20, 10, 50, False],
    ["Pistol Crossbow", "Ranged Weapon", 5, 200, 30.0, 20, 10, 40, False],
    ["Light Crossbow", "Ranged Weapon", 7, 500, 30.0, 20, 10, 45, False],
    ["Heavy Crossbow", "Ranged Weapon", 10, 1000, 30.0, 20, 10, 50, False],
    ["Armored Clothing", "Armor", 0, 300, 2.0, 25, 15, 5, False],
    ["Explorer Jumpsuit", "Armor", 0, 400, 4.0, 25, 15, 0, False],
    ["Flak Vest", "Armor", 20, 1000, 3.0, 20, 15, 20, False],
    ["Flak Vest with Plates", "Armor", 30.0, 3000, 6.0, 20, 15, 40, False],
    ["Armor Jacket", "Armor", 10, 1000, 6.0, 20, 10, 30, False],
    ["Lined Coat", "Armor", 5, 500, 4.0, 25, 15, 15, False],
    ["Light Carapace", "Armor", 40, 4000, 8.0, 25, 15, 40, False],
    ["Heavy Carapace", "Armor", 45, 6000, 14.0, 25, 15, 50, False],
    ["Form Fitting Body Armor", "Armor", 20, 5000, 4.0, 25, 15, 10, False],
    ["Radio Shack 0815", "Computer", 1, 100, 0.05, 60, 40, 20, False],
    ["Renraku Hackset", "Computer", 10, 10000, 2.0, 10, 10, 20, False],
    ["Fairlight Excalibur", "Computer", 90, 100, 0.05, 60, 40, 20, False],
    ["Tower", "Computer", 0, 10000, 2.0, 10, 10, 0, False],
    ["Mainframe", "Computer", 10, 100, 0.05, 60, 40, 0, False],
    ["Cluster", "Computer", 20, 10000, 2.0, 10, 10, 0, False],
    ["Optotronics Kit", "", 0, 1000, 3, 0, 0, 0, False],
    ["Vibropicker", "Anti-Security Tools", 30, 500, 0.1, 0, 0, 40, False],
    ["Voice Emulator", "Anti-Security Tools", 40, 600, 0.1, 0, 0, 60, True],
    ["Fingerprint Emulator", "Anti-Security Tools", 40, 500, 0.2, 0, 0, 60, True],
    ["Retina Emulator", "Anti-Security Tools", 50, 800, 0.5, 0, 0, 60, True],
    ["Bio Replicator", "Anti-Security Tools", 50, 1000, 0.5, 0, 0, 70, True],
    ["Microfone Deceiver", "Anti-Security Tools", 30, 200, 0.2, 0, 0, 40, True],
    ["Camera Deceiver", "Anti-Security Tools", 30, 300, 0.3, 0, 0, 50, True],
    ["Camera", "Sensors", 0, 100, 0.2, 0, 0, 0, True],
    ["Microphone", "Sensors", 0, 50, 0.05, 0, 0, 0, True],
    ["Laser Microphone", "Sensors", 30, 100, 0.3, 0, 0, 30, True],
    ["Weapon/Cyberware Detector", "Sensors", 30, 500, 2., 0, 0, 40, True],
    ["Ultrasound", "Sensors", 0, 0, 0, 0, 0, 0, True],
    ["Rangefinder", "Sensors", 0, 0, 0, 0, 0, 0, True],
    ["Chem Sniffer", "Sensors", 0, 0, 0, 0, 0, 0, True],
    ["Flashlight", "Sensors", 0, 0, 0, 0, 0, 0, True],
    ["Respirator", "Survival", 0, 0, 0, 0, 0, 0, True],
    ["Rebreather", "Survival", 0, 0, 0, 0, 0, 0, False],
    ["Climbing Gear", "Survival", 0, 0, 0, 0, 0, 0, False],
    ["Diving Gear", "Survival", 0, 0, 0, 0, 0, 0, False],
    ["Urban Survival Kit", "Survival", 0, 0, 0, 0, 0, 0, False],
    ["Outdoors Survival Kit", "Survival", 0, 0, 0, 0, 0, 0, False],
    ["Micro Winch (10kg)", "Survival", 0, 0, 0, 0, 0, 0, False],
    ["Standard Winch (100kg)", "Survival", 0, 0, 0, 0, 0, 0, False],
    ["Large Winch (250kg)", "Survival", 0, 0, 0, 0, 0, 0, False],
    ["XXL Winch (500kg)", "Survival", 0, 0, 0, 0, 0, 0, False],
    ["Microwire (20m)", "Survival", 0, 0, 0, 0, 0, 0, False],
    ["Stealth Wire (20m)", "Survival", 0, 0, 0, 0, 0, 0, False],
    ["Myomeric Rope (20m)", "Survival", 0, 0, 0, 0, 0, 0, False],
    ["Medkit", "Biotech", 0, 0, 0, 0, 0, 0, True],
    ["Bio Monitor", "Biotech", 0, 0, 0, 0, 0, 0, False],
    ["Chem Patch", "Biotech", 0, 0, 0, 0, 0, 0, True],
]
    
gameitems_nt = namedtuple('gameitem', ['id'] + gameitems[0])
gameitems_dict = OrderedDict([(entry[0], gameitems_nt(*([i] + entry))) for i, entry in enumerate(gameitems[1:])])


# effective strength = strength *1.5 if two handed
# kind          damage              penetration
# slashing      minstr/3 + str/6      minstr/3 + str/6
# impact        minstr/2.5 + str/5    minstr/4 + str/8
# penetration   minstr/3.5 + str/7    minstr/2 + str/4

closecombatweapons = [
    ["item", "skill", "skillmod", "damage", "damagetype", "penetration", "minstr", "hands",  "special"],
    ["Scimitar", "Slashing Weapons", 5., '10.+{Strength}/6.', "impact", '3.33+{Strength}/18.', 30., 1, None],
    ["Axe", "Impact Weapons", 3., '15.28+{Strength}/6.55', "impact", '12.22+{Strength}/8.18', 50., 1, None],
    ["Rapier", "Piercing Weapons", 7., '5.+{Strength}/10.', "impact", '7.5.+{Strength}/6.67.', 25., 1, None],
    ["Baton", "Impact Weapons", 5., '6.94+{Strength}/7.20', "impact", '5..56+{Strength}/9.', 30., 1, None],
    ["Combat Knife", "Piercing Weapons", 0., '3.33+{Strength}/9.', "impact", '5.+{Strength}/6.', 15., 1, None],
    ["Katana", "Slashing Weapons", 7., '13.5+{Strength}/4.44', "impact", '4.5.+{Strength}/13.33', 30., 2, None],
    ["Sword", "Slashing Weapons", 5., '12.21+{Strength}/6.55', "impact", '6.67+{Strength}/12.', 40., 1, None],
    ["Hammer", "Impact Weapons", 0., '15.+{Strength}/6.67', "impact", '16.67+{Strength}/6.', 50., 1, None],
    ["Spear", "Piercing Weapons", 10., '8.+{Strength}/7.5', "impact", '12.+{Strength}/5.', 30., 2, None],
    ["Snap Blades", "Piercing Weapons", 0., '4.44+{Strength}/9.', "impact", '6.67+{Strength}/6.', 20., 1, None],
    ["Mono Whip", "Slashing Weapons", 10., '20.+{Strength}/99999.', "impact", '20.+{Strength}/99999.', 20., 1, None],
    ["Chainsaw", "Slashing Weapons", 0., '18.+{Strength}/5.', "impact", '6.+{Strength}/15.', 45., 1, None],
]

closecombatweapons_nt = namedtuple('rangedweapon', ['id'] + closecombatweapons[0])
closecombatweapons_dict = OrderedDict(
    [(entry[0], closecombatweapons_nt(*([i] + entry))) for i, entry in enumerate(closecombatweapons[1:])])


rangedweapons = [
    ["item", "skill", "skillmod", "damage", "damagetype", "penetration", "range", "shot", "burst", "auto",
     "minstr", "recoil", "mag", "magtype", "top", "under", "barrel", "special", "hands"],
    ["Heavy Pistol", "Pistols", 0., 16., "ballistic", 15., 12., 5, 0, 0, 50, 30, 10, "", 1, 0, 1, None, 1],
    ["Light Pistol", "Pistols", 0., 8., "ballistic", 10., 10., 6, 0, 0, 30, 15, 15, "", 0, 0, 1, None, 1],
    ["Machine Pistol", "Automatics", 0., 8., "ballistic", 10., 10, 6, 12, 18, 40, 15, 20, "", 1, 0, 1, None, 1],
    ["Sub-Machine-Gun", "Automatics", 0., 8., "ballistic", 10., 20, 6, 15, 30, 20, 7, 30, "", 1, 0, 1, None, 2],
    ["Shotgun", "Long Rifle", 0., 18., "ballistic", 20., 20, 5, 0, 0, 40, 15, 6, "", 1, 1, 1, None, 2],
    ["Battle Rifle", "Automatics", 0., 18., "ballistic", 30., 100, 4, 10, 20, 54, 20, 20, "", 1, 1, 1, # g3
     None, 2],
    ["Assault Rifle", "Automatics", 0., 12., "ballistic", 20., 80, 5, 12, 18, 36, 12, 30, "", 1, 1, 1, None, 2], #g36
    ["Sniper Rifle", "Long Rifles", 0., 18., "ballistic", 30., 160, 2, 0, 0, 60, 15, 10, "", 1, 1, 1, None, 2],
    ["Light MG", "Automatics", 0., 12., "ballistic", 20., 120, 2, 20, 40, 60, 10, 100, "", 1, 1, 1, None, 2],
    ["Medium MG", "Automatics", 0., 18., "ballistic", 30., 150, 1, 20, 40, 80, 15, 100, "", 1, 1, 1, None, 2],
    ["Heavy MG", "Automatics", 0., 42., "ballistic", 76., 300, 1, 30, 50, 180, 25, 100, "", 1, 1, 1, None, 2], #browning m2
    ["Assault Cannon", "Long Rifles", 0., 42., "ballistic", 76., 300, 1, 0, 0, 120, 25, 5, "", 1, 1, 1, None, 2], #light fifty

    ["Bow", "Archery", 0., '5+{Strength}/10.', "impact", '5+{Strength}/10.', 30, 1, 1, 1, 30, 0, 0, "", 1, 1, 1, None, 2],
    ["Orc Bow", "Archery", 0., '10+{Strength}/10.', "impact", '10+{Strength}/10.', 50, 1, 1, 1, 60, 0, 0, "", 1, 1, 1, None, 2],
    ["Troll Bow", "Archery", 0., '15+{Strength}/10.', "impact", '15+{Strength}/10.', 60, 1, 1, 1, 90, 0, 0, "", 1, 1, 1, None, 2],
    ["Pistol Crossbow", "Archery", 0., 6., "impact", 6., 10, 1, 1, 1, 26, 0, 0, "", 1, 1, 1, None, 1],
    ["Light Crossbow", "Archery", 0., 10., "impact", 10., 30, 1, 1, 1, 30, 0, 0, "", 1, 1, 1, None, 2],
    ["Heavy Crossbow", "Archery", 0., 16., "impact", 16., 48, 1, 1, 1, 40, 0, 0, "", 1, 1, 1, None, 2],
]

rangedweapons_nt = namedtuple('rangedweapon', ['id'] + rangedweapons[0])
rangedweapons_dict = OrderedDict(
    [(entry[0], rangedweapons_nt(*([i] + entry))) for i, entry in enumerate(rangedweapons[1:])])

armor = [
    ["item", "locations", "protections", "maxagi", "coordmult"],
    ["Armored Clothing",
     ["Upper Body", "Lower Body", "Right Arm", "Left Arm", "Right Leg", "Left Leg"],
     [[20.,0.], [20.,0.], [20.,0.], [20.,0.], [20.,0.], [20.,0.]],
     60, 0.95],
    ["Explorer Jumpsuit",
     ["Upper Body", "Lower Body", "Right Arm", "Left Arm", "Right Leg", "Left Leg"],
     [[10.,30.], [10.,30.], [10.,30.], [10.,0.], [30.,0.], [10.,30.]],
     70, 0.90],
    ["Flak Vest",
     ["Upper Body", "Lower Body"],
     [[50.,20.],[50.,20.]],
     50, 0.9],
    ["Flak Vest",
     ["Upper Body", "Lower Body"],
     [[70.,40.],[70.,40.]],
     40, 0.85],
    ["Form Fitting Body Armor",
     ["Upper Body", "Lower Body", "Right Arm", "Left Arm", "Right Leg", "Left Leg"],
     [[25.,0.], [25.,0.], [25.,0.], [25.,0.], [25.,0.], [25.,0.]],
     50, 0.95],
    ["Lined Coat",
     ["Upper Body", "Lower Body", "Right Arm", "Left Arm", "Right Leg", "Left Leg"],
     [[30.,0.], [30.,0.], [30.,0.], [30.,0.], [20.,0.], [20.,0.]],
    50, 0.9],
    ["Armor Jacket",
     ["Upper Body", "Lower Body", "Right Arm", "Left Arm"],
     [[40., 15.],[30., 10.],[40., 15.],[40., 15.]],
     40, 0.8],
    ["Light Carapace",
     ["Head", "Upper Body", "Lower Body", "Right Arm", "Left Arm", "Right Leg", "Left Leg"],
     [[30., 15.], [50., 30.], [50., 30.], [40., 20.], [40., 20.], [40.,20.], [40.,20.]],
     30, 0.8],
    ["Heavy Carapace",
     ["Head", "Upper Body", "Lower Body", "Right Arm", "Left Arm", "Right Leg", "Left Leg"],
     [[40., 20.], [70., 40.], [70., 40.], [50., 25.], [50., 25.], [50.,25.], [50.,25.]],
     20, 0.75],
]

armor_nt = namedtuple('armor', ['id'] + armor[0])
armor_dict = OrderedDict(
    [(entry[0], armor_nt(*([i] + entry))) for i, entry in enumerate(armor[1:])])

essence_by_ware = {'cyberware': 0.,
                   'bioware': 0.}

ware = [
    ["name", "kind", "essence", "part_weight", "additional_weight", "description", "basecost", "effectcost", "partcost", "parts",
     "effects", "location"],
    ["Left Cyberarm", "cyberware", 0, 0, 0, "Artificial cyberlimb", 0, 1000, 6000, ["Left Arm"], [], ''],
    ["Right Cyberarm", "cyberware", 0, 0, 0, "Artificial cyberlimb", 0, 1000, 6000, ["Right Arm"], [], ''],
    ["Left Cyberleg", "cyberware", 0, 0, 0, "Artificial cyberlimb", 0, 1000, 6000, ["Left Leg"], [], ''],
    ["Right Cyberleg", "cyberware", 0, 0, 0, "Artificial cyberlimb", 0, 1000, 6000, ["Right Leg"], [], ''],
    ["Muscle Augmentation Upper", "bioware", 0, 0, 0, "Biological muscle replacement", 6000, 0, 6000,
     ["Left Arm Muscles", "Right Arm Muscles", "Upper Body Muscles"], [], ''],
    ["Muscle Augmentation Lower", "bioware", 0, 0, 0, "Biological muscle replacement", 6000, 0, 6000,
     ["Left Leg Muscles", "Right Leg Muscles", "Lower Body Muscles"], [], ''],
    ["Muscle Augmentation Total", "bioware", 0, 0, 0, "Biological muscle replacement", 6000, 0, 6000,
     ["Left Leg Muscles", "Right Leg Muscles", "Lower Body Muscles",
      "Left Arm Muscles", "Right Arm Muscles", "Upper Body Muscles"], [], ''],
    ["Muscle Replacement Upper", "cyberware", 0, 0, 0, "Cybernetic muscle replacement", 6000, 0, 6000,
     ["Left Arm Muscles", "Right Arm Muscles", "Upper Body Muscles"], [], ''],
    ["Muscle Replacement Lower", "cyberware", 0, 0, 0, "Cybernetic muscle replacement", 6000, 0, 6000,
     ["Left Leg Muscles", "Right Leg Muscles", "Lower Body Muscles"], [], ''],
    ["Muscle Replacement Total", "cyberware", 0, 0, 0, "Cybernetic muscle replacement", 6000, 0, 6000,
     ["Left Leg Muscles", "Right Leg Muscles", "Lower Body Muscles",
      "Left Arm Muscles", "Right Arm Muscles", "Upper Body Muscles"], [], ''],
    ["Wired Reflexes I", "cyberware", 10, 0, 0, "Cybernetic nerve replacement", 5000, 5000, 6000,
     ["Vertebrae"], [['stats', 'Physical Reaction', '+10'], ['stats', 'Physical Action Multiplyer', '*0.9']], ''],
    ["Wired Reflexes II", "cyberware", 20, 0, 0, "Cybernetic nerve replacement", 5000, 25000, 6000,
     ["Vertebrae", "Upper Body Nerves", "Left Arm Nerves", "Right Arm Nerves"],
     [['stats', 'Physical Reaction', '+20'], ['stats', 'Physical Action Multiplyer', '*0.8']], ''],
    ["Wired Reflexes III", "cyberware", 30, 0, 0, "Cybernetic nerve replacement", 5000, 125000, 6000,
     ["Vertebrae", "Upper Body Nerves", "Left Arm Nerves", "Right Arm Nerves", "Lower Body Nerves", "Left Leg Nerves",
      "Right Leg Nerves"],
     [['stats', 'Physical Reaction', '+30'], ['stats', 'Physical Action Multiplyer', '*0.7']], ''],
    ["Synaptic Accelerator I", "bioware", 10, 0, 0, "Bionetic nerve replacement", 1500, 5000, 6000,
     ["Vertebrae"], [ ['stats', 'Physical Reaction', '+10'], ['stats', 'Physical Action Multiplyer', '*0.9']], ''],
    ["Synaptic Accelerator II", "bioware", 20, 0, 0, "Bionetic nerve replacement",15000, 35000, 6000,
     ["Vertebrae", "Upper Body Nerves", "Left Arm Nerves", "Right Arm Nerves"],
     [['stats', 'Physical Reaction', '+20'], ['stats', 'Physical Action Multiplyer', '*0.8']], ''],
    ["Synaptic Accelerator III", "bioware", 30, 0, 0, "Bionetic nerve replacement", 15000, 245000, 6000,
     ["Vertebrae", "Upper Body Nerves", "Left Arm Nerves", "Right Arm Nerves", "Lower Body Nerves", "Left Leg Nerves",
      "Right Leg Nerves"],
     [['stats', 'Physical Reaction', '+30'], ['stats', 'Physical Action Multiplyer', '*0.7']], ''],
    ["Encephalon I", "cyberware", 5, 5, 0, "Cybernetic Coprocessor", 0, 6000, 0, [],
     [["attributes", "Logic", "+10"]], ''],
    ["Encephalon II", "cyberware", 10, 10, 0, "Cybernetic Coprocessor", 0, 30000, 0, [],
     [["attributes", "Logic", "+20"]], ''],
    ["Encephalon III", "cyberware", 15, 15, 0, "Cybernetic Coprocessor", 0, 150000, 0, [],
     [["attributes", "Logic", "+30"]], ''],
    ["Thalamus Enhancer I", "cyberware", 5, 5, 0, "Cybernetic Coprocessor", 0, 6000, 0, [],
     [["attributes", "Intuition", "+10"]], ''],
    ["Thalamus Enhancer II", "cyberware", 10, 10, 0, "Cybernetic Coprocessor", 0, 30000, 0, [],
     [["attributes", "Intuition", "+20"]], ''],
    ["Thalamus Enhancer III", "cyberware", 15, 15, 0, "Cybernetic Coprocessor", 0, 150000, 0, [],
     [["attributes", "Intuition", "+30"]], ''],
    ["Lymbic Filter I", "cyberware", 5, 5, 0, "Cybernetic Coprocessor", 0, 6000, 0, [],
     [["attributes", "Willpower", "+10"]], ''],
    ["Lymbic Filter II", "cyberware", 10, 10, 0, "Cybernetic Coprocessor", 0, 30000, 0, [],
     [["attributes", "Willpower", "+20"]], ''],
    ["Lymbic Filter III", "cyberware", 15, 15, 0, "Cybernetic Coprocessor", 0, 150000, 0, [],
     [["attributes", "Willpower", "+30"]], ''],
    ["Cerebral Booster I", "bioware", 5, 5, 0, "Cybernetic Coprocessor", 6000, 6000, 0, [],
     [["attributes", "Logic", "+10"]], ''],
    ["Cerebral Booster II", "bioware",10, 10, 0, "Cybernetic Coprocessor", 6000, 48000, 0, [],
     [["attributes", "Logic", "+20"]], ''],
    ["Cerebral Booster III", "bioware", 15, 15, 0, "Cybernetic Coprocessor", 6000, 294000, 0, [],
     [["attributes", "Logic", "+30"]], ''],
    ["Biological Intuition I", "bioware", 5, 5, 0, "Cybernetic Coprocessor", 6000, 6000, 0, [],
     [["attributes", "Intuition", "+10"]], ''],
    ["Biological Intuition II", "bioware", 10, 10, 0, "Cybernetic Coprocessor", 6000, 42000, 0, [],
     [["attributes", "Intuition", "+20"]], ''],
    ["Biological Intuition III", "bioware", 15, 15, 0, "Cybernetic Coprocessor", 6000, 294000, 0, [],
     [["attributes", "Intuition", "+30"]], ''],
    ["Biological Willpower I", "bioware", 5, 5, 0, "Cybernetic Coprocessor", 6000, 6000, 0, [],
     [["attributes", "Willpower", "+10"]], ''],
    ["Biological Willpower II", "bioware", 10, 10, 0, "Cybernetic Coprocessor", 6000, 42000, 0, [],
     [["attributes", "Willpower", "+20"]], ''],
    ["Biological Willpower III", "bioware", 15, 15, 0, "Cybernetic Coprocessor", 6000, 294000, 0, [],
     [["attributes", "Willpower", "+30"]], ''],
]

ware_nt = namedtuple('ware', ['id'] + ware[0])
ware_dict = OrderedDict([(entry[0], ware_nt(*([i]
                                              + entry))) for i, entry in enumerate(ware[1:])])


adept_powers = [
    ["name", "cost", "description", "formdescription", "effects"],
    ["Combat Sense", 'X', 'Enhance Reaction', [['Physical Reaction +', '{Value}*{Magic}/30.']], [['stats', 'Physical Reaction', '+{Value}*{Magic}/30.']]],
    ["Danger Sense", 'X', 'Enhance Reaction for suprise tests (Manual)', [['Physical Reaction in Surprise Tests+', '{Value}*{Magic}/15.']], [['test', 'Surprise', '+{Value}*{Magic}/15.']]],
    ["Astral Sight", '10', 'Allow Adept to perceive astrally', [], [[]]],
    ["Traceless Walk", '5', 'Leave no traces when walking. Does not trigger pressure sensors. (Manual)',[], [[]]],
    ["Wall Running", '10', 'Allow Adept to run on a wall as long as he is sprinting',[], [[]]],
    ["Killing Hands", '5', 'Cause Physical Damage in Combat',[],  [[]]],
    ["Critical Strike", 'X', 'Multiply Unarmed Combat Damage (Manual)', [['Unarmed Combat Damage *', '(1+{Value}*{Magic}/1200.)']], [['stat', 'Unarmed Combat Damage', '*(1+{Value}*{Magic}/1200.)']]],
    ["Spirit Claw", 'X', 'Multiply Unarmed Combat Damage to dual/astral targets (Manual)', [['Unarmed Combat Damage *', '(1+{Value}*{Magic}/600.)']],
     [['stat', 'Unarmed Combat Damage', '*(1+{Value}*{Magic}/600.)']]],
    ["Penetrating Strike", 'X', 'Multiply Unarmed Combat Penetration (Manual)', [['Unarmed Combat Penetration *', '(1+{Value}*{Magic}/120.)']],
     [['stat', 'Unarmed Combat Penetration', '*(1+{Value}*{Magic}/120.)']]],
    ["Elemental Strike", '5', 'Add elemental Effect to Unarmed Combat Damage (Manual)', [], [[]]],
    ["Elemental Aura", 'X', 'Elemental Aura that deals damage on Contact (successfull attack of being successfully attacked in (un)armed combat). (Manual)',
        [['Elemental Aura Damage ', '{Value}*{Magic}/20.'], ['Elemental Aura Penetration ', '{Value}*{Magic}/60.']], [[]]],
    ["Elemental Resistance", 'X', 'Armor against specific elemental effects (Manual)', [['Elemental Armor', '{Value}*{Magic}/10']], [[]]],
    ["Freefall", 'X', 'Gain no damage for falling a given distance (Manual)', [['Free falling Distance in meters ', '{Value}*{Magic}/20']], [[]]],
    ["Improved Jump", 'X', 'Jump further', [['Jumping Distance *', '(1+{Value}*{Magic}/600)']], [['stat', 'Jumping Distance', '*(1+{Value}*{Magic}/600)']]],
    ["Improved Running", 'X', 'Run faster', [['Run Speed *', '(1+{Value}*{Magic}/600)']], [['stat', 'Run Speed', '*(1+{Value}*{Magic}/600)']]],
    ["Improved Swimming", 'X', 'Swim faster', [['Swim Speed *', '(1+{Value}*{Magic}/600)']], [['stat', 'Swim Speed', '*(1+{Value}*{Magic}/600)']]],
    ["Rapid Healing", 'X', 'Increase Heal Time (Manual)', [['Heal Time /', '(1+{Value}*{Magic}/150.)']], [['stat', 'Heal Time', '/(1+{Value}*{Magic}/150.)']]],
    ["Kinesics", '10', 'Change Face. Same Gender and Metatype. Change time 5 min, Perception Test with a Test Difficulty Equal to Magic is needed to find faults. (Manual)',[],  [[]]],
    ["Melain Control", '5', 'Change Hair Color (only natural colors). Change time 1min. Perception Test with a Test Difficulty Equal to Magic is needed to find faults. (Manual)',[],  [[]]],
    ["Voice Control", '5', 'Change Voice. change time 1 min. Perception Test with a Test Difficulty Equal to Magic is needed to find faults. (Manual)',[],  [[]]],
    ["Pain Resistance", 'X', 'Ignore low life penalties', [['Ignore percentage of damage', '{Value}*{Magic}/5.']], [['stat', 'Pain Resistance', '{Value}*{Magic}/500']]],
    ["Spell Resistance", 'X', 'Improve resistance to spells (Manual)', [['Spell Resistance +', '{Value}*{Magic}/30.']], [['stat', 'Spell Resistance', '+{Value}*{Magic}/30.']]],
    ] + [
    ["Enhanced Attribute {}".format(i.name), 'X', 'Enhance {}'.format(i.name),
     [['{} *'.format(i.name), '(1+{Value}*{Magic}/1800.)']],
     [['attributes', '{}'.format(i.name), '*(1+{Value}*{Magic}/1800.)']]]
    for i in attributes_dict.values() if i.kind != 'special'
    ] + [
    ["Improved Skill {}".format(i.name), 'X', 'Improve {}'.format(i.name),
     [['{} *'.format(i.name), '+{Value}*{Magic}/30.']],
     [['skills', '{}'.format(i.name), '+{Value}*{Magic}/30.']]]
    for i in skills_dict.values()
    ]


adept_powers_nt = namedtuple('adept_power', ['id'] + adept_powers[0])
adept_powers_dict = OrderedDict([(entry[0], adept_powers_nt(*([i] + entry))) for i, entry in enumerate(adept_powers[1:])])


computer = [
    ["name", "Processor", "System", "Uplink", "Signal", "Size"],
    ["Radio Shack 0815", 5, 20, 10, 30, 2],
    ["Renraku Hackset", 30, 30, 30, 30, 2],
    ["Fairlight Excalibur", 60, 60, 60, 60, 2],
    ["Tower", 30, 30, 60, 0, 10],
    ["Mainframe", 40, 20, 60, 0, 100],
    ["Cluster", 100, 30, 100, 0, 1000],
]

computer_nt = namedtuple('computer', ['id'] + computer[0])
computer_dict = OrderedDict([(entry[0], computer_nt(*([i] + entry))) for i, entry in enumerate(computer[1:])])

spells = [
    ['name', 'category', 'subcategoy', 'threshold', 'resist', 'drain', 'effect', 'range', 'volume', 'anchor',
     'casttime'],
    ['Mana Bolt',
     'Mana, Mind',
     'destruction',
     '10',
     'Willpower',
     'X',
     'X% Damage',
     '64m',
     '1 Target',
     '-',
     '3'],
    ['Power Bolt',
     'Mana, Body',
     'destruction',
     '0',
     'Body',
     'X',
     'X% Damage',
     '128m',
     '1 Target',
     '-',
     '2'],
    ['Fireball',
     'Physical',
     'destruction',
     '30',
     'Dodge',
     'X+Y',
     'X Damage, Y/5 Penetration, burn, nostage',
     '32m',
     '2m',
     '-',
     '5'],
    ['Firebolt',
     'Physical',
     'destruction',
     '20',
     'Dodge',
     'X+Y',
     'X Damage, Y/2 Penetration',
     '64m',
     '1 Target',
     '-',
     '3'],
]

spells_nt = namedtuple('spell', ['id'] + spells[0])
spells_dict = OrderedDict([(entry[0], spells_nt(*([i] + entry))) for i, entry in enumerate(spells[1:])])


#weight:payloads:
# cars: 1:1
# rotorcraft 1:1
# vector thrust: 2:1
# jets: 3:1
# bike 2:1
vehicles = [
    ["name", "weight", "max_speed", "acceleration", "load", 'size', 'Constitution', 'Armor'],
    ['Lady Bug', 0.0005, 10, 3, '', 0.01, 20, 1],
    ['Hummel', 0.001, 12, 4, '', 0.025, 20, 1],
    ['Libelle', 0.005, 13, 5, '', 0.1, 15, 1],
    ['Roach', 0.01, 1, 1, '', 0.05, 40, 3], #American Roach
    ['Kanmushi', 0.0005, 0.2, 0.2, '', 0.01, 30, 1],
    ['Spider', 0.1, 4, 4, '', 0.2, 30, 1], #Vogelspinne
    ['Flying Football', 5, 25, 4, 5, 0.5, 30, 30],
    ['Ball', 0.5, 10, 3, 0.5, 0.1, 40, 5],
    ['Blimp', 10, 15, 1, 10, 2, 20, 0],
    ['Cat', 4, 10, 5, 1, 0.4, 30, 1],
    ['Wheeled Dog', 20, 25, 2, 20, 0.5, 40, 40],
    ['Steel Lynx', 100, 40, 3, 100, 1, 40, 50],
    ['Vector Thrust Lynx', 100, 60, 4, 50, 1, 30, 40],
    ['Mini Plane', 3, 40, 5, 2, 1, 20, 1],
    ['Jet Drone', 20, 120, 10, 7, 2, 20, 20],
    ['Hover Drone', 2, 30, 2, 2, 0.5, 30, 3],
    ['Google Car', 500, 30, 2, 300, 2.5, 40, 10],
    ['Speed Car', 1500, 85, 5, 300, 4.5, 40, 10],
    ['Ford Americar', 1500, 50, 2, 500, 5, 40, 15], # opel insignia
    ['Pizza Van', 2000, 40, 2, 1500, 5.5, 40, 15], #sprinter kurz
    ['Runner Van', 2500, 30, 1.5, 2500, 7, 40, 15], #sprinter lang
    ['Speedbike', 200, 85, 6, 120, 2, 30, 10], # ducati 1199
    ['Hard Bike', 350, 50, 4,  200, 2.5, 40, 15], # harley davidson breakout
    ['Combat Helicopter', 5000, 80, 6, 3000, 15, 40, 50], # apache
    #['Commuting Helicopter', '', '', '', '', '', ''],
    ['APC', 10000, 30, 1, 5000, 7, 50, 150], # LAV
    ['IFV', 15000, 15, 1, 15000, 7, 50, 200], # Bradley
    ['Tank', 30000, 20, 2, 30000, 9, 50, 500], # Leopard 2a6
    #['', '', '', '', '', '', ''],
]

vehicles_nt = namedtuple('vehicles', ['id'] + vehicles[0])
vehicles_dict = OrderedDict([(entry[0], vehicles_nt(*([i] + entry))) for i, entry in enumerate(vehicles[1:])])