# coding: utf8
# versuche so etwas wie
import basic
import data

def index():
    redirect(URL('manage_chars'))

@auth.requires_login()
def manage_chars():
    table = db.chars
    query = db.chars.player == auth.user.id or db.chars.master == auth.user.id
    table.id.represent = lambda id: A(id, _href=URL("edit_char", args=(id)))
    table.player.represent = lambda player: db.auth_user[player].username
    create = crud.create(table)
    form = crud.select(table, query=query, fields=["id", "name"])
    return dict(form=form, create=create)


@auth.requires_login()
def edit_char():
    char = request.args(0)
    session.char = char
    if not db.chars[char] or (db.chars[char].player != auth.user.id
                              and db.chars[char].master != auth.user.id):
        redirect(URL(f='index'))
    table = db.chars
    table.player.writable = False
    table.player.represent = lambda player: db.auth_user[player].username
    basic.Char(db, char)
    form = crud.update(table, char)
    linklist = [A("attributes", _href=URL('edit_attributes', args=[char])),
                A("skills", _href=URL('edit_skills', args=[char])),
                A("damage", _href=URL('edit_damage', args=[char])),
                A("wounds", _href=URL('edit_wounds', args=[char])),
                A("items", _href=URL('edit_items', args=[char])),
                A("loadout", _href=URL('edit_loadout', args=[char])),
                A("sins", _href=URL('edit_sins', args=[char])),
                A("locations", _href=URL('edit_locations', args=[char])),
                A("ware", _href=URL('manage_ware', args=[char])),
                A("adept powers", _href=URL('manage_powers', args=[char])),
                A("spells", _href=URL('manage_spells', args=[char])),
                A("computers", _href=URL('edit_computers', args=[char])),
                ]
    return dict(form=form, linklist=linklist)


@auth.requires_login()
def edit_attributes():
    char = request.args(0) or session.char
    if not db.chars[char] or (db.chars[char].player != auth.user.id
                              and db.chars[char].master != auth.user.id):
        redirect(URL(f='index'))
    charname = db.chars[char].name
    fields = []
    attributes = []
    rows = db(db.char_attributes.char == char).select(db.char_attributes.ALL)
    for row in rows:
        fields += [Field(row.attribute, 'double', default=row.value)]
    form = SQLFORM.factory(*fields)
    if form.accepts(request.vars, session):
        response.flash = 'form accepted'
        for entry in form.vars:
            db((db.char_attributes.char == char) & (db.char_attributes.attribute == entry)).update(value=form.vars[entry])
        db.commit()
    elif form.errors:
        response.flash = 'form has errors'
    rows = db(db.char_attributes.char == char).select(db.char_attributes.ALL)
    base = {}
    xp = {}
    total_xp = 0
    for row in rows:
        attribute = row.attribute
        form.custom.widget[attribute]['value'] = row.value
        form.custom.widget[attribute]['_style'] = 'width:50px'
        form.custom.widget[attribute]._postprocessing()
        base[attribute] = basic.CharPropertyGetter(basic.Char(db, char), 'base').get_attribute_value(attribute)
        xp[attribute] = round(basic.CharPropertyGetter(basic.Char(db, char), 'unaugmented').get_attribute_xp_cost(attribute))
        total_xp += xp[attribute]
    return dict(charname=charname, form=form, attributes=data.attributes_dict.keys(),
                xp=xp, base=base, total_xp=total_xp)


@auth.requires_login()
def edit_skills():
    char = request.args(0) or session.char
    if not db.chars[char] or (db.chars[char].player != auth.user.id
                              and db.chars[char].master != auth.user.id):
        redirect(URL(f='index'))
    charname = db.chars[char].name
    fields = []
    skills = []
    rows = db(db.char_skills.char == char).select(db.char_skills.ALL)
    for row in rows:
        fields += [Field(row.skill.replace(' ', '_'), 'double', default=row.value, label=row.skill)]
    form = SQLFORM.factory(*fields)
    if form.accepts(request.vars, session):
        response.flash = 'form accepted'
        for entry in form.vars:
            db((db.char_skills.char == char) & (db.char_skills.skill == entry.replace('_', ' '))).update(value=form.vars[entry])
        db.commit()
    elif form.errors:
        response.flash = 'form has errors'
    rows = db(db.char_skills.char == char).select(db.char_skills.ALL)
    base = {}
    weight = {}
    xp = {}
    total_xp = 0
    getter = basic.CharPropertyGetter(basic.Char(db, char), 'unaugmented')
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
        total_xp += xp[skillfield]
    return dict(charname=charname, form=form, skills=[i.replace(" ", "_") for i in data.skills_dict.keys()],
                xp=xp, base=base, total_xp=total_xp, weight = weight)


@auth.requires_login()
def manage_powers():
    char_id = request.args(0) or session.char
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                              and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    table = db.char_adept_powers
    table.char.default = char_id
    query = (table.char == char_id)
    maxlength = {'char_adept_powers.power': 50, 'char_adept_powers.value': 100}
    table.value.represent = lambda value, row: basic.CharAdeptPower(db, row.power, basic.Char(db, char_id)).get_description()
    form = SQLFORM.grid(query, fields = [table.power, table.value], csv = False, args=request.args[:1], maxtextlengths = maxlength)
    return dict(form=form)


@auth.requires_login()
def manage_ware():
    char_id = request.args(0) or session.char
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                              and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    table = db.char_ware
    table.char.default = char_id
    query = (table.char == char_id)
    table.ware.represent = lambda ware, row: A(ware, _href=URL("edit_ware", args=(row.id)))
    form = SQLFORM.grid(query, fields = [table.id, table.ware], csv = False, args=request.args[:1],
                        oncreate = (lambda form: basic.CharWare(db, form.vars.ware, form.vars.id, basic.Char(db, char_id))))
    return dict(form=form)


@auth.requires_login()
def edit_ware():
    char_ware_id = request.args(0)
    char = db(db.char_ware.id==char_ware_id).select(db.char_ware.char).first().char
    if not db.chars[char] or (db.chars[char].player != auth.user.id
                              and db.chars[char].master != auth.user.id):
        redirect(URL(f='index'))
    ware = db.char_ware[char_ware_id].ware
    fields = []
    attributes = []
    rows = db(db.char_ware_stats.ware == char_ware_id).select(db.char_ware_stats.ALL)
    for row in rows:
        fields += [Field(row.stat, 'double', default=row.value)]
    form = SQLFORM.factory(*fields)
    if form.accepts(request.vars, session):
        response.flash = 'form accepted'
        for entry in form.vars:
            db(db.char_ware_stats.ware == char_ware_id and db.char_ware_stats.stat == entry).update(value=form.vars[entry])
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
    return dict(ware=ware, form=form, stats=[key for key, value in data.attributes_dict.items()
                                             if value.kind == 'physical' or value.name == 'Weight'] + ['Essence'])


@auth.requires_login()
def edit_damage():
    char_id = request.args(0) or session.char
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    table = db.char_damage
    table.char.default = char_id
    query = db.char_damage.char == char_id
    form = SQLFORM.grid(query, fields = [table.damagekind, table.value], csv = False, args=request.args[:1])
    return dict(form=form)


@auth.requires_login()
def edit_wounds():
    char_id = request.args(0) or session.char
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                              and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    table = db.char_wounds
    table.char.default = char_id
    query = db.char_wounds.char == char_id
    form = SQLFORM.grid(query, fields = [table.bodypart, table.damagekind, table.value], csv = False, args=request.args[:1])
    return dict(form=form)


@auth.requires_login()
def edit_items():
    char_id = request.args(0) or session.char
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                              and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    table = db.char_items
    table.char.default = char_id
    query = table.char == char_id
    form = SQLFORM.grid(query, fields = [table.item, table.rating, table.loadout, table.location], csv = False, args=request.args[:1])
    return dict(form=form)

@auth.requires_login()
def manage_spells():
    char_id = request.args(0) or session.char
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                              and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    table = db.char_spells
    table.char.default = char_id
    query = table.char == char_id
    form = SQLFORM.grid(query, fields = [table.spell], csv = False, args=request.args[:1])
    return dict(form=form)


@auth.requires_login()
def edit_sins():
    char_id = request.args(0) or session.char
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                              and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    table = db.char_sins
    table.locations.requires = IS_IN_DB(db(db.char_locations.char == char_id), 'char_locations.id', '%(name)s', multiple=True)
    table.char.default = char_id
    query = table.char == char_id
    form = SQLFORM.grid(query, fields = [table.name, table.rating, table.permits, table.locations], csv = False, args=request.args[:1])
    return dict(form=form)


@auth.requires_login()
def edit_locations():
    char_id = request.args(0) or session.char
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                              and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    table = db.char_locations
    table.char.default = char_id
    query = table.char == char_id
    form = SQLFORM.grid(query, fields = [table.name], csv = False, args=request.args[:1])
    return dict(form=form)


@auth.requires_login()
def edit_loadout():
    char_id = request.args(0) or session.char
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                                 and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    query = (db.char_loadout.char==char_id)

    if request.vars.get('loadout'):
        db.char_loadout.update_or_insert(query, value=request.vars.get('loadout'), char = char_id)
    val = db(query).select(db.char_loadout.value).first()
    if not val:
        val = 0
    else:
        val = int(val.value)
    fields = [Field('loadout', 'integer', default=val, label = 'Loadout', requires=IS_IN_SET(list(range(10))))]
    form = SQLFORM.factory(*fields)
    form.element(_name='loadout')['_onblur']="ajax('/gabaros/manage_char/edit_loadout/{}', " \
                                            "['loadout'], '')".format(char_id)
    if form.process().accepts:
        if form.vars.get('loadout') is not None:
            db.char_loadout.update_or_insert(query, value=form.vars.get('loadout'), char = char_id)
            fields = [Field('loadout', 'integer', default=form.vars.get('loadout'), label = 'Loadout',
                            requires=IS_IN_SET(list(range(10))))]
            form = SQLFORM.factory(*fields)
    form.element(_name='loadout')['_onblur']="ajax('/gabaros/manage_char/edit_loadout/{}', " \
                                            "['loadout'], '')".format(char_id)
    return dict(form = form)


@auth.requires_login()
def edit_computers():
    char_id = request.args(0) or session.char
    if not db.chars[char_id] or (db.chars[char_id].player != auth.user.id
                              and db.chars[char_id].master != auth.user.id):
        redirect(URL(f='index'))
    table = db.char_computers
    table.char.default = char_id
    owned_decks =db((db.char_items.char == char_id) &
                         (db.char_items.item.belongs(data.computer_dict.keys()))
                        )
    table.item.requires = IS_IN_DB(owned_decks, 'char_items.id', '%(item)s')
    query = table.char == char_id
    form = SQLFORM.grid(query, fields = [table.item, table.firewall, table.current_uplink, table.damage], csv = False, args=request.args[:1])
    return dict(form=form)
