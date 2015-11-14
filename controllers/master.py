# coding: utf8
import collections
import applications.gabaros.modules.data as data
import applications.gabaros.modules.rules as rules
from random import gauss

@auth.requires_login()
def index():
    return dict()


@auth.requires_login()
def chat():
    form=LOAD('master', 'ajax_form', ajax=True)
    script=SCRIPT("""
        var text = ''
        jQuery(document).ready(function(){
        var callback = function(e){alert(e.data);
            text = e.data + '<br>' + text;
            document.getElementById('text').innerHTML = text;};
          if(!$.web2py.web2py_websocket('ws://127.0.0.1:8888/realtime/""" + str(auth.user.id) + """', callback))
            alert("html5 websocket not supported by your browser, try Google Chrome");
        });
    """)
    return dict(form=form, script=script)

@auth.requires_login()
def ajax_form():
    players = db(db.chars.master==auth.user.id).select(db.chars.name)
    players = [i.name for i in players]
    form=SQLFORM.factory(Field('message'),
                         Field('players',
                               type='list',
                               requires=IS_IN_SET(players)))
    if form.accepts(request,session):
        from gluon.contrib.websocket_messaging import websocket_send
        players = form.vars.players
        if not isinstance(players, list):
            players = [players]
        for player in players:
            websocket_send(
                'http://127.0.0.1:8888', form.vars.message, 'mykey', player)
    return form


@auth.requires_login()
def livedata():
    db.rolls.char.represent = lambda char: db.chars[char].name
    db.rolls.roll.represent = lambda val: int(round(val))
    db.rolls.value.represent = lambda val: int(round(val))
    db.rolls.result.represent = lambda val: int(round(val))
    rows = db(db.rolls.char.belongs(db(db.chars.master == auth.user.id)._select(db.chars.id))).select(db.rolls.ALL, orderby=~db.rolls.id,
                                                                         limitby=(0, 10), distinct=True)
    table = SQLTABLE(rows, headers='labels', _class = 'table table-striped')
    return dict(rows=rows, table=table)

@auth.requires_login()
def live():
    db.rolls.char.represent = lambda char: db.chars[char].name
    db.rolls.roll.represent = lambda val: int(round(val))
    db.rolls.value.represent = lambda val: int(round(val))
    db.rolls.result.represent = lambda val: int(round(val))
    rows = db(db.rolls.char.belongs(db(db.chars.master == auth.user.id)._select(db.chars.id))).select(db.rolls.ALL, orderby=~db.rolls.id,
                                                                         limitby=(0, 10), distinct=True)
    table = SQLTABLE(rows, headers='labels', _class = 'table table-striped')
    return dict(rows=rows, table=table)

@auth.requires_login()
def combat():
    initiative = [None, None]
    combats = []
    combat = session.master_current_combat
    rows = db(db.combats.master==auth.user.id).select(db.combats.name)
    for row in rows:
        combats.append(row.name)
    form = SQLFORM.factory(Field('combat', requires=IS_IN_SET(combats), label = 'Combat'))
    if form.process().accepted:
        response.flash = 'form accepted'
        combat = form.vars.combat
        session.master_current_combat = combat
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    if combat:
        db.actions.char.represent = lambda char: db.chars[char].name
        rows = db((db.actions.combat==db.combats.id) & (db.combats.name == combat)).select(db.actions.char, db.actions.cost)
        if rows:
            initiative = collections.defaultdict(int)
            for row in rows:
                char = row.char.name
                cost = row.cost
                initiative[char] += cost
            initiative = [[key, value] for key, value in initiative.items()]
            initiative = sorted(initiative, key = lambda x: x[1], reverse = True)
    tempinitiative = [['Char', 'Initiative']]
    tempinitiative.extend(initiative)
    initiative = tempinitiative

    return dict(initiative=initiative, form=form, combat = combat)

#@auth.requires_login()
#def combat():
#    fields = []
#    combatants = []
#    rows = db(db.chars.master == auth.user.id).select(db.chars.name)
#    for row in rows:
#        combatants += [row.name]
#    combatants += [""]
#    combatants = sorted(combatants)
#    fields += [Field("name", type='string', label=T('Name'))]
#    fields += [Field("combatant1", type='string', requires=IS_IN_SET(combatants), label=T('Combatant 1'), default=None)]
#    fields += [Field("combatant2", type='string', requires=IS_IN_SET(combatants), label=T('Combatant 2'), default=None)]
#    fields += [Field("combatant3", type='string', requires=IS_IN_SET(combatants), label=T('Combatant 3'), default=None)]
#    fields += [Field("combatant4", type='string', requires=IS_IN_SET(combatants), label=T('Combatant 4'), default=None)]
#    fields += [Field("combatant5", type='string', requires=IS_IN_SET(combatants), label=T('Combatant 5'), default=None)]
#    fields += [Field("combatant6", type='string', requires=IS_IN_SET(combatants), label=T('Combatant 6'), default=None)]
#    fields += [Field("combatant7", type='string', requires=IS_IN_SET(combatants), label=T('Combatant 7'), default=None)]
#    fields += [Field("combatant8", type='string', requires=IS_IN_SET(combatants), label=T('Combatant 8'), default=None)]
#    form = SQLFORM.factory(*fields)
#    if form.process(formname='form_one').accepted:
#        response.flash = 'form accepted'
#        id = db.combat.bulk_insert([{'name': form.vars.name, 'round': 1, 'master': auth.user.id}])[0]
#        for i in range(1, 9):
#            if form.vars['combatant' + str(i)]:
#                row = db(db.chars.name == form.vars['combatant' + str(i)]).select(db.chars.id).first()
#                combatant = row.id
#                db.combatants.bulk_insert([{'combat': id, 'char': combatant}])
#                initiative = database.get_initiative(db, cache, combatant) + gauss(0, 10)
#                db.combat_initiative.bulk_insert(
#                    [{'combat': id, 'round': 1, 'char': combatant, 'initiative': initiative}])
#    elif form.errors:
#        response.flash = 'form has errors'
#    form2 = SQLFORM.factory(*[Field('add', type='boolean', label=T('Add Round'), default=True, readable=False)],
#                            submit_button='Next Round')
#    combat = database.get_current_combat(db, auth.user.id)
#    if form2.process(formname='form_two').accepted:
#        response.flash = 'form accepted'
#        database.add_combat_round(db, auth.user.id)
#        round = db(db.combat.id == combat).select(db.combat.round).first().round
#        rows = db(db.combatants.combat == combat).select(db.combatants.char)
#        for row in rows:
#            combatant = row.char.id
#            initiative = database.get_initiative(db, cache, combatant) + gauss(0, 10)
#            db.combat_initiative.bulk_insert(
#                [{'combat': combat, 'round': round, 'char': combatant, 'initiative': initiative}])
#    elif form2.errors:
#        response.flash = 'form has errors'
#    cname = None
#    cround = None
#    row = db(db.combat.id == combat).select(db.combat.round, db.combat.name).first()
#    if row:
#        cname = row.name
#        cround = row.round
#    rows = db(db.combatants.combat == combat).select(db.combatants.char)
#    combatants = []
#    for row in rows:
#        charid = row.char.id
#        charname = row.char.name
#        awarecount, timecount = database.get_ccab(db, charid)
#        initiative = db((db.combat_initiative.combat == combat) & (db.combat_initiative.char == charid) & (
#        db.combat_initiative.round == cround)).select(db.combat_initiative.initiative).first()
#        if initiative:
#            initiative = initiative.initiative
#        else:
#            initiative = None
#        combatants += [[charid, charname, initiative, awarecount, timecount]]
#    combatants = sorted(combatants, key=lambda x: x[2], reverse=True)
#    return dict(form=form, form2=form2, cname=cname, cround=cround, combatants=combatants)


@auth.requires_login()
def calc_deck():
    fields = [Field("processor", 'float', default=0)]
    fields += [Field("system", 'float', default=0)]
    fields += [Field("uplink", 'float', default=0)]
    fields += [Field("size", 'float', default=0)]
    fields += [Field("hours_per_week", 'float', default=0)]
    fields += [Field("skill", 'float', default=0)]
    fields += [Field("users", 'float', default=0)]
    form = SQLFORM.factory(*fields)
    maintainance = 0
    cost = 0
    firewall = 0
    system = 0
    processor = 0
    uplink = 0
    if form.process().accepted:
        response.flash = 'form accepted'
        processor = form.vars["processor"]
        system = form.vars["system"]
        uplink = form.vars["uplink"]
        size = form.vars["size"]
        skill = form.vars["skill"]
        users = form.vars["users"]
        hours_per_week = form.vars["hours_per_week"]
        cost = (rules.processor_cost(processor, size) +
                rules.uplink_cost(uplink, size) +
                rules.system_cost(system, processor) +
                rules.size_cost(size))
        maintainance = rules.maintain_cost(size)
        firewall = rules.firewall_rating(hours_per_week, skill,
                                           system, users)

    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form, firewall=firewall, cost=cost, maintainance=maintainance, system=system, processor=processor,
                uplink=uplink)

def calc_vehicle():
    fields = [Field("chassis", 'string', requires=IS_IN_SET(data.vehicle_chassis_dict.keys()))]
    fields += [Field("computer", 'string', requires=IS_IN_SET(data.computer_dict.keys()))]
    fields += [Field("sensors", 'string', requires=IS_IN_SET([i[0] for i in data.sensor_packages_dict.keys()]))]
    fields += [Field("agent", 'string', requires=IS_IN_SET([data.agents_dict.keys()]))]
    form = SQLFORM.factory(*fields)
    chassis = []
    computer = []
    sensors = []
    agent = None
    capacity = 0
    used_capacity = 0
    free_capacity = 0

    if form.process().accepted:
        chassis = data.vehicle_chassis_dict[form.vars.chassis]
        computer = data.gameitems_dict[form.vars.computer]
        sensors = data.sensor_packages_dict[form.vars.sensors]
        capacity = chassis.capacity
        used_capacity = computer.absolute_capacity + sum([data.gameitems_dict[i].absolute_capacity for i in sensors.content])
    return dict(form=form, chassis=chassis, agent = agent, computer=computer, sensors=sensors, capacity=capacity, used_capacity=used_capacity,
               free_capacity = capacity-used_capacity)
