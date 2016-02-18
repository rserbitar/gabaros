# coding: utf8
# versuche so etwas wie
import datetime
import basic
import data
from random import gauss
import rules
from collections import OrderedDict
from math import log

def index():
    redirect(URL('view_chars'))


def roll(char_id, value, name, visible):
    roll = int(rules.die_roll())
    if value is None:
        value = -100
    else:
        value = float(value)
    if name is None:
        name = ''
    name = name.replace('_', ' ')
    result = int(round(value + roll))
    db.rolls.insert(char=char_id, name=name, value=value, roll=roll, result=result, visible=visible)
    return result


def roll_button():
    value = request.args(2)
    char = int(request.args(0))
    name = request.args(1)
    visible = int(request.args(3))
    result = roll(char, value, name, visible)
    if visible:
        response.js = 'jQuery(".flash").html("{}: {}").slideDown();'.format(name, result)
    else:
        response.js = 'jQuery(".flash").html("{} roll was sent!").slideDown();'.format(name)


@auth.requires_login()
def view_items():
    char_id = get_char()
    table = db.char_items
    table2 = db.item_upgrades
    itemdata = db(table.char==char_id).select(table.id, table.item, table.rating, table.location, table.loadout)
    upgrades = db(table2.char==char_id).select(table2.id, table2.item, table2.upgrade)
    upgrades = {row.upgrade.id: (row.item.item, row.item.id) for row in upgrades}
    itemdata2 = [['Item', 'Rating', 'Weight', 'Visible Stealth', 'Scan Stealth', 'Location', 'Loadout']]
    for row in itemdata:
        item = data.gameitems_dict[row.item]
        if row.id not in upgrades:
            itemdata2.append([row.item, row.rating, item.weight, item.vis_stealth, item.scan_stealth, row.location.name if row.location else '', row.loadout])
            if item.clas == 'Ranged Weapon':
                special = data.rangedweapons_dict[item.name].special
                if special and 'upgrades' in special:
                    for upgrade in special['upgrades']:
                        upgrade = data.gameitems_dict[upgrade]
                        itemdata2.append(['{} - {}'.format(row.item, upgrade.name), None, upgrade.weight, upgrade.vis_stealth, upgrade.scan_stealth, None, None])
        else:
            if upgrades[row.id][1] not in upgrades:
                itemdata2.append(['{} - {}'.format(upgrades[row.id][0], row.item), row.rating, item.weight, item.vis_stealth, item.scan_stealth, row.location.name if row.location else '', row.loadout])
            else:
                itemdata2.append(['{} - {} - {}'.format(upgrades[upgrades[row.id][1]][0], upgrades[row.id][0], row.item), row.rating, item.weight, item.vis_stealth, item.scan_stealth, row.location.name if row.location else '', row.loadout])
    table = itemdata2
    return dict(table=table)

@auth.requires_login()
def view_chars():
    table = db.chars
    query = db.chars.player == auth.user.id or db.chars.master == auth.user.id
    table.id.represent = lambda id: A(id, _href=URL("view_char", args=(id)))
    table.player.represent = lambda player: db.auth_user[player].username
    form = crud.select(table, query=query, fields=["id", "name"])
    return dict(form=form)


@auth.requires_login()
def view_char():
    char_id = get_char()
    table = db.chars
    table.player.writable = False
    table.player.represent = lambda player: db.auth_user[player].username
    linklist = [A("attributes", _href=URL('view_attributes')),
                A("skills", _href=URL('view_skills')),
                A("computer", _href=URL('view_computer')),
                A("weapons", _href=URL('view_weapons')),
                A("combat", _href=URL('combat')),
                ]
    return dict(linklist=linklist)


@auth.requires_login()
def view_skills():
    char_id = get_char()
    skills = [["Skill", "Test", "Secret"]]
    skilldepth_dict = {}
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id))
    for skill, skilldata in data.skills_dict.items():
        skillname = skill
        skilldepth = skilldepth_dict.get(skilldata.parent, 0)
        skilldepth_dict[skill] = skilldepth + 1
        val = char_property_getter.get_skilltest_value(skill)
        button1 = A("{:.0f}".format(val),
                    callback=URL('roll_button', args=[char_id, skillname, val, 1]), _class='btn')
        button2 = A("{:.0f}".format(val),
                    callback=URL('roll_button', args=[char_id, skillname, val, 0]), _class='btn')
        if skilldepth == 0:
            skilltext = H3(skillname)
        elif skilldepth == 1:
            skilltext = H4(skillname)
        else:
            skilltext = skillname
        skills += [[skilltext, button1, button2]]
    sidebar = wikify(['Task Resolution', 'Skill'])
    return dict(skills=skills, sidebar=sidebar)

def view_skills_alphabetical():
    char_id = get_char()
    skills = [["Skill", "Test", "Secret"]]
    skilldepth_dict = {}
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id))
    for skill, skilldata in data.skills_dict.items():
        skillname = skill
        skilldepth = skilldepth_dict.get(skilldata.parent, 0)
        skilldepth_dict[skill] = skilldepth + 1
        val = char_property_getter.get_skilltest_value(skill)
        button1 = A("{:.0f}".format(val),
                    callback=URL('roll_button', args=[char_id, skillname, val, 1]), _class='btn')
        button2 = A("{:.0f}".format(val),
                    callback=URL('roll_button', args=[char_id, skillname, val, 0]), _class='btn')
        if skilldepth == 0:
            skilltext = H3(skillname)
        elif skilldepth == 1:
            skilltext = H4(skillname)
        else:
            skilltext = skillname
        skills += [[skillname, skilltext, button1, button2]]
    temp = sorted(skills[1:], key = lambda x: x[0])
    skills = [skills[0]] + [i[1:] for i in temp]
    sidebar = wikify(['Task Resolution', 'Skill'])
    return dict(skills=skills, sidebar=sidebar)


@auth.requires_login()
def view_attributes():
    char_id = get_char()
    attributes = [["Attribute", "Unaugmented", "Augmented", "Temporary", "Value", "Mod", "Test", "Secret"]]
    char = basic.Char(db, char_id)

    char_property_getter = basic.CharPropertyGetter(char, modlevel = 'unaugmented')
    char_property_getter2 = basic.CharPropertyGetter(char, modlevel = 'augmented')
    char_property_getter3 = basic.CharPropertyGetter(char, modlevel = 'temporary')
    char_property_getter4 = basic.CharPropertyGetter(char, modlevel = 'stateful')
    for attribute in data.attributes_dict.keys()+ ['Essence']:
        unaugmented = round(char_property_getter.get_attribute_value(attribute),2)
        augmented = round(char_property_getter2.get_attribute_value(attribute),2)
        temporary = round(char_property_getter3.get_attribute_value(attribute),2)
        value = round(char_property_getter4.get_attribute_value(attribute),2)
        modval = round(char_property_getter4.get_attribute_test_value(attribute),2)
        button1= A("{:.0f}".format(modval),
                    callback=URL('roll_button', args=[char_id, attribute, modval, 1]), _class='btn')
        button2 = A("{:.0f}".format(modval),
                    callback=URL('roll_button', args=[char_id, attribute, modval, 0]), _class='btn')
        attributes += [[attribute, unaugmented, augmented, temporary, value, modval, button1, button2]]
    return dict(attributes=attributes)


@auth.requires_login()
def view_matrix_actions():
    char_id = get_char()
    computer_id = request.args(0)
    computer = basic.Computer(db, computer_id, basic.Char(db, char_id))
    actions = [["Action", "Prerequisite", "Test", "Secret"]]
    for action, item in sorted(data.matrix_actions_dict.items()):
        value = computer.get_action_value(action)
        prerequisite = item.prerequisite
        if value is not None:
            button1 = A("{:.0f}".format(value),
                    callback=URL('roll_button', args=[char_id, action, value, 1]), _class='btn')
            button2 = A("{:.0f}".format(value),
                    callback=URL('roll_button', args=[char_id, action, value, 0]), _class='btn')
        else:
            button1 = ''
            button2 = ''
        actions += [[action, prerequisite, button1, button2]]
    sidebar = wikify(['Matrix Actions'])
    return dict(actions=actions, computer = computer.name, sidebar=sidebar)


@auth.requires_login()
def view_computer():
    char_id = get_char()
    computers = [row.id for row in db(db.char_computers.char == char_id).select(db.char_computers.id)]
    char = basic.Char(db, char_id)
    table = [['Computer', 'Processor', 'System', 'Signal', 'Firewall', 'Uplink', 'Current Uplink', 'Damage']]
    at_least_one_computer = False
    for computer_id in computers:
        at_least_one_computer = True
        row = []
        computer = basic.Computer(db, computer_id, char)
        row.append(A(computer.name, _href=URL('view_matrix_actions', args = [computer_id])))
        row.append(computer.attributes['Processor'])
        row.append(computer.attributes['System'])
        row.append(computer.attributes['Signal'])
        row.append(computer.attributes['Firewall'])
        row.append(computer.attributes['Uplink'])
        row.append(computer.attributes['Current Uplink'])
        row.append(computer.damage)
        table.append(row)
    programmes = [['Programmes','Values']]
    if at_least_one_computer:
        char_programmes = computer.programmes
        for programme in sorted(data.programmes_dict.keys()):
            programmes.append([programme, char_programmes.get(programme)])
    sidebar = wikify(['Matrix Attributes', 'Programs'])
    return dict(computer=table, programmes=programmes, sidebar=sidebar)


def combat():
    char_id = get_char()
    char = basic.Char(db, char_id)
    insert_situation_mod = LOAD('view_char','insert_situation_mod.load',ajax=True, target = 'insert_situation_mod')
    view_weapons = LOAD('view_char','view_weapons.load',ajax=True, target = 'view_weapons')
    view_actions = LOAD('view_char','view_actions.load',ajax=True, target = 'view_actions')
    view_cc_weapons = LOAD('view_char','view_cc_weapons.load',ajax=True, target = 'view_cc_weapons')
    sidebar = wikify(['Actions', 'Combat Resolution', 'Task Modifier'])
    return dict(view_weapons=view_weapons, insert_situation_mod=insert_situation_mod, view_actions=view_actions,
                view_cc_weapons=view_cc_weapons, sidebar=sidebar)

def damage():
    char_id = get_char()
    char = basic.Char(db, char_id)
    view_damage_state = LOAD('view_char','view_damage_state.load',ajax=True, target = 'view_damage_state')
    apply_damage = LOAD('view_char','apply_damage.load',ajax=True, target = 'apply_damage')
    heal_damage = LOAD('view_char','heal_damage.load',ajax=True, target = 'heal_damage')
    sidebar = wikify(['Damage'])
    return dict(view_damage_state=view_damage_state, apply_damage=apply_damage, heal_damage=heal_damage)


def get_net_shoottest_val(char_id, weapon_name):
    char = basic.Char(db, char_id)
    weapon = basic.RangedWeapon(weapon_name, char)
    rows = db((db.state_mods.char==char_id) & (db.state_mods.name.belongs(['situation_mod', 'shoot_distance', 'magnification', 'braced', 'burst']))
    ).select(db.state_mods.name, db.state_mods.value, db.state_mods.type)
    resultdict = {'situation_mod': 0.,
                  'shoot_distance': 10.,
                  'magnification': 1.,
                  'braced': False,
                  'burst': 'None'}
    for row in rows:
        resultdict[row.name] = convert(row.value, row.type)
    roll = gauss(0, 10)
    situation_mod = resultdict['situation_mod']
    net_value = situation_mod - roll
    damage, result = weapon.get_damage(net_value, resultdict['shoot_distance'], resultdict['magnification'], 2., resultdict['braced'], resultdict['burst'])
    result['roll'] = roll
    result['other mods'] = situation_mod
    test_val = (-result['difficulty'] - result['other mods'] - result['minimum strength mod']
                  - result['weapon range mod'] - result['sight range mod'] + result['skill'] - result['wide burst mod'])
    return int(round(test_val))

def get_net_cc_test_val(char_id, weapon_name):
    char = basic.Char(db, char_id)
    weapon = basic.CloseCombatWeapon(weapon_name, char)
    rows = db((db.state_mods.char==char_id) & (db.state_mods.name.belongs(['situation_mod']))
    ).select(db.state_mods.name, db.state_mods.value, db.state_mods.type)
    resultdict = {'situation_mod': 0.}
    for row in rows:
        resultdict[row.name] = convert(row.value, row.type)
    roll = gauss(0, 10)
    situation_mod = resultdict['situation_mod']
    net_value = situation_mod - roll
    damage, result = weapon.get_damage(net_value)
    result['roll'] = roll
    result['other mods'] = situation_mod
    test_val = (result['weapon skill mod'] - result['other mods'] - result['minimum strength mod']
                   + result['skill'])
    return int(round(test_val))


@auth.requires_login()
def view_weapons():
    char_id = get_char()
    char = basic.Char(db, char_id)
    weapons = basic.CharPropertyGetter(char).get_ranged_weapons()
    table = [['Weapon', 'Skill', 'Val', 'Net Val', 'Dam', 'Type', 'Pen', 'Range', 'Bullets', 'Rec', 'Mag', 'Type', 'Hands', 'Shoot', 'Upgrades', 'Special']]
    for weapon in weapons:
        row = []
        row.append(weapon.name)
        row.append(weapon.skill)
        row.append('{:.0f}'.format(weapon.get_net_skill_value()))
        row.append(get_net_shoottest_val(char_id, weapon.name))
        row.append(weapon.damage)
        row.append(weapon.damagetype)
        row.append(weapon.penetration)
        row.append(weapon.range)
        row.append('{}/{}/{}'.format(weapon.shot, weapon.burst, weapon.auto))
        row.append(weapon.recoil)
        row.append(weapon.mag)
        row.append(weapon.magtype)
        row.append(weapon.hands)
        row.append(A('Shoot', callback=URL('shoot_weapon', args=[weapon.name]),
                     target = 'attack_result', _class='btn'))
        row.append(', '.join([i.name for i in weapon.upgrades]))
        row.append([(key, value) for key,value in weapon.special.items() if key != 'upgrades'])
        table.append(row)
    #fields = [Field('val', 'integer', default=0, label = 'Modifications')]
    #form = SQLFORM.factory(*fields, table_name = 'weapons',  buttons=[], _method = '', _action = None)
    #form.element(_name='val')['_onblur']="ajax('/gabaros/view_char/insert_state_mod/{}/shoot', " \
    #                                     "['val'], '')".format(char_id)
    #form.element(_name='val')['_onkeypress']="ajax('/gabaros/view_char/insert_state_mod/{}/shoot', " \
    #                                     "['val'], '')".format(char_id)
    return dict(weapons=table)


def convert(value, type_indicator):
    if type_indicator == 'str':
        result = value
    elif type_indicator == 'float':
        result = float(value)
    elif type_indicator == 'bool':
        if value == 'False':
            result = False
        else:
            result = True
    else:
        result = value
    return result

@auth.requires_login()
def shoot_weapon():
    char_id = get_char()
    weapon_name = request.args(0).replace('_', ' ')
    char = basic.Char(db, char_id)
    weapon = basic.RangedWeapon(weapon_name, char)
    rows = db((db.state_mods.char==char_id) & (db.state_mods.name.belongs(['situation_mod', 'shoot_distance', 'magnification', 'braced', 'burst']))
    ).select(db.state_mods.name, db.state_mods.value, db.state_mods.type)
    resultdict = {'situation_mod': 0.,
                  'shoot_distance': 10.,
                  'magnification': 1.,
                  'braced': False,
                  'burst': 'None'}
    for row in rows:
        resultdict[row.name] = convert(row.value, row.type)
    roll = gauss(0, 10)
    situation_mod = resultdict['situation_mod']
    net_value = situation_mod - roll
    damage, result = weapon.get_damage(net_value, resultdict['shoot_distance'], resultdict['magnification'], 2., resultdict['braced'], resultdict['burst'])
    result['roll'] = roll
    result['other mods'] = situation_mod
    difficulty = -(result['difficulty'] + result['other mods'] + result['minimum strength mod']
                  + result['weapon range mod'] + result['sight range mod'] - result['skill'] + result['wide burst mod'])
    text = """
    <table class='table table-striped table-condensed'>
            <tr>
                <th>Stat</th>
                <th>Value</th>
                <th>Stat</th>
                <th>Value</th>
            </tr>
            <tr>
                <th>Damage</td>
                <td>{damage}</td>
                <th>Weapon Range Mod</td>
                <td>{weapon_range_mod}</td>
            </tr>
            <tr>
                <th>Result</td>
                <td>{result}</td>
                <th>Sight Mod</td>
                <td>{sight_range_mod}</td>
            </tr>
            <tr>
                <th>Roll</td>
                <td>{roll}</td>
                <th>Min Strength mod</td>
                <td>{minimum_strength_mod}</td>
            </tr>
            <tr>
                <th>Skill</td>
                <td>{skill}</td>
                <th>Wide Burst Mod</td>
                <td>{wide_burst_mod}</td>
            </tr>
            <tr>
                <th>Difficulty</td>
                <td>{difficulty}</td>
                <th>Other Mods</td>
                <td>{other_mods}</td>
            </tr>
    </table>
    """
    if damage:
        damage = damage
    else:
        damage = 0.
    text = text.format(damage=[(int(i[0]), i[1]) for i in damage],
                weapon_range_mod = int(round(result['weapon range mod'])),
                sight_range_mod = int(round(result['sight range mod'])),
                minimum_strength_mod = int(round(result['minimum strength mod'])),
                wide_burst_mod = int(round(result['wide burst mod'])),
                other_mods =int(round( result['other mods'])),
                result = int(round(result['result'])),
                roll = int(round(result['roll'])),
                skill = int(round(result['skill'])),
                difficulty = int(round(result['difficulty'])))
    db.rolls.insert(char=char_id, name='shoot', value=difficulty, roll=roll, result=result['result'], visible=True)
    return text


@auth.requires_login()
def view_cc_weapons():
    char_id = get_char()
    char = basic.Char(db, char_id)
    weapons = basic.CharPropertyGetter(char).get_close_combat_weapons()
    table = [['Weapon', 'Skill', 'Val', 'Net Val', 'Dam', 'Type', 'Pen', 'Hands', 'Swing']]
    for weapon in weapons:
        row = []
        row.append(weapon.name)
        row.append(weapon.skill)
        row.append('{:.0f}'.format(weapon.get_net_skill_value()))
        row.append(get_net_cc_test_val(char_id, weapon.name))
        row.append(weapon.damage)
        row.append(weapon.damagetype)
        row.append(weapon.penetration)
        row.append(weapon.hands)
        row.append(A('Swing', callback=URL('swing_weapon', args=[weapon.name]),
                     target = 'attack_result', _class='btn'))
        table.append(row)
    #fields = [Field('val', 'integer', default=0, label = 'Modifications')]
    #form = SQLFORM.factory(*fields, table_name = 'weapons',  buttons=[], _method = '', _action = None)
    #form.element(_name='val')['_onblur']="ajax('/gabaros/view_char/insert_state_mod/shoot', " \
    #                                     "['val'], '')".format(char_id)
    #form.element(_name='val')['_onkeypress']="ajax('/gabaros/view_char/insert_state_mod/shoot', " \
    #                                     "['val'], '')".format(char_id)
    return dict(weapons=table)


@auth.requires_login()
def swing_weapon():
    char_id = get_char()
    weapon_name = request.args(0).replace('_', ' ')
    char = basic.Char(db, char_id)
    weapon = basic.CloseCombatWeapon(weapon_name, char)
    rows = db((db.state_mods.char==char_id) & (db.state_mods.name.belongs(['situation_mod']))
    ).select(db.state_mods.name, db.state_mods.value, db.state_mods.type)
    resultdict = {'situation_mod': 0.}
    for row in rows:
        resultdict[row.name] = convert(row.value, row.type)
    roll = gauss(0, 10)
    situation_mod = resultdict['situation_mod']
    net_value = situation_mod - roll
    damage, result = weapon.get_damage(net_value)
    result['roll'] = roll
    result['other mods'] = situation_mod
    difficulty = -(-result['weapon skill mod'] + result['other mods'] + result['minimum strength mod'] - result['skill'])
    text = """
    <table class='table table-striped table-condensed'>
            <tr>
                <th>Stat</th>
                <th>Value</th>
                <th>Stat</th>
                <th>Value</th>
            </tr>
            <tr>
                <th>Damage</td>
                <td>{damage}</td>
                <th>Min Strength mod</td>
                <td>{minimum_strength_mod}</td>
            </tr>
            <tr>
                <th>Result</td>
                <td>{result}</td>
                <th>Weapon Skill Mod</td>
                <td>{weapon_skill_mod}</td>
            </tr>
            <tr>
                <th>Roll</td>
                <td>{roll}</td>
                <th>Other Mods</td>
                <td>{other_mods}</td>
            </tr>
            <tr>
                <th>Skill</td>
                <td>{skill}</td>
            </tr>
            <tr>
                <th>Difficulty</td>
                <td>{difficulty}</td>
            </tr>
    </table>
    """
    if damage:
        damage = damage
    else:
        damage = 0.
    text = text.format(damage=[(int(i[0]), i[1]) for i in damage],
                weapon_skill_mod = int(round(result['weapon skill mod'])),
                minimum_strength_mod = int(round(result['minimum strength mod'])),
                other_mods =int(round( result['other mods'])),
                result = int(round(result['result'])),
                roll = int(round(result['roll'])),
                skill = int(round(result['skill'])),
                difficulty = int(round(result['difficulty'])))
    db.rolls.insert(char=char_id, name='swing', value=difficulty, roll=roll, result=result['result'], visible=True)
    return text

@auth.requires_login()
def insert_state_mod():
    char_id = get_char()
    name = request.args[0]
    db.state_mods.update_or_insert(((db.state_mods.char==char) &
                                    (db.state_mods.name==name)),
                                    value=request.vars.val, char = char, name = name)


@auth.requires_login()
def insert_situation_mod():
    char_id = get_char()
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    situation_mod_types = {'shoot_distance': 'float',
                           'situation_mod': 'float',
                           'magnification': 'float',
                           'braced': 'bool',
                           'burst': 'str'}
    vars = situation_mod_types.keys()
    query = [((db.state_mods.char==char_id) & (db.state_mods.name==i)) for i in vars]

    for i, var in enumerate(vars):
        if request.vars.get(var):
            db.state_mods.update_or_insert(query[i],
                                            value=request.vars.get(var), char = char_id, name = var, type = situation_mod_types[var])
            response.js =  "jQuery('#view_weapons').get(0).reload()"
    fields = [Field('shoot_distance', 'integer', default=0, label = 'Distance',  requires=IS_NOT_EMPTY())]
    fields.append(Field('situation_mod', 'integer', default=0, label = 'Situation Mod',  requires=IS_NOT_EMPTY()))
    fields.append(Field('magnification', 'integer', default=1, label = 'Magnification',  requires=IS_IN_SET([1, 2, 4, 8])))
    fields.append(Field('braced', 'boolean', default=False, label = 'Braced'))
    fields.append(Field('burst', 'string', default='None', label = 'Burst',  requires=IS_IN_SET(['None','Narrow Shot','Wide Shot','Narrow Burst','Wide Burst','Narrow Auto','Wide Auto'])))
    form = SQLFORM.factory(*fields)
    for var in vars:
        form.element(_name=var)['_onblur']="ajax('/gabaros/view_char/insert_situation_mod', " \
                                            "['{}'], '')".format(var)
    if form.process().accepted:
        for i, var in enumerate(vars):
            if form.vars.get(var) is not None:
                db.state_mods.update_or_insert(query[i],
                                            value=form.vars.get(var), char = char_id, name = var, type = situation_mod_types[var])
                response.js =  "jQuery('#view_weapons').get(0).reload()"
    for i,var in enumerate(vars):
        valpair = db(query[i]).select(db.state_mods.value, db.state_mods.type).first()
        if valpair:
            val = convert(valpair.value, valpair.type)
            form.element(_name=var).update(_value=val)
    return dict(form = form)


@auth.requires_login()
def view_actions():
    char_id = get_char()
    char_property_getter = basic.CharPhysicalPropertyGetter(basic.Char(db, char_id))
    combat = db(db.actions.char==char_id).select(db.actions.combat).last()
    if combat:
        combat = combat.combat
    if session.combat:
        combat = session.combat
    else:
        combat = 1
    fields = [Field('combat', type = 'reference combats', requires = IS_IN_DB(db,db.combats.id,'%(name)s'), default = combat)]
    form = SQLFORM.factory(*fields)
    if form.process().accepted:
        combat = int(form.vars.combat)
        session.combat = combat
    combat_name = None
    rows = db(db.combats.id == combat).select(db.combats.name).first()
    if rows:
        combat_name = rows.name
    reaction = int(round(char_property_getter.get_reaction()))
    actions = ['Free', 'Simple', 'Complex']
    action_costs = {i: int(round(char_property_getter.get_actioncost(i))) for i in actions}
    action_buttons = {i: A(i, callback=URL('perform_action', args=[i, combat]),
                     target = 'next_action', _class='btn') for i in actions}
    reaction_button = A("Reaction ({})".format(reaction),
                    callback=URL('roll_button', args=[char_id, 'Reaction', reaction, 1]), _class='btn', _title = 'test')
    action_history = get_action_history(char_id, combat)
    return dict(reaction_button=reaction_button, actions=actions, action_costs=action_costs, action_buttons=action_buttons, action_history = action_history, form=form, combat_name = combat_name)


def get_action_history(char_id, combat):
    data = db((db.actions.char==char_id) & (db.actions.combat==combat)).select(db.actions.action, db.actions.cost)
    action_history = [['Action    ', 'Cost    ', 'Phase    ']]
    phase = 0
    for row in data:
        action_history.append([row.action, int(round(row.cost)), int(round(phase))])
        phase += int(round(row.cost))
    return CAT(H3('Next Action: ', B('{}'.format(int(round(phase))))), P(), TABLE(*([TR(*[TH(i) for i in rows]) for rows in action_history[:1]]+[TR(*rows) for rows in reversed(action_history[1:])]),_class = 'table table-striped table-condensed'))


@auth.requires_login()
def perform_action():
    char_id = get_char()
    action = request.args(0)
    combat = request.args(1)
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id))
    action_cost = char_property_getter.get_actioncost(action)
    db.actions.insert(char=int(char_id), combat=combat, action=action, cost=action_cost)
    action_history = get_action_history(char_id, combat)
    return action_history


@auth.requires_login()
def view_bodyparts():
    char_id = get_char()
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id))
    table = char_property_getter.get_bodypart_table()
    return dict(table=table)


@auth.requires_login()
def view_stats():
    char_id = get_char()
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id), modlevel='stateful')
    char_physical_property_getter = basic.CharPhysicalPropertyGetter(basic.Char(db, char_id), modlevel='stateful')
    stats = OrderedDict()
    stats['Maximum Life'] = int(round(char_property_getter.get_maxlife()))
    stats['Action Multiplier'] = round(char_physical_property_getter.get_actionmult(),2)
    stats['Physical Reaction'] = int(round(char_physical_property_getter.get_reaction()))
    stats['Standing Jump Distance']  = round(char_physical_property_getter.get_jump_distance(False),2)
    stats['Running Jump Distance']  = round(char_physical_property_getter.get_jump_distance(True),2)
    stats['Standing Jump Height']  = round(char_physical_property_getter.get_jump_height(False),2)
    stats['Running Jump Height']  = round(char_physical_property_getter.get_jump_height(True),2)
    speed = [round(i,2) for i in char_physical_property_getter.get_speed()]
    stats['Walk Speed'] = speed[0]
    stats['Run Speed'] = speed[1]
    stats['Sprint Speed'] = speed[2]
    stats['Psychological Threshold'] = round(char_property_getter.get_psycho_thresh(),2)
    drain_resist = round(char_property_getter.get_drain_resist(),2)
    drain_percent = round(rules.resist_damage(100., drain_resist, 0),2)
    stats['Sponataneous Modification Maximum'] = round(char_property_getter.get_spomod_max(),2)
    stats['Drain Resistance'] = "{} / {}%".format(drain_resist, drain_percent)
    for part in ['Body', 'Head', 'Upper Torso', 'Lower Torso', 'Right Arm', 'Left Arm', 'Right Leg', 'Left Leg']:
        stats['Wound Limit {}'.format(part)] = round(char_physical_property_getter.char_body.bodyparts[part].get_woundlimit(),2)
    return dict(stats=stats)


@auth.requires_login()
def view_armor():
    char_id = get_char()
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id), modlevel='stateful')
    armors = char_property_getter.get_armor()
    armor_table = [['Bodypart'] + [armor.name for armor in armors] + ['Total']]
    bodyparts = data.main_bodyparts
    damage_types = ['ballistic','impact']
    for bodypart in bodyparts:
        template = [bodypart]
        for armor in armors:
            template.append('{}/{}'.format(int(round(armor.get_protection(bodypart, damage_types[0]))),
                                           int(round(armor.get_protection(bodypart, damage_types[1])))))
        template.append('{}/{}'.format(int(round(char_property_getter.get_protection(bodypart, damage_types[0]))),
                                       int(round(char_property_getter.get_protection(bodypart, damage_types[1])))))
        armor_table.append(template)
    return dict(armor_table=armor_table)


@auth.requires_login()
def view_damage_state():
    char_id = get_char()
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id), modlevel='stateful')
    wounds = char_property_getter.char.wounds
    damage = char_property_getter.char.damage
    maxlife = char_property_getter.get_maxlife()
    damage_attribute_mod = char_property_getter.get_damagemod('relative')
    damage_skill_mod = char_property_getter.get_damagemod('absolute')
    return dict(wounds=wounds, damage=damage, maxlife=maxlife, damage_attribute_mod = damage_attribute_mod, damage_skill_mod=damage_skill_mod)


@auth.requires_login()
def apply_damage():
    char_id = get_char()
    fields = [Field('kind', 'string', requires=IS_IN_SET(data.damagekinds_dict.keys()), default = 'physical',
                    label = 'Damage Kind'),
              Field('damage', 'integer', default=0, label = 'Damage'),
              Field('penetration', 'integer', default=0, label = 'Penetration'),
              Field('bodypart', 'string', requires=IS_IN_SET(['Body'] + data.main_bodyparts), default = 'Body'),
              Field('typ', 'string', requires=IS_IN_SET(['ballistic','impact', 'none']), default = 'ballistic'),
              Field('percent', 'boolean', default = False),
              Field('resist', 'str', requires=IS_IN_SET(['', 'Willpower', 'Body']), default = ''),
              Field('wounding', 'boolean', default = True)]
    form = SQLFORM.factory(*fields, table_name = 'damage_apply')
    if form.process().accepted:
        char = basic.Char(db, char_id)
        char_property_putter = basic.CharPropertyPutter(char)
        if form.vars.resist or form.vars.kind in ['drain stun', 'drain physical']:
            die_roll = roll(char_id, 0, 'Resist', True)
            resist = form.vars.resist
            resist_roll = die_roll
        else:
            resist = form.vars.resist
            resist_roll = None
        damage_text = char_property_putter.put_damage(form.vars.damage,
                                                      form.vars.penetration,
                                                      form.vars.bodypart,
                                                      form.vars.kind,
                                                      form.vars.typ,
                                                      form.vars.percent,
                                                      resist,
                                                      resist_roll,
                                                      form.vars.wounding
                                                      )
        response.flash = damage_text
        response.js = "jQuery('#view_damage_state').get(0).reload()"
    elif form.errors:
       response.flash = 'form has errors'
    return dict(form=form)


@auth.requires_login()
def heal_damage():
    char_id = get_char()
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id), modlevel='stateful')
    wounds = char_property_getter.char.wounds
    wounds = ['{},{}'.format(location, kind) for location, values in wounds.items() for kind in values]
    damage = char_property_getter.char.damage
    damage = damage.keys()
    fields = [Field('heal_time', 'string',
                    label = 'Healing Time'),
              Field('med_test', 'integer', default=0, label = 'Medical Care Test'),]
    form = SQLFORM.factory(*fields, table_name = 'rest')
    fields2 = [Field('damage_healed', 'float', default = 0, label = 'Damage Healed'),
              Field('damage_kind', 'string', requires=IS_IN_SET(damage), label = 'Damage Kind'),]
    form2 = SQLFORM.factory(*fields2, table_name = 'heal_damage')
    fields3 = [Field('wounds_healed', 'integer', requires=IS_IN_SET([1,2,3,4,5]), default = 1, label = 'Wounds Healed'),
              Field('location', 'string', requires=IS_IN_SET(wounds), label = 'Location and Damage Kind')]
    form3 = SQLFORM.factory(*fields3, table_name = 'heal_wounds')
    fields4 = [Field('first_aid_test', 'float',label = 'First Aid Test')]
    form4 = SQLFORM.factory(*fields4, table_name = 'first_aid')
    if form.process(formname='form_one').accepted:
        char = basic.Char(db, char_id)
        char_property_putter = basic.CharPropertyPutter(char)
        die_roll = roll(char_id, 0, 'Rest', True)
        text = char_property_putter.rest(form.vars.heal_time,
                                                      form.vars.med_test,
                                                      die_roll
                                                      )
        response.flash = text
        response.js = "jQuery('#view_damage_state').get(0).reload()"
    elif form.errors:
       response.flash = 'form has errors'


    if form2.process(formname='form_two').accepted:
        char = basic.Char(db, char_id)
        char_property_putter = basic.CharPropertyPutter(char)
        text = char_property_putter.heal_damage(form2.vars.damage_healed,
                                                      form2.vars.damage_kind
                                                      )
        response.flash = text
        response.js = "jQuery('#view_damage_state').get(0).reload()"
    elif form.errors:
       response.flash = 'form has errors'


    if form3.process(formname='form_three').accepted:
        char = basic.Char(db, char_id)
        char_property_putter = basic.CharPropertyPutter(char)
        text = char_property_putter.heal_wounds(int(form3.vars.wounds_healed),
                                                      form3.vars.location
                                                      )
        response.flash = text
        response.js = "jQuery('#view_damage_state').get(0).reload()"
    elif form.errors:
       response.flash = 'form has errors'

    if form4.process(formname='form_four').accepted:
        char = basic.Char(db, char_id)
        char_property_putter = basic.CharPropertyPutter(char)
        text = char_property_putter.first_aid(form4.vars.first_aid
                                                      )
        response.flash = text
        response.js = "jQuery('#view_damage_state').get(0).reload()"
    elif form.errors:
       response.flash = 'form has errors'
    return dict(form=form, form2 = form2, form3=form3, form4=form4)


@auth.requires_login()
def chat():
    char_id = get_char()
    player = db.chars[char_id].name
    form=LOAD('view_char', 'ajax_form', args=char_id, ajax=True)
    script=SCRIPT("""
        var text = ''
        jQuery(document).ready(function(){
        var callback = function(e){alert(e.data);
            text = e.data + '<br>' + text;
            document.getElementById('text').innerHTML = text;};
          if(!$.web2py.web2py_websocket('ws://127.0.0.1:8888/realtime/""" + str(player) + """', callback))
            alert("html5 websocket not supported by your browser, try Google Chrome");
        });""")
    return dict(form=form, script=script)


@auth.requires_login()
def ajax_form():
    char_id = get_char()
    master = db.chars[char_id].master
    charname = db.chars[char_id].name
    now = datetime.datetime.now().time()
    form=SQLFORM.factory(Field('message'))
    if form.accepts(request,session):
        from gluon.contrib.websocket_messaging import websocket_send
        message = '{}:{} <b>{}</b>: {}'.format(now.hour, now.minute, charname, form.vars.message)
        websocket_send('http://127.0.0.1:8888', message, 'mykey', master)
    return form


@auth.requires_login()
def view_xp():
    char_id = get_char()
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id), modlevel='unaugmented')
    xp = char_property_getter.get_total_exp()
    totalxp = sum(xp.values())
    return dict(totalxp=totalxp, xp=xp)


@auth.requires_login()
def view_cost():
    char_id = get_char()
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id), modlevel='stateful')
    cost = char_property_getter.get_total_cost()
    totalcost = sum(cost.values())
    return dict(totalcost=totalcost, cost=cost)
