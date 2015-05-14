# coding: utf8
# versuche so etwas wie
import basic
import data
from random import gauss


def index():
    redirect(URL('view_chars'))

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
    char = request.args(0)
    if not db.chars[char] or (db.chars[char].player != auth.user.id
                              and db.chars[char].master != auth.user.id):
        redirect(URL(f='index'))
    table = db.chars
    table.player.writable = False
    table.player.represent = lambda player: db.auth_user[player].username
    linklist = [A("attributes", _href=URL('view_attributes', args=[char])),
                A("skills", _href=URL('view_skills', args=[char])),
                A("computer", _href=URL('view_computer', args=[char])),
                A("weapons", _href=URL('view_weapons', args=[char])),
                A("combat", _href=URL('combat', args=[char])),
                ]
    return dict(linklist=linklist)


def roll_button():
    value = request.args(2)
    char = int(request.args(0))
    name = request.args(1)
    visible = int(request.args(3))
    roll = int(round(gauss(0, 10)))
    if value is None:
        value = -100
    else:
        value = float(value)
    if name is None:
        name = ''
    name = name.replace('_', ' ')
    result = int(round(value + roll))
    db.rolls.insert(char=char, name=name, value=value, roll=roll, result=result, visible=visible)
    if visible:
        response.js = 'jQuery(".flash").html("{}: {}").slideDown();'.format(name, result)
    else:
        response.js = 'jQuery(".flash").html("{} roll was sent!").slideDown();'.format(name)


@auth.requires_login()
def view_skills():
    char_id = request.args(0)
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
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
        skills += [["* " * skilldepth + skillname, button1, button2]]
    return dict(skills=skills)


@auth.requires_login()
def view_attributes():
    char_id = request.args(0)
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    attributes = [["Attribute", "Unaugmented", "Augmented", "Temporary", "Value", "Mod", "Test", "Secret"]]
    char = basic.Char(db, char_id)

    char_property_getter = basic.CharPropertyGetter(char, modlevel = 'unaugmented')
    char_property_getter2 = basic.CharPropertyGetter(char, modlevel = 'augmented')
    char_property_getter3 = basic.CharPropertyGetter(char, modlevel = 'temporary')
    char_property_getter4 = basic.CharPropertyGetter(char, modlevel = 'stateful')
    for attribute in data.attributes_dict.keys():
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
    char_id = request.args(0)
    computer_id = request.args(1)
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
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
    return dict(actions=actions)


@auth.requires_login()
def view_computer():
    char_id = request.args(0)
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    computers = [row.id for row in db(db.char_computers.char == char_id).select(db.char_computers.id)]
    char = basic.Char(db, char_id)
    table = [['Computer', 'Processor', 'Signal', 'Firewall', 'Uplink', 'Current Uplink', 'Damage']]
    at_least_one_computer = False
    for computer_id in computers:
        at_least_one_computer = True
        row = []
        computer = basic.Computer(db, computer_id, char)
        row.append(A(computer.name, _href=URL('view_matrix_actions', args = [char_id, computer_id])))
        row.append(computer.attributes['Processor'])
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
    return dict(computer=table, programmes=programmes)


@auth.requires_login()
def view_weapons():
    char_id = request.args(0)
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    char = basic.Char(db, char_id)
    weapons = basic.CharPropertyGetter(char).get_weapons()
    table = [['Weapon', 'Skill', 'Val', 'Net Val', 'Dam', 'Type', 'Pen', 'Range', 'Bullets', 'Rec', 'Mag', 'Type', 'Shoot']]
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
        row.append(A('Shoot', callback=URL('shoot_weapon', args=[char_id, weapon.name]),
                     target = 'shoot_result', _class='btn'))
        table.append(row)
    #fields = [Field('val', 'integer', default=0, label = 'Modifications')]
    #form = SQLFORM.factory(*fields, table_name = 'weapons',  buttons=[], _method = '', _action = None)
    #form.element(_name='val')['_onblur']="ajax('/gabaros/view_char/insert_state_mod/{}/shoot', " \
    #                                     "['val'], '')".format(char_id)
    #form.element(_name='val')['_onkeypress']="ajax('/gabaros/view_char/insert_state_mod/{}/shoot', " \
    #                                     "['val'], '')".format(char_id)
    return dict(weapons=table)


def combat():
    char_id = request.args(0)
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    char = basic.Char(db, char_id)
    insert_shoot_mod = LOAD('view_char','insert_shoot_mod.load',ajax=True, args = [char_id], target = 'insert_shoot_mod')
    view_weapons = LOAD('view_char','view_weapons.load',ajax=True, args = [char_id], target = 'view_weapons')
    view_actions = LOAD('view_char','view_actions.load',ajax=True, args = [char_id], target = 'view_actions')
    return dict(view_weapons=view_weapons, insert_shoot_mod=insert_shoot_mod, view_actions=view_actions)


def get_net_shoottest_val(char_id, weapon_name):
    char = basic.Char(db, char_id)
    weapon = basic.Weapon(weapon_name, char)
    rows = db((db.state_mods.char==char_id) & (db.state_mods.name.belongs(['shoot_mod', 'shoot_distance']))
    ).select(db.state_mods.name, db.state_mods.value)
    resultdict = {'shoot_mod': 0.,
                  'shoot_distance': 10.}
    for row in rows:
        resultdict[row.name] = row.value
    roll = gauss(0, 10)
    shoot_mod = resultdict['shoot_mod']
    net_value = shoot_mod - roll
    damage, result = weapon.get_damage(net_value, resultdict['shoot_distance'])
    result['roll'] = roll
    result['other mods'] = shoot_mod
    test_val = (-result['difficulty'] - result['other mods'] - result['minimum strength mod']
                  - result['weapon range mod'] - result['sight range mod'] + result['skill'])
    return int(round(test_val))


@auth.requires_login()
def shoot_weapon():
    char_id = request.args(0)
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    weapon_name = request.args(1).replace('_', ' ')
    char = basic.Char(db, char_id)
    weapon = basic.Weapon(weapon_name, char)
    rows = db((db.state_mods.char==char_id) & (db.state_mods.name.belongs(['shoot_mod', 'shoot_distance']))
    ).select(db.state_mods.name, db.state_mods.value)
    resultdict = {'shoot_mod': 0.,
                  'shoot_distance': 10.}
    for row in rows:
        resultdict[row.name] = row.value
    roll = gauss(0, 10)
    shoot_mod = resultdict['shoot_mod']
    net_value = shoot_mod - roll
    damage, result = weapon.get_damage(net_value, resultdict['shoot_distance'])
    result['roll'] = roll
    result['other mods'] = shoot_mod
    difficulty = -(result['difficulty'] + result['other mods'] + result['minimum strength mod']
                  + result['weapon range mod'] + result['sight range mod'] - result['skill'])   
    text = ('damage: {}, {}'.format(damage, result))
    db.rolls.insert(char=char_id, name='shoot', value=difficulty, roll=roll, result=result['result'], visible=True)
    return text


@auth.requires_login()
def insert_state_mod():
    char = int(request.args[0])
    name = request.args[1]
    db.state_mods.update_or_insert(((db.state_mods.char==char) &
                                    (db.state_mods.name==name)),
                                    value=request.vars.val, char = char, name = name)


@auth.requires_login()
def insert_shoot_mod():
    char_id = request.args(0)
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    vars = ['shoot_mod','shoot_distance']
    query = [((db.state_mods.char==char_id) & (db.state_mods.name==i)) for i in vars]

    for i, var in enumerate(vars):
        if request.vars.get(var):
            db.state_mods.update_or_insert(query[i],
                                            value=request.vars.get(var), char = char_id, name = var)
            response.js =  "jQuery('#view_weapons').get(0).reload()"
    fields = [Field('shoot_distance', 'integer', default=0, label = 'Distance',  requires=IS_NOT_EMPTY())]
    fields.append(Field('shoot_mod', 'integer', default=0, label = 'Modifications',  requires=IS_NOT_EMPTY()))
    form = SQLFORM.factory(*fields)
    for var in vars:
        form.element(_name=var)['_onblur']="ajax('/gabaros/view_char/insert_shoot_mod/{}', " \
                                            "['{}'], '')".format(char_id, var)
    if form.process().accepts:
        for i, var in enumerate(vars):
            if form.vars.get(var) is not None:
                db.state_mods.update_or_insert(query[i],
                                            value=form.vars.get(var), char = char_id, name = var)
                response.js =  "jQuery('#view_weapons').get(0).reload()"
    for i,var in enumerate(vars):
        val = db(query[i]).select(db.state_mods.value).first()
        if val:
            val = int(val.value)
            form.element(_name=var).update(_value=val)
    return dict(form = form)


@auth.requires_login()
def view_actions():
    char_id = request.args(0)
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    char_property_getter = basic.CharPhysicalPropertyGetter(basic.Char(db, char_id))
    reaction = int(round(char_property_getter.get_reaction()))
    actions = ['Free', 'Simple', 'Complex']
    action_costs = {i: int(round(char_property_getter.get_actioncost(i))) for i in actions}
    action_buttons = {i: A(i, callback=URL('perform_action', args=[char_id, i]),
                     target = 'next_action', _class='btn') for i in actions}
    reaction_button = A("Reaction ({})".format(reaction),
                    callback=URL('roll_button', args=[char_id, 'Reaction', reaction, 1]), _class='btn', _title = 'test')
    action_history = get_action_history(char_id)
    return dict(reaction_button=reaction_button, actions=actions, action_costs=action_costs, action_buttons=action_buttons, action_history = action_history)


def get_action_history(char_id):
    data = db((db.actions.char==char_id) & (db.actions.combat==1)).select(db.actions.action, db.actions.cost)
    action_history = [['Action    ', 'Cost    ', 'Phase    ']]
    phase = 0
    for row in data:
        action_history.append([row.action, int(round(row.cost)), int(round(phase))])
        phase += int(round(row.cost))
    return CAT('Next Action: ', B('{}'.format(int(round(phase)))), P(), TABLE(*([TR(*[TH(i, _style="width:80px") for i in rows]) for rows in action_history[:1]]+[TR(*rows) for rows in reversed(action_history[1:])])))


@auth.requires_login()
def perform_action():
    char_id = request.args(0)
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    action = request.args(1)
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id))
    action_cost = char_property_getter.get_actioncost(action)
    db.actions.insert(char=char_id, combat=1, action=action, cost=action_cost)
    action_history = get_action_history(char_id)
    return action_history


@auth.requires_login()
def view_bodyparts():
    char_id = request.args(0)
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id))
    table = char_property_getter.get_bodypart_table()
    return dict(table=table)


@auth.requires_login()
def view_stats():
    char_id = request.args(0)
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id), modlevel='stateful')
    char_physical_property_getter = basic.CharPhysicalPropertyGetter(basic.Char(db, char_id), modlevel='stateful')
    maxlife = int(round(char_property_getter.get_maxlife()))
    action_mult = round(char_physical_property_getter.get_actionmult(),2)
    reaction = int(round(char_physical_property_getter.get_reaction()))
    jump_dist_stand = round(char_physical_property_getter.get_jump_distance(False),2)
    jump_dist_run = round(char_physical_property_getter.get_jump_distance(True),2)
    jump_height_stand = round(char_physical_property_getter.get_jump_height(False),2)
    jump_height_run = round(char_physical_property_getter.get_jump_height(True),2)
    speed = [round(i,2) for i in char_physical_property_getter.get_speed()]

    return dict(maxlife=maxlife,
                action_mult=action_mult,
                reaction=reaction,
                jump_dist_stand=jump_dist_stand,
                jump_dist_run=jump_dist_run,
                jump_height_stand=jump_height_stand,
                jump_height_run=jump_height_run,
                speed=speed)


@auth.requires_login()
def view_armor():
    char_id = request.args(0)
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
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
    char_id = request.args(0)
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id), modlevel='stateful')
    wounds = char_property_getter.char.wounds
    damage = char_property_getter.char.damage
    maxlife = char_property_getter.get_maxlife()
    return dict(wounds=wounds, damage=damage, maxlife=maxlife)


@auth.requires_login()
def apply_damage():
    char_id = request.args(0)
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    fields = [Field('damage', 'integer', default=0, label = 'Damage'),
              Field('penetration', 'integer', default=0, label = 'Penetration'),
              Field('bodypart', 'string', requires=IS_IN_SET(['Body'] + data.main_bodyparts), default = 'Body'),
              Field('kind', 'string', requires=IS_IN_SET(data.damagekinds_dict.keys()), default = 'physical',
                    label = 'Damage Kind'),
              Field('typ', 'string', requires=IS_IN_SET(['ballistic','impact']), default = 'ballistic'),
              Field('percent', 'boolean', default = False),
              Field('resist', 'boolean', default = False)]
    form = SQLFORM.factory(*fields, table_name = 'damage_apply')
    if form.process().accepted:
        char = basic.Char(db, char_id)
        char_property_putter = basic.CharPropertyPutter(char)
        damage_text = char_property_putter.put_damage(form.vars.damage,
                                                      form.vars.penetration,
                                                      form.vars.bodypart,
                                                      form.vars.kind,
                                                      form.vars.typ,
                                                      form.vars.percent,
                                                      form.vars.resist
                                                      )
        response.flash = damage_text
    elif form.errors:
       response.flash = 'form has errors'
    else:
       response.flash = 'please fill out the form'
    return dict(form=form)
