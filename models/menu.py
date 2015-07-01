# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
                  _class="navbar-brand",_href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), []),
      (T('Manage Char'), False, '#', [
          (T('Create/Select'), False, URL('gabaros', 'manage_char', 'index')),
          LI(_class="divider"),
          (T('Attributes'), False, URL('gabaros', 'manage_char', 'edit_attributes', args = [session.char])),
          (T('Skills'), False, URL('gabaros', 'manage_char', 'edit_skills', args = [session.char])),
          (T('Adept Powers'), False, URL('gabaros', 'manage_char', 'manage_powers', args = [session.char])),
          (T('Spells'), False, URL('gabaros', 'manage_char', 'manage_spells', args = [session.char])),
          (T('Ware'), False, URL('gabaros', 'manage_char', 'manage_ware', args = [session.char])),
          LI(_class="divider"),
          (T('Damage'), False, URL('gabaros', 'manage_char', 'edit_damage', args = [session.char])),
          (T('Wounds'), False, URL('gabaros', 'manage_char', 'edit_wounds', args = [session.char])),
          LI(_class="divider"),
          (T('Items'), False, URL('gabaros', 'manage_char', 'edit_items', args = [session.char])),
          (T('Loadout'), False, URL('gabaros', 'manage_char', 'edit_loadout', args = [session.char])),
          (T('Computers'), False, URL('gabaros', 'manage_char', 'edit_computers', args = [session.char])),
          (T('Sins'), False, URL('gabaros', 'manage_char', 'edit_sins', args = [session.char])),
          (T('Locations'), False, URL('gabaros', 'manage_char', 'edit_locations', args = [session.char])),
            ]),
      (T('View Char'), False, '#', [
          (T('Attributes'), False, URL('gabaros', 'view_char', 'view_attributes', args = [session.char])),
          (T('Stats'), False, URL('gabaros', 'view_char', 'view_stats', args = [session.char])),
          (T('Skills'), False, URL('gabaros', 'view_char', 'view_skills', args = [session.char])),
          (T('XP'), False, URL('gabaros', 'view_char', 'view_xp', args = [session.char])),
          (T('Cost'), False, URL('gabaros', 'view_char', 'view_cost', args = [session.char])),
          (T('Bodyparts'), False, URL('gabaros', 'view_char', 'view_bodyparts', args = [session.char])),
          (T('Actions'), False, URL('gabaros', 'view_char', 'view_actions', args = [session.char])),
          (T('Damage'), False, URL('gabaros', 'view_char', 'view_damage_state', args = [session.char])),
          (T('Weapons'), False, URL('gabaros', 'view_char', 'view_weapons', args = [session.char])),
          (T('Armor'), False, URL('gabaros', 'view_char', 'view_armor', args = [session.char])),
          (T('Computer'), False, URL('gabaros', 'view_char', 'view_computer', args = [session.char])),
          LI(_class="divider"),
          (T('Combat'), False, URL('gabaros', 'view_char', 'combat', args = [session.char])),
          (T('Apply Damage'), False, URL('gabaros', 'view_char', 'apply_damage', args = [session.char])),
            ]),
      (T('Gameinformation'), False, '#', [
          (T('Gametables'), False, URL('gabaros', 'game', 'gametables', args = [session.char])),
          ]),
]

DEVELOPMENT_MENU = False

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu += [
        (T('My Sites'), False, URL('admin', 'default', 'site')),
          (T('This App'), False, '#', [
              (T('Design'), False, URL('admin', 'default', 'design/%s' % app)),
              LI(_class="divider"),
              (T('Controller'), False,
               URL(
               'admin', 'default', 'edit/%s/controllers/%s.py' % (app, ctr))),
              (T('View'), False,
               URL(
               'admin', 'default', 'edit/%s/views/%s' % (app, response.view))),
              (T('DB Model'), False,
               URL(
               'admin', 'default', 'edit/%s/models/db.py' % app)),
              (T('Menu Model'), False,
               URL(
               'admin', 'default', 'edit/%s/models/menu.py' % app)),
              (T('Config.ini'), False,
               URL(
               'admin', 'default', 'edit/%s/private/appconfig.ini' % app)),
              (T('Layout'), False,
               URL(
               'admin', 'default', 'edit/%s/views/layout.html' % app)),
              (T('Stylesheet'), False,
               URL(
               'admin', 'default', 'edit/%s/static/css/web2py-bootstrap3.css' % app)),
              (T('Database'), False, URL(app, 'appadmin', 'index')),
              (T('Errors'), False, URL(
               'admin', 'default', 'errors/' + app)),
              (T('About'), False, URL(
               'admin', 'default', 'about/' + app)),
              ]),
          ('web2py.com', False, '#', [
             (T('Download'), False,
              'http://www.web2py.com/examples/default/download'),
             (T('Support'), False,
              'http://www.web2py.com/examples/default/support'),
             (T('Demo'), False, 'http://web2py.com/demo_admin'),
             (T('Quick Examples'), False,
              'http://web2py.com/examples/default/examples'),
             (T('FAQ'), False, 'http://web2py.com/AlterEgo'),
             (T('Videos'), False,
              'http://www.web2py.com/examples/default/videos/'),
             (T('Free Applications'),
              False, 'http://web2py.com/appliances'),
             (T('Plugins'), False, 'http://web2py.com/plugins'),
             (T('Recipes'), False, 'http://web2pyslices.com/'),
             ]),
          (T('Documentation'), False, '#', [
             (T('Online book'), False, 'http://www.web2py.com/book'),
             LI(_class="divider"),
             (T('Preface'), False,
              'http://www.web2py.com/book/default/chapter/00'),
             (T('Introduction'), False,
              'http://www.web2py.com/book/default/chapter/01'),
             (T('Python'), False,
              'http://www.web2py.com/book/default/chapter/02'),
             (T('Overview'), False,
              'http://www.web2py.com/book/default/chapter/03'),
             (T('The Core'), False,
              'http://www.web2py.com/book/default/chapter/04'),
             (T('The Views'), False,
              'http://www.web2py.com/book/default/chapter/05'),
             (T('Database'), False,
              'http://www.web2py.com/book/default/chapter/06'),
             (T('Forms and Validators'), False,
              'http://www.web2py.com/book/default/chapter/07'),
             (T('Email and SMS'), False,
              'http://www.web2py.com/book/default/chapter/08'),
             (T('Access Control'), False,
              'http://www.web2py.com/book/default/chapter/09'),
             (T('Services'), False,
              'http://www.web2py.com/book/default/chapter/10'),
             (T('Ajax Recipes'), False,
              'http://www.web2py.com/book/default/chapter/11'),
             (T('Components and Plugins'), False,
              'http://www.web2py.com/book/default/chapter/12'),
             (T('Deployment Recipes'), False,
              'http://www.web2py.com/book/default/chapter/13'),
             (T('Other Recipes'), False,
              'http://www.web2py.com/book/default/chapter/14'),
             (T('Helping web2py'), False,
              'http://www.web2py.com/book/default/chapter/15'),
             (T("Buy web2py's book"), False,
              'http://stores.lulu.com/web2py'),
             ]),
          (T('Community'), False, None, [
             (T('Groups'), False,
              'http://www.web2py.com/examples/default/usergroups'),
              (T('Twitter'), False, 'http://twitter.com/web2py'),
              (T('Live Chat'), False,
               'http://webchat.freenode.net/?channels=web2py'),
              ]),
        ]
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu()
