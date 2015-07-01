# coding: utf8
import collections
import applications.gabaros.modules.data as data
def gametables():
    table = ''
    dictionaries = {i[:-5].replace('_', ' ').capitalize():getattr(data,i) for i in dir(data) if i[-5:] == '_dict'}
    fields = Field('table', type='str', requires=IS_IN_SET(dictionaries.keys()), label = 'Table')
    form=SQLFORM.factory(fields)
    if form.process().accepted:
        dictionary = dictionaries[form.vars.table]
        first = dictionary[dictionary.keys()[0]]
        dict_data = []
        for entry in dictionary.values():
            dict_data.append(list(entry))
        for i, row in enumerate(dict_data):
            for j, entry in enumerate(row):
                if isinstance(entry,list):
                    dict_data[i][j] = ', '.join([str(k) for k in entry])
        table = [first._fields]
        table.extend(dict_data)
    elif form.errors:
       response.flash = 'form has errors'
    else:
       response.flash = 'Please select a table'

    return dict(form=form, table=table)