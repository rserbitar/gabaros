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
        unaugmented = char_property_getter.get_attribute_value(attribute)
        augmented = char_property_getter2.get_attribute_value(attribute)
        temporary = char_property_getter3.get_attribute_value(attribute)
        value = char_property_getter4.get_attribute_value(attribute)
        modval = char_property_getter4.get_attribute_test_value(attribute)
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
    actions = [["Action", "Prequesite", "Test", "Secret"]]
    for action, item in data.matrix_actions_dict.items():
        value = computer.get_action_value(action)
        prequesite = item.prequesite
        if value is not None:
            button1 = A("{:.0f}".format(value),
                    callback=URL('roll_button', args=[char_id, action, value, 1]), _class='btn')
            button2 = A("{:.0f}".format(value),
                    callback=URL('roll_button', args=[char_id, action, value, 0]), _class='btn')
        else:
            button1 = ''
            button2 = ''
        actions += [[action, prequesite, button1, button2]]
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
    row = []
    for computer_id in computers:
        computer = basic.Computer(db, computer_id, char)
        row.append(A(computer.name, _href=URL('view_matrix_actions', args = [char_id, computer_id])))
        row.append(computer.attributes['Processor'])
        row.append(computer.attributes['Signal'])
        row.append(computer.attributes['Firewall'])
        row.append(computer.attributes['Uplink'])
        row.append(computer.attributes['Current Uplink'])
        row.append(computer.damage)
    table.append(row)
    return dict(computer=table)


@auth.requires_login()
def view_weapons():
    char_id = request.args(0)
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    char = basic.Char(db, char_id)
    weapons = basic.CharPropertyGetter(char).get_weapons()
    table = [['Weapon', 'Skill', 'Val', 'Dam', 'Type', 'Pen', 'Range', 'Bullets', 'Rec', 'Mag', 'Type', 'Shoot']]
    for weapon in weapons:
        row = []
        row.append(weapon.name)
        row.append(weapon.skill)
        row.append('{:.0f}'.format(weapon.get_net_skill_value()))
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
    fields = [Field('val', 'integer', default=0, label = 'Modifications')]
    form = SQLFORM.factory(*fields, table_name = 'weapons',  buttons=[], _method = '', _action = None)
    form.element(_name='val')['_onblur']="ajax('/gabaros/view_char/insert_state_mod/{}/shoot', " \
                                         "['val'], '')".format(char_id)
    form.element(_name='val')['_onkeypress']="ajax('/gabaros/view_char/insert_state_mod/{}/shoot', " \
                                         "['val'], '')".format(char_id)
    return dict(weapons=table, insert_shoot_mod = LOAD('view_char','insert_shoot_mod.load',ajax=True, args = [char_id]))


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
    text = ('damage: {}, {}'.format(damage, result))
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
    for i,var in enumerate(vars):
        val = db(query[i]).select(db.state_mods.value).first()
        if val:
            val = int(val.value)
            form.element(_name=var).update(_value=val)
    return dict(form = form)