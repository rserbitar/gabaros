# coding: utf8
# versuche so etwas wie
import basic
import data
import rules

def index():
    redirect(URL('manage_chars'))

@auth.requires_login()
def insert_button():
    table = request.args(0)
    name = request.args(1)
    value = request.args(2).replace('_',' ')
    reload = request.args(3)
    db[table].bulk_insert([{'char':get_char(), name:value}])
    response.flash = '{} was added'.format(value)
    if reload:
        redirect(URL(reload), client_side=True)
    return dict()

def my_ondelete(function):
    def func(table, id):
        db(table[table._id.name] == id).delete()
        redirect(URL(function), client_side=True)
    return func

def select_char(id):
    session.char=int(id)
    return  A(id, _href=URL("edit_char", args=(id)))

def get_table(table_name, insert_table=False, insert_value=False, reload = False):
    dictionary = getattr(data, table_name + '_dict')
    first = list(dictionary[dictionary.keys()[0]]._fields)
    if insert_table:
        first.append('insert')
    dict_data = []
    for entry in dictionary.values():
        dict_data.append(list(entry))
        if insert_table:
            dict_data[-1].append(A('Insert', callback=URL('insert_button', args = [insert_table, insert_value, dict_data[-1][1], reload])))
    for i, row in enumerate(dict_data):
        for j, entry in enumerate(row):
            if isinstance(entry,list):
                dict_data[i][j] = ', '.join([str(k) for k in entry])
            if isinstance(entry,float):
                dict_data[i][j] = round(entry, 2)
    table = [first]
    table.extend(dict_data)
    return table

@auth.requires_login()
def manage_chars():
    table = db.chars
    query = db.chars.player == auth.user.id or db.chars.master == auth.user.id
    table.id.represent = select_char
    table.player.represent = lambda player: db.auth_user[player].username
    create = crud.create(table)
    form = crud.select(table, query=query, fields=["id", "name"])
    return dict(form=form, create=create)


@auth.requires_login()
def edit_char():
    char = request.args(0)
    session.char = int(char)
    if not db.chars[char] or (db.chars[char].player != auth.user.id
                              and db.chars[char].master != auth.user.id):
        redirect(URL(f='index'))
    table = db.chars
    table.player.writable = False
    table.player.represent = lambda player: db.auth_user[player].username
    basic.Char(db, char)
    form = crud.update(table, char)
    return dict(form=form)


@auth.requires_login()
def edit_attributes():
    char_id = get_char()
    fields = []
    attributes = []
    rows = db(db.char_attributes.char == char_id).select(db.char_attributes.ALL)
    for row in rows:
        fields += [Field(row.attribute, 'double', default=row.value)]
    form = SQLFORM.factory(*fields, ondelete=my_ondelete('edit_attributes'))
    if form.accepts(request.vars, session):
        response.flash = 'form accepted'
        for entry in form.vars:
            db((db.char_attributes.char == char_id) & (db.char_attributes.attribute == entry)).update(value=form.vars[entry])
        db.commit()
    elif form.errors:
        response.flash = 'form has errors'
    rows = db(db.char_attributes.char == char_id).select(db.char_attributes.ALL)
    base = {}
    xp = {}
    total_attribute_xp = 0
    char = basic.Char(db, char_id)
    getter_base = basic.CharPropertyGetter(char, 'base')
    getter_unaugmented = basic.CharPropertyGetter(basic.Char(db, char_id), 'unaugmented')
    for row in rows:
        attribute = row.attribute
        form.custom.widget[attribute]['value'] = row.value
        form.custom.widget[attribute]['_style'] = 'width:50px'
        form.custom.widget[attribute]._postprocessing()
        base[attribute] = getter_base.get_attribute_value(attribute)
        xp[attribute] = round(getter_unaugmented.get_attribute_xp_cost(attribute))
        total_attribute_xp += xp[attribute]
    char_property_getter = basic.CharPropertyGetter(char, modlevel='augmented')
    char_xp = char_property_getter.get_xp()
    total_xp = sum(char_property_getter.get_total_exp().values())
    return dict(form=form, attributes=data.attributes_dict.keys(),
                xp=xp, base=base, total_attribute_xp=total_attribute_xp, total_xp=total_xp, char_xp = char_xp)


@auth.requires_login()
def edit_skills():
    char_id = get_char()
    fields = []
    skills = []
    rows = db(db.char_skills.char == char_id).select(db.char_skills.ALL)
    for row in rows:
        fields += [Field(row.skill.replace(' ', '_'), 'double', default=row.value, label=row.skill)]
    form = SQLFORM.factory(*fields, ondelete=my_ondelete('edit_skills'))
    if form.accepts(request.vars, session):
        response.flash = 'form accepted'
        for entry in form.vars:
            db((db.char_skills.char == char_id) & (db.char_skills.skill == entry.replace('_', ' '))).update(value=form.vars[entry])
        db.commit()
    elif form.errors:
        response.flash = 'form has errors'
    rows = db(db.char_skills.char == char_id).select(db.char_skills.ALL)
    base = {}
    weight = {}
    xp = {}
    total_skill_xp = 0
    char = basic.Char(db, char_id)
    getter = basic.CharPropertyGetter(char, 'unaugmented')
    for row in rows:
        skillfield = row.skill.replace(' ', '_')
        skill = row.skill
        form.custom.widget[skillfield]['value'] = row.value
        form.custom.widget[skillfield]['_style'] = 'width:50px'
        form.custom.widget[skillfield]._postprocessing()
        parent = data.skills_dict[skill].parent
        base_val = 0
        if parent:
            base_val = getter.get_skill_value(parent)
        base[skillfield] = base_val
        weight[skillfield] = data.skills_dict[skill].expweight
        xp[skillfield] = round(getter.get_skill_xp_cost(skill))
        total_skill_xp += xp[skillfield]
    char_property_getter = basic.CharPropertyGetter(char, modlevel='augmented')
    char_xp = char_property_getter.get_xp()
    total_xp = sum(char_property_getter.get_total_exp().values())
    return dict(form=form, skills=[i.replace(" ", "_") for i in data.skills_dict.keys()],
                xp=xp, base=base, total_skill_xp=total_skill_xp, weight = weight, char_xp = char_xp, total_xp = total_xp)

@auth.requires_login()
def manage_powers():
    char_id = get_char()
    table = db.char_adept_powers
    table.value.show_if = (table.power.belongs([power.name for power in data.adept_powers_dict.values() if power.cost == 'X']))
    table.char.default = char_id
    query = (table.char == char_id)
    maxtextlength = {'char_adept_powers.power': 50, 'char_adept_powers.value': 100}
    table.value.represent = lambda value, row: basic.CharAdeptPower(db, row.power, basic.Char(db, char_id)).get_description()
    form = SQLFORM.grid(query, fields = [table.power, table.value], csv = False, maxtextlengths = maxtextlength, ondelete=my_ondelete('manage_powers'))
    table = get_table('adept_powers', 'char_adept_powers', 'power', 'manage_powers')
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id), modlevel='augmented')
    cost = char_property_getter.get_power_cost()
    magic = char_property_getter.get_attribute_value('Magic')
    return dict(form=form, table=table, cost=cost, magic=magic)


@auth.requires_login()
def manage_ware():
    char_id = get_char()
    table = db.char_ware
    table.char.default = char_id
    query = (table.char == char_id)
    table.ware.represent = lambda ware, row: A(ware, _href=URL("edit_ware", args=(row.id)))
    maxtextlength = {'table.ware': 50}
    char = basic.Char(db, char_id)
    links = [dict(header='Cost', body=lambda row: int(round(basic.CharWare(db, row.ware, row.id, char).get_cost()))),
             dict(header='Essence', body=lambda row: round(basic.CharWare(db, row.ware, row.id, char).get_essence_cost(),2))]
    form = SQLFORM.grid(query, fields = [table.id, table.ware], csv = False,
                        maxtextlength = maxtextlength,
                        links = links,
                        ondelete=my_ondelete('manage_ware'),
                        oncreate = (lambda form: basic.CharWare(db, form.vars.ware, form.vars.id, basic.Char(db, char_id))))
    table = get_table('ware', 'char_ware', 'ware', 'manage_ware')
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id), modlevel='augmented')
    cost = char_property_getter.get_total_cost()
    total_cost = sum(cost.values())
    money = char_property_getter.get_money()
    essence = char_property_getter.get_attribute_value('Essence')
    return dict(form=form, table=table, total_cost = total_cost, money = money, essence = essence)


@auth.requires_login()
def manage_fixtures():
    char_id = get_char()
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id), 'augmented')
    bodyparts = []
    for bodypart in data.bodyparts_dict:
        capacity = char_property_getter.char_body.bodyparts[bodypart].get_capacity()
        if capacity:
            used = char_property_getter.char_body.bodyparts[bodypart].get_used_capacity()
            bodyparts.append([bodypart, round(capacity,2), round(used,2)])
    table = db.char_fixtures
    table.char.default = char_id
    query = (table.char == char_id)
    maxtextlength = {'table.fixture' : 50}
    char = basic.Char(db, char_id)
    links = [dict(header='Cost', body=lambda row: data.fixtures_dict[row.fixture].cost),
             dict(header='Capacity', body=lambda row: {key:round(value,2) for key,value in basic.CharFixture(row.fixture, char).get_capacity_dict().items()})]
    form = SQLFORM.grid(query, fields = [table.id, table.fixture], csv = False, maxtextlength=maxtextlength, links=links, ondelete=my_ondelete('manage_fixtures'))
    table = get_table('fixtures', 'char_fixtures', 'fixture', 'manage_fixtures')
    cost = char_property_getter.get_total_cost()
    total_cost = sum(cost.values())
    money = char_property_getter.get_money()
    return dict(form=form, bodyparts=bodyparts, table=table, total_cost = total_cost, money = money)


@auth.requires_login()
def manage_upgrades():
    char_id = get_char()
    table = db.item_upgrades
    table.char.default = char_id
    query = (table.char == char_id)
    char = basic.Char(db, char_id)
    form = SQLFORM.grid(query, fields = [table.id, table.item, table.upgrade], csv = False, ondelete=my_ondelete('manage_upgrades'))
    return dict(form=form)

@auth.requires_login()
def upgrade_item():
    char_id = get_char()
    char_gameitem_id = int(request.args(0))
    table = db.char_items
    gameitem_name = table[char_gameitem_id].item
    if not table[char_gameitem_id].char == char_id:
        redirect(URL('manage_chars'))
    gameitem = data.gameitems_dict[gameitem_name]
    capacity = gameitem.capacity
    upgradeables = gameitem.upgradeables[:]
    if gameitem.clas == 'Ranged Weapon':
        capacity = []
        ranged_weapon = data.rangedweapons_dict[gameitem.name]
        if ranged_weapon.top:
            upgradeables.extend(data.rangedweapon_upgrades['top'])
            capacity.append('top')
        if ranged_weapon.barrel:
            upgradeables.extend(data.rangedweapon_upgrades['barrel'])
            capacity.append('barrel')
        if ranged_weapon.under:
            upgradeables.extend(data.rangedweapon_upgrades['under'])
            capacity.append('under')
    fields = [Field('upgrade', 'string', requires=IS_IN_SET(upgradeables))]
    upgradeables = [data.gameitems_dict[i] for i in upgradeables]
    if gameitem.clas not in  ['Ranged Weapon']:
        upgradeables = [(i.name, i.absolute_capacity+i.relative_capacity*capacity) for i in upgradeables]
    else:
        upgradeables = [(i.name) for i in upgradeables]
    form = SQLFORM.factory(*fields)
    if form.accepts(request.vars, session):
        response.flash = 'form accepted'
        upgrade = form.vars.upgrade
        id = db.char_items.insert(char=char_id, item=upgrade, location = None, loadout = None, rating = None)
        db.item_upgrades.insert(char=char_id, item = char_gameitem_id, upgrade = id)
    elif form.errors:
        response.flash = 'form has errors'
    upgrades = db(db.item_upgrades.item==char_gameitem_id).select(db.item_upgrades.id, db.item_upgrades.upgrade)
    if gameitem.clas not in  ['Ranged Weapon']:
        upgrades = [(A(i.upgrade.item, _href=URL("upgrade_item", args=(i.upgrade.id))),
                     data.gameitems_dict[i.upgrade.item].absolute_capacity+data.gameitems_dict[i.upgrade.item].relative_capacity*capacity,
                    A("Unlink", callback=URL('unlink_upgrade', args=[i.id, char_gameitem_id]), _class='btn'),
                    A("Delete", callback=URL('delete_upgrade', args=[i.upgrade.id, i.id, char_gameitem_id]), _class='btn'))
                    for i in upgrades]
    else:
        upgrades = [(A(i.upgrade.item, _href=URL("upgrade_item", args=(i.upgrade.id))),
                       data.rangedweapon_upgrades_reverse[i.upgrade.item],
                    A("Unlink", callback=URL('unlink_upgrade', args=[i.id, char_gameitem_id]), _class='btn'),
                    A("Delete", callback=URL('delete_upgrade', args=[i.upgrade.id, i.id, char_gameitem_id]), _class='btn'))
                for i in upgrades]
    if isinstance(capacity, float) or isinstance(capacity, int):
        free_capacity = capacity - sum([i[1] for i in upgrades])
    else:
        free_capacity = set(capacity) - set([i[1] for i in upgrades])
    return dict(name = gameitem_name, form=form, upgrades=upgrades, upgradeables=upgradeables, capacity=capacity, free_capacity=free_capacity)

@auth.requires_login()
def unlink_upgrade():
    char_id = get_char()
    id = int(request.args(0))
    char_gameitem_id = int(request.args(1))
    db(db.item_upgrades.id == id).delete()
    redirect(URL('upgrade_item', args=[char_gameitem_id]), client_side=True)


@auth.requires_login()
def delete_upgrade():
    char_id = get_char()
    item_id = int(request.args(0))
    unlink_id = int(request.args(1))
    char_gameitem_id = int(request.args(2))
    db(db.item_upgrades.id == unlink_id).delete()
    db(db.char_items.id == item_id).delete()
    redirect(URL('upgrade_item', args=[char_gameitem_id]), client_side=True)


@auth.requires_login()
def edit_ware():
    char_id = get_char()
    char_ware_id = request.args(0)
    ware = db.char_ware[char_ware_id].ware
    fields = []
    attributes = []
    rows = db(db.char_ware_stats.ware == char_ware_id).select(db.char_ware_stats.ALL)
    for row in rows:
        fields += [Field(row.stat, 'double', default=row.value)]
    form = SQLFORM.factory(*fields, ondelete=my_ondelete('edit_ware'))
    if form.accepts(request.vars, session):
        response.flash = 'form accepted'
        for entry in form.vars:
            db((db.char_ware_stats.ware == char_ware_id) & (db.char_ware_stats.stat == entry)).update(value=form.vars[entry])
        db.commit()
    elif form.errors:
        response.flash = 'form has errors'
    rows = db(db.char_ware_stats.ware == char_ware_id).select(db.char_ware_stats.ALL)
#    base = {}
#    xp = {}
#    modified = {}
    for row in rows:
        stat = row.stat
        form.custom.widget[stat]['value'] = row.value
        form.custom.widget[stat]['_style'] = 'width:50px'
        form.custom.widget[stat]._postprocessing()
#        base[attribute] = database.get_attrib_xp_base(db, cache, char, attribute)
#        xp[attribute] = database.get_attrib_xpcost(db, cache, char, attribute)
#        modified[attribute] = database.get_attribute_value(db, cache, attribute, char, mod='modified')
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id), 'augmented')
    cost = char_property_getter.get_total_cost()
    total_cost = sum(cost.values())
    money = char_property_getter.get_money()
    return dict(ware=ware, total_cost = total_cost, money = money,
                form=form, stats=[key for key, value in data.attributes_dict.items()
                                             if value.kind == 'physical' or value.name == 'Weight'] + ['Essence'])


@auth.requires_login()
def edit_damage():
    char_id = get_char()
    table = db.char_damage
    table.char.default = char_id
    query = db.char_damage.char == char_id
    form = SQLFORM.grid(query, fields = [table.damagekind, table.value], csv = False)
    return dict(form=form)


@auth.requires_login()
def edit_wounds():
    char_id = get_char()
    table = db.char_wounds
    table.char.default = char_id
    query = db.char_wounds.char == char_id
    form = SQLFORM.grid(query, fields = [table.bodypart, table.damagekind, table.value], csv = False)
    return dict(form=form)


@auth.requires_login()
def edit_items():
    char_id = get_char()
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id), 'augmented')
    table = db.char_items
    table.rating.show_if = (table.item.belongs([item.name for item in data.gameitems_dict.values() if item.rating]))
    table.char.default = char_id
    table.item.represent = lambda item, row: A(item, _href=URL("upgrade_item", args=(row.id)))
    query = table.char == char_id
    links = [dict(header='Cost', body=lambda row: int(round(rules.cost_by_rating(data.gameitems_dict[row.item].rating, data.gameitems_dict[row.item].cost, row.rating))))]
    form = SQLFORM.grid(query, fields = [table.item, table.rating, table.loadout, table.location], csv = False, ondelete=my_ondelete('edit_items'), links=links )
    table = get_table('gameitems', 'char_items', 'item', 'edit_items')
    cost = char_property_getter.get_total_cost()
    total_cost = sum(cost.values())
    money = char_property_getter.get_money()
    return dict(form=form, table=table, total_cost = total_cost, money = money)

@auth.requires_login()
def manage_spells():
    char_id = get_char()
    table = db.char_spells
    table.char.default = char_id
    query = table.char == char_id
    form = SQLFORM.grid(query, fields = [table.spell], csv = False)
    return dict(form=form)

@auth.requires_login()
def manage_metamagic():
    char_id = get_char()
    table = db.char_metamagic
    table.char.default = char_id
    query = table.char == char_id
    form = SQLFORM.grid(query, fields = [table.metamagic], csv = False)
    return dict(form=form)


@auth.requires_login()
def edit_sins():
    char_id = get_char()
    table = db.char_sins
    table.locations.requires = IS_IN_DB(db(db.char_locations.char == char_id), 'char_locations.id', '%(name)s', multiple=True)
    table.char.default = char_id
    query = table.char == char_id
    form = SQLFORM.grid(query, fields = [table.name, table.rating, table.permits, table.locations], csv = False)
    return dict(form=form)


@auth.requires_login()
def edit_locations():
    char_id = get_char()
    table = db.char_locations
    table.char.default = char_id
    query = table.char == char_id
    form = SQLFORM.grid(query, fields = [table.name], csv = False)
    return dict(form=form)

@auth.requires_login()
def edit_contacts():
    char_id = get_char()
    master_id = db(db.chars.id==char_id).select(db.chars.master).first().master
    table1 = db.contacts
    table1.master.default = master_id
    query1 = (table1.master == master_id)
    form1 = SQLFORM.grid(query1, fields = [table1.name], csv = False)
    return dict(form=form1)

@auth.requires_login()
def edit_char_contacts():
    char_id = get_char()
    master_id = db(db.chars.id==char_id).select(db.chars.master).first().master
    table2 =db.char_contacts
    table2.char.default = char_id
    query2 = (table2.char == char_id)
    form2 = SQLFORM.grid(query2, fields = [table2.name], csv = False)
    return dict(form=form2)


@auth.requires_login()
def manage_contacts():
    char_id = get_char()
    master_id = db(db.chars.id==char_id).select(db.chars.master).first().master
    return dict()

@auth.requires_login()
def edit_loadout():
    char_id = get_char()
    query = (db.char_loadout.char==char_id)

    if request.vars.get('loadout'):
        db.char_loadout.update_or_insert(query, value=request.vars.get('loadout'), char = char_id)
    val = db(query).select(db.char_loadout.value).first()
    if not val:
        val = 0
    else:
        val = int(val.value)
    fields1 = [Field('loadout', 'integer', default=val, label = 'Loadout', requires=IS_IN_SET(list(range(10))))]
    form1 = SQLFORM.factory(*fields1)

    if form1.process(formname='form_one').accepted:
        if form1.vars.get('loadout') is not None:
            db.char_loadout.update_or_insert(query, value=form1.vars.get('loadout'), char = char_id)
            form1.custom.widget['loadout']['value'] = form1.vars.get('loadout')
            form1.custom.widget['loadout']._postprocessing()

    items = db(db.char_items.char == char_id).select(db.char_items.id, db.char_items.item, db.char_items.loadout)
    fields2 = [Field('item_{}_{}'.format(i.id,j), 'boolean', default=True if j in i.loadout else False) for i in items for j in range(10)]
    form2 = SQLFORM.factory(*fields2)
    if form2.process(formname='form_two').accepted:
        for item in items:
            templist = []
            for j in range(10):
                if form2.vars['item_{}_{}'.format(item.id, j)]:
                    templist.append(j)
                form2.custom.widget['item_{}_{}'.format(item.id, j)]['value'] = form2.vars['item_{}_{}'.format(item.id, j)]
                form2.custom.widget['item_{}_{}'.format(item.id, j)]._postprocessing()
            db(db.char_items.id == item.id).update(loadout = templist)
    return dict(form1 = form1, form2=form2, items=[(i.id, i.item) for i in items])


@auth.requires_login()
def edit_computers():
    char_id = get_char()
    table = db.char_computers
    table.char.default = char_id
    owned_decks =db((db.char_items.char == char_id) &
                         (db.char_items.item.belongs(data.computer_dict.keys()))
                        )
    table.item.requires = IS_IN_DB(owned_decks, 'char_items.id', '%(item)s')
    query = table.char == char_id
    form = SQLFORM.grid(query, fields = [table.item, table.firewall, table.current_uplink, table.damage], csv = False)
    return dict(form=form)

@auth.requires_login()
def manage_money():
    char_id = get_char()
    table = db.char_money
    table.char.default = char_id
    query = table.char == char_id
    form = SQLFORM.grid(query, fields = [table.money, table.usage, table.timestamp], csv = False, ondelete=my_ondelete('manage_money'))
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id), modlevel='augmented')
    cost = char_property_getter.get_total_cost()
    total_cost = sum(cost.values())
    money = char_property_getter.get_money()
    return dict(form=form, total_cost = total_cost, money=money)

@auth.requires_login()
def manage_xp():
    char_id = get_char()
    table = db.char_xp
    table.char.default = char_id
    query = table.char == char_id
    form = SQLFORM.grid(query, fields = [table.xp, table.usage, table.timestamp], csv = False, ondelete=my_ondelete('manage_xp'))
    char_property_getter = basic.CharPropertyGetter(basic.Char(db, char_id), modlevel='augmented')
    char_xp = char_property_getter.get_xp()
    total_xp = sum(char_property_getter.get_total_exp().values())
    cost = char_property_getter.get_total_cost()
    total_cost = sum(cost.values())
    money = char_property_getter.get_money()
    return dict(form=form, total_cost = total_cost, money=money, total_xp = total_xp, char_xp = char_xp)
