# coding: utf8
from datetime import datetime

db.define_table('rolls',
    Field('char', type='reference chars', label=T('Player'),
    writable=False,
    requires = IS_IN_DB(db,db.chars.id,'%(name)s')),
    Field('name', type = 'string', label = T('Name')),
    Field('value', type = 'double', label = T('Value')),
    Field('roll', type = 'double', label = T('Roll')),
    Field('result', type = 'double', label = T('Result')),
    Field('visible', type = 'boolean', label = T('Visible')),
    Field('time', type = 'datetime', label = T('Time'),
    writable = False, default = datetime.now()),
    )


db.define_table('state_mods',
    Field('char', type='reference chars', label=T('Player'),
    writable=False,
    requires = IS_IN_DB(db,db.chars.id,'%(name)s')),
    Field('name', type = 'string', label = T('Name')),
    Field('value', type = 'double', label = T('Value')),
    )


db.define_table('combats',
    Field('char', type='reference chars', label=T('Player'),
    writable=False,
    requires = IS_IN_DB(db,db.chars.id,'%(name)s')),
    Field('name', type = 'string', label = T('Name')),
    Field('lighting', type = 'string', label = T('Lighting')),
    Field('noise', type = 'string', label = T('Noise')),
    Field('environment', type = 'string', label = T('Environment')),
    )
    
db.define_table('actions',
    Field('char', type='reference chars', label=T('Player'),
    writable=False,
    requires = IS_IN_DB(db,db.chars.id,'%(name)s')),
    Field('combat', type = 'reference combats', requires = IS_IN_DB(db,db.combats.id,'%(name)s')),
    Field('action', type = 'string', label = T('Value')),
    Field('cost', type = 'double', label = T('Roll')),
    )
