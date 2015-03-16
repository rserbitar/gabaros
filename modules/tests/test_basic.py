import pytest
import basic
import data

@pytest.fixture()
def db():

    class DBFunc():

        def generic(self, *args, **kwargs):
            pass

        def __getattr__(self, generic):
            return self.generic

    class DB(object):

        def generic(self, *args, **kwargs):
            pass

        def __getattr__(self, generic):
            self.db = DBFunc()
            return self.db

    db = DB()
    return db

@pytest.fixture(params = ['base', 'unaugmented', 'augmented', 'temporary', 'stateful'])
def modlevel(request):
    return request.param

@pytest.fixture(params = data.attributes_dict.keys())
def attribute(request):
    return request.param


@pytest.fixture()
def load_char(charname = 'Testman', gender = 'Male', race = 'Human'):

    def load_char(self):
        self.name = charname
        self.gender = gender
        self.race = race
        char_property_getter = basic.CharPropertyGetter(self, 'base')
        for attribute in data.attributes_dict.keys():
            value = char_property_getter.get_attribute_value(attribute)
            self.attributes[attribute] = value

        for name, skill in data.skills_dict.items():
            self.skills[name] = 0


    return load_char


@pytest.fixture()
def char(db, load_char, monkeypatch):

    monkeypatch.setattr(basic.Char, 'load_char', load_char)

    char = basic.Char(db, None)

    char.init_attributes()
    char.init_skills()

    return char


class TestChar():

    def test_init(self, db, load_char, monkeypatch):

        monkeypatch.setattr(basic.Char, 'load_char', load_char)

        char = basic.Char(db, None)

        char.init_attributes()
        char.init_skills()

        assert char.name == 'Testman'
        print(char.attributes)


class Computer():

    def test_init(self):
        pass


class Weapons():

    def test_init(self):
        pass


class Armor():

    def test_init(self):
        pass


class Ware():

    def test_init(self):
        pass


class CharWare():

    def test_init(self):
        pass


class Body():

    def test_init(self):
        pass


class CharBody():

    def test_init(self):
        pass


class Bodypart():

    def test_init(self):
        pass


class CharBodyoart():

    def test_init(self):
        pass


class TestCharPropertyGetter():

    def test_init(self, char, modlevel):
        charpropertygetter = basic.CharPropertyGetter(char, modlevel)
        assert charpropertygetter

    def test_get_attribute(self, char, modlevel, attribute):
        charpropertygetter = basic.CharPropertyGetter(char, modlevel)
        value = charpropertygetter.get_attribute_value(attribute)
        assert value
