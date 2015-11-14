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
response.meta.author = 'Serbitar <serbita@sessionmob.de>'
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
          (T('Create/Select'), False, URL('manage_char', 'index')),
          LI(_class="divider"),
          (T('XP'), False, URL('manage_char', 'manage_xp')),
          (T('Money'), False, URL('manage_char', 'manage_money')),
          LI(_class="divider"),
          (T('Attributes'), False, URL('manage_char', 'edit_attributes')),
          (T('Skills'), False, URL('manage_char', 'edit_skills')),
          LI(_class="divider"),
          (T('Adept Powers'), False, URL('manage_char', 'manage_powers')),
          (T('Spells'), False, URL('manage_char', 'manage_spells')),
          (T('Metamagic'), False, URL('manage_char', 'manage_metamagic')),
          LI(_class="divider"),
          (T('Ware'), False, URL('manage_char', 'manage_ware')),
          (T('Fixtures'), False, URL('manage_char', 'manage_fixtures')),
          LI(_class="divider"),
          (T('Damage'), False, URL('manage_char', 'edit_damage')),
          (T('Wounds'), False, URL('manage_char', 'edit_wounds')),
          LI(_class="divider"),
          (T('Items'), False, URL('manage_char', 'edit_items')),
          (T('Upgrades'), False, URL('manage_char', 'manage_upgrades')),
          (T('Loadout'), False, URL('manage_char', 'edit_loadout')),
          (T('Computers'), False, URL('manage_char', 'edit_computers')),
          (T('Sins'), False, URL('manage_char', 'edit_sins')),
          (T('Locations'), False, URL('manage_char', 'edit_locations')),
            ]),
      (T('View Char'), False, '#', [
          (T('Attributes'), False, URL('view_char', 'view_attributes')),
          (T('Stats'), False, URL('view_char', 'view_stats')),
          (T('Skills'), False, URL('view_char', 'view_skills')),
          (T('XP'), False, URL('view_char', 'view_xp')),
          (T('Cost'), False, URL('view_char', 'view_cost')),
          (T('Bodyparts'), False, URL('view_char', 'view_bodyparts')),
          (T('Actions'), False, URL('view_char', 'view_actions')),
          (T('Gear'), False, URL('view_char', 'view_items')),
          (T('Weapons'), False, URL('view_char', 'view_weapons')),
          (T('Armor'), False, URL('view_char', 'view_armor')),
          (T('Computer'), False, URL('view_char', 'view_computer')),
          LI(_class="divider"),
          (T('Combat'), False, URL('view_char', 'combat')),
          (T('Damage'), False, URL('view_char', 'damage')),
            ]),
      (T('Gameinformation'), False, '#', [
          (T('Wiki'), False, A('Wiki', _href='http://gabaros.sessionmob.de')),
          (T('Gametables'), False, URL('game', 'gametables')),
          ]),
      (T('Toggle Sidebar'), False, A('Toggle Sidebar', _href="#menu-toggle", _id="menu-toggle"), []),
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

def get_char():
    char = session.char
    if not db.chars[char] or (db.chars[char].player != auth.user.id
                              and db.chars[char].master != auth.user.id):
        redirect(URL(f='index'))
    return char

def get_char_name():
    name = ''
    char = session.char
    if char:
        name = db.chars[char].name
    return name

def wikify(links):
    baselink = 'http://gabaros.sessionmob.de'
    sidebar = [A('Wiki', _href=baselink, _target='_blank')]
    for link in links:
        sidebar.append(A(link, _href=baselink + '/index.php/' +link.replace(' ', '_'), _target='_blank'))
    return sidebar
