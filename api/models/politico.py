from api.models.politicalparty import PoliticalParty
from api.models.politicaloffice import PoliticalOffice
from api.models.user import User
from api.models.errors import InputError


class Politico():
    def __init__(self):
        self.party_id_count = 0
        self.political_parties = []
        self.office_id_count = 0
        self.political_offices = []

    def create_political_party(self, name, hq, logo_url):
        if(name is None or len(name) == 0):
            raise InputError(
                'name is required when creating a political party')

        if(hq is None or len(hq) == 0):
            raise InputError('hq is requred when creating a political party')

        # logo url can be empty
        if(logo_url is None):
            logo_url = ""

        party = PoliticalParty.get_party_by_name(name)
        if party is None:
            new_party = PoliticalParty.save_party(name, hq, logo_url)
            return new_party
        else:
            raise InputError('party name is already registered')

    def edit_political_party(self, id, name):
        party = PoliticalParty.update_political_party(id, name)
        if(party is not None):
            return {
                "id": party["id"],
                "name": name
            }
        else:
            raise InputError('party not found')

    def get_political_parties(self):
        return PoliticalParty.get_political_parties()

    def get_political_party(self, id):
        party = PoliticalParty.get_party_by_id(id)
        if party is not None:
            return party
        return []

    def delete_political_party(self, id):
        party = PoliticalParty.delete_political_party(id)
        if (party is None):
            return False
        return True

    def create_political_office(self, name, office_type):
        if name is None or len(name) == 0:
            raise InputError(
                'name is required when creating a political office')
        if office_type is None or len(office_type) == 0:
            raise InputError(
                'type is required when creating a political office')

        office = PoliticalOffice.get_office_by_name(name)
        if office is None:
            office = PoliticalOffice.save_office(name, office_type)
            return office
        else:
            raise InputError('office name is already registered')

    def get_political_offices(self):
        return PoliticalOffice.get_political_offices()

    def get_political_office(self, id):
        office = PoliticalOffice.get_office_by_id(id)
        if office is not None:
            return office
        return []

    def delete_political_office(self, id):
        office = PoliticalOffice.delete_political_office(id)
        if (office is None):
            return False
        return True

    def edit_political_office(self, id, name):
        office = PoliticalOffice.update_political_office(id, name)
        if(office is not None):
            return {
                "id": office["id"],
                "name": name
            }
        else:
            raise InputError('party not found')

    def create_user(self, name, email, password, c_password):
        if name is None or len(name) == 0:
            raise InputError('name is required when creating a user')

        if email is None or len(email) == 0:
            raise InputError('email address is required when creating a user')

        if password is None or len(password) < 6:
            raise InputError(
                'password is required when creating a user and must be at least 6 characters long')

        if c_password != password:
            raise InputError("passwords don't match")
        user = User.get_user_by_email(email)
        if user is None:
            user = User.save_user(name, email, password)
            return user
        else:
            raise InputError('email address already taken')

    def login(self, email, password):
        if email is None or len(email) == 0:
            raise InputError('email address is required when logging in')

        if password is None:
            raise InputError('password is required when logging in')

        user = User.login(email, password)
        return user
