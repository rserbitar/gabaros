# coding: utf8
import collections
import applications.gabaros.modules.data as data
import spirit
import vehicle

def gametables():
    table_name = request.args(0)
    if table_name:
        table_name = table_name.replace('_',' ')
    table = ''
    tablename=''
    dictionaries = {i[:-5].replace('_', ' ').capitalize():getattr(data,i) for i in dir(data) if i[-5:] == '_dict'}
    fields = Field('table', type='str', requires=IS_IN_SET(sorted(dictionaries.keys())), label = 'Table')
    form=SQLFORM.factory(fields)
    if form.process().accepted:
        table_name = form.vars.table
        tablename=form.vars.table
    if table_name:
        if not tablename:
            tablename = table_name.replace('_', ' ')
        dictionary = dictionaries[table_name]
        first = dictionary[dictionary.keys()[0]]
        dict_data = []
        for entry in dictionary.values():
            dict_data.append(list(entry))
        for i, row in enumerate(dict_data):
            for j, entry in enumerate(row):
                if isinstance(entry,list):
                    dict_data[i][j] = ', '.join([str(k) for k in entry])
                if isinstance(entry,float):
                    dict_data[i][j] = round(entry, 2)
        table = [first._fields]
        table.extend(dict_data)
    elif form.errors:
       response.flash = 'form has errors'
    else:
       response.flash = 'Please select a table'

    return dict(form=form, table=table, tablename=tablename)


def view_spirit():
    fields = [Field('force', type='int', label = 'Force'),
              Field('class_', type='str', requires=IS_IN_SET(['creation', 'destruction', 'detection', 'manipulation']), label = 'Class'),
             Field('manifestation', type='str', requires=IS_IN_SET(['ethereal', 'fluid', 'solid']), label = 'Manifestation')]
    summoned = None
    form=SQLFORM.factory(*fields)
    if form.process().accepted:
        force, class_, manifestation = float(form.vars.force), form.vars.class_, form.vars.manifestation
        summoned = spirit.Spirit(force, class_, manifestation)
    return dict(form=form, summoned=summoned)


def view_vehicle():
    fields = [Field('vehicle', type='str', requires=IS_IN_SET(data.vehicles_dict.keys()), label = 'Vehicle')]
    vehicle = None
    form=SQLFORM.factory(*fields)
    if form.process().accepted:
        vehicle = data.vehicles_dict[form.vars.vehicle]
        vehicle = vehicle.Vehicle(vehicle.chassis, vehicle.agent, vehicle.computer, vehicle.sensors_package)
    return dict(form=form, vehicle=vehicle)
