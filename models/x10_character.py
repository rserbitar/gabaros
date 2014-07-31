# coding: utf8
import applications.gabaros2.modules.data as data


db.define_table('chars', Field('player', type='reference auth_user', label=T('Player'), default=auth.user_id,
                               update=auth.user_id, writable=False),
                Field('master', type='reference auth_user', label=T('Master'),
                      requires=IS_IN_DB(db, db.auth_user.id, '%(username)s')),
                Field('name', type='string', label=T('Name')),
                Field('gender', type='string', label=T('Gender'), requires=IS_IN_SET(data.gendermods_dict.keys())),
                Field('race', type='string', label=T('Race'), requires=IS_IN_SET(data.races_dict.keys())),
                format=lambda x: x.name)

db.define_table('char_attributes', Field('char', type='reference chars', label=T('Character')),
                Field('attribute', type='string', label=T('Attribute'),
                      requires=IS_IN_SET(data.attributes_dict.keys())),
                Field('value', type='double', label=T('Value'), default=30))

db.define_table('char_skills', Field('char', type='reference chars', label=T('Character')),
                Field('skill', type='string', label=T('Skill'), requires=IS_IN_SET(data.skills_dict.keys())),
                Field('value', type='double', label=T('Value'), default=30))

db.define_table('char_items', Field('char', type='reference chars', label=T('Character'), writable=False),
                Field('item', type='string', label=T('Item'), requires=IS_IN_SET(data.gameitems_dict.keys())),
                Field('loadout', type='list:integer', label=T('Loadout'),
                      requires=IS_IN_SET([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], multiple=True), default=0))

db.define_table('char_ware', Field('char', type='reference chars', label=T('Character')),
                Field('ware', type='string', label=T('Ware'), requires=IS_IN_SET(data.ware_dict.keys())))

db.define_table('char_ware_stats', Field('ware', type='reference char_ware', label=T('Ware')),
                Field('stat', type='string', label=T('Stat')), Field('value', type='double', label=T('Value')))

db.define_table('char_decks', Field('char', type='reference chars', label=T('Character')),
                Field('item', type='reference char_items', label=T('Item')),
                Field('firewall', type='double', label=T('Firewall')),
                Field('current_uplink', type='double', label=T('Current Uplink')))

db.define_table('char_programmes', Field('char', type='reference chars', label=T('Character')),
                Field('programme', type='string', label=T('Programme'),
                      requires=IS_IN_SET(data.programmes_dict.keys())),
                Field('deck', type='reference char_items', label=T('Deck'),
                      requires=IS_IN_DB(db, db.char_items.id, '%(item)s')),
                Field('rating', type='double', label=T('Rating')))

db.define_table('char_locations', Field('char', type='reference chars', label=T('Character'), writable=False),
                Field('name', type='string', label=T('Name')), format=lambda x: x.name)

db.define_table('char_sins', Field('char', type='reference chars', label=T('Character'), writable=False),
                Field('name', type='string', label=T('SIN Name')), Field('rating', type='integer', label=T('Rating')),
                Field('permits', type='string', label=T('Permits'), requires=IS_IN_SET(data.permits_dict.keys())),
                Field('locations', type='list:reference char_locations', label=T('Locations')),
                Field('money', type='float', label='Money'))