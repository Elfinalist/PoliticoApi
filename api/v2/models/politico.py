from api.v2.models.politicalparty import PoliticalParty
from api.v2.models.politicaloffice import PoliticalOffice
from api.v2.models.user import User
from api.v2.models.errors import InputError


class Politico():
    def __init__(self):
        self.party_id_count = 0
        self.political_parties = []
        self.office_id_count = 0
        self.political_offices = []

    def create_political_party(self, name, hq, logo_url):
        """Create A Political Party

        Keyword arguments:
        name      -- name of the political party (required)
        hq        -- political party headquarters (required)
        logo_url  -- image url for party logo (optional)
        """
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
        """Edit a political party

        Keyword arguments:
        id    -- id of the political party (required)
        name  -- new political party name (required)
        """
        party = PoliticalParty.update_political_party(id, name)
        if(party is not None):
            return {
                "id": party["id"],
                "name": name
            }
        else:
            raise InputError('party not found')

    def get_political_parties(self):
        """Get Political Parties

        Keyword arguments:
        """
        return PoliticalParty.get_political_parties()

    def get_political_party(self, id):
        """Get A Political Party

        Keyword arguments:
        id  -- the id of the party to get
        """
        party = PoliticalParty.get_party_by_id(id)
        if party is not None:
            return party
        return []

    def delete_political_party(self, id):
        """Delete A Political Party

        Keyword arguments:
        id  -- the id of the party to delete
        """
        party = PoliticalParty.delete_political_party(id)
        if (party is None):
            return False
        return True

    def create_political_office(self, name, office_type):
        """Create A Political Office

        Keyword arguments:
        name         -- name of the political office (required)
        office_type  -- type of political office (required)
        """
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
        """Get All Political Office

        Keyword arguments:
        """
        return PoliticalOffice.get_political_offices()

    def get_political_office(self, id):
        """Get A Political Office

        Keyword arguments:
        id -- office id of the political office to get
        """
        office = PoliticalOffice.get_office_by_id(id)
        if office is not None:
            return office
        return []

    def delete_political_office(self, id):
        """Delete A Political Office

        Keyword arguments:
        id -  office id of the political office to delete
        """
        office = PoliticalOffice.delete_political_office(id)
        if (office is None):
            return False
        return True

    def edit_political_office(self, id, name):
        """Edit A Political Office

        Keyword arguments:
        id -    office id of the political office to edit
        name -  new name of the political office to edit
        """
        office = PoliticalOffice.update_political_office(id, name)
        if(office is not None):
            return {
                "id": office["id"],
                "name": name
            }
        else:
            raise InputError('party not found')

    def create_user(self, name, email, password, c_password):
        """Create A Political Party

        Keyword arguments:
        name       -- name of the user (required)
        email      -- email of the user (required)
        password   -- password of the user (required)
        c_password -- repeat password to confirm match (required)
        """

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
        """User Login

        Keyword arguments:
        email      -- email of the user (required)
        password   -- password of the user (required)
        """
        if email is None or len(email) == 0:
            raise InputError('email address is required when logging in')

        if password is None:
            raise InputError('password is required when logging in')

        user = User.login(email, password)
        return user
