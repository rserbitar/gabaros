# -*- coding: utf-8 -*-
# Versuchen Sie so etwas wie
def index(): return dict(message="hello from maintainance.py")

def add_skill():
    for row in db().select(db.chars.id):
        db['char_skills'].insert(**{"char": row.id, "skill": "Astral Combat", "value": 0.0})
