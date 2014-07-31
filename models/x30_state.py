# coding: utf8
from datetime import datetime
import applications.gabaros2.modules.data as data


db.define_table('char_state',
                Field('char', type='reference chars', label=T('Character'), writable=False,
                      requires=IS_IN_DB(db, db.chars.id, '%(name)s')),
                Field('stat', type='string', label=T('Stat')), Field('value', type='double', label=T('Value')))

db.define_table('char_wounds',
                Field('char', type='reference chars', label=T('Character'),
                                     requires=IS_IN_DB(db, db.chars.id, '%(name)s'), writable=False),
                Field('bodypart', type='string', requires=IS_IN_SET(data.bodyparts_dict.keys()), label=T('Body Part')),
                Field('damagekind', type='string', requires=IS_IN_SET(data.damagekinds_dict.keys()), label=T('Damage Kind')),
                Field('value', type='double', label=T('Value')))

db.define_table('char_damage',
                Field('char', type='reference chars', label=T('Character'),
                                     requires=IS_IN_DB(db, db.chars.id, '%(name)s'), writable=False),
                Field('damagekind', type='string', requires=IS_IN_SET(data.damagekinds_dict.keys()), label=T('Damage Kind')),
                Field('value', type='double', label=T('Value')))

db.define_table('char_xp',
                Field('char', type='reference chars', label=T('Character'),
                                     requires=IS_IN_DB(db, db.chars.id, '%(name)s'), writable=False),
                Field('xp', type='float'))
