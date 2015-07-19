# coding: utf8
import collections
import applications.gabaros.modules.data as data
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
