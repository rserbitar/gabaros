# coding: utf8
from datetime import datetime
import data


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
                Field('xp', type='float'),
                Field('usage', type='string', requires=IS_IN_SET(['rewards', 'money', 'hand of god', 'other']), default = 'other'),
                Field('timestamp', type='date'))

db.define_table('char_money',
                Field('char', type='reference chars', label=T('Character'),
                                     requires=IS_IN_DB(db, db.chars.id, '%(name)s'), writable=False),
                Field('money', type='float'),
                Field('usage', type='string', requires=IS_IN_SET(['income', 'lifestyle', 'other']), default = 'other'),
                Field('timestamp', type='date')
                )

db.define_table('char_loadout',
                Field('char', type='reference chars', label=T('Character'),
                                     requires=IS_IN_DB(db, db.chars.id, '%(name)s'), writable=False),
                Field('value', type='integer', requires=IS_IN_SET([0,1,2,3,4,5,6,7,8,9]), default=0))
