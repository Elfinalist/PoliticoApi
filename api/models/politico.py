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
            raise InputError('name is required when creating a political party')
        
        if(hq is None or len(hq) == 0):
            raise InputError('hq is requred when creating a political party')

        #logo url can be empty
        if(logo_url is None):
            logo_url = ""
        
        self.party_id_count += 1
        new_party = PoliticalParty(self.party_id_count, name, hq, logo_url)
        self.political_parties.append(new_party)
        return new_party
    
    def edit_political_party(self, id, name):
        party = self.get_political_party(id)
        if(len(party)):
            party_index = self.political_parties.index(party)
            self.political_parties[party_index]["name"] = name
            return {
                "id": party["id"],
                "name": name
            }
        else:
            raise InputError('party not found')

    def get_political_parties(self):
        if self.party_id_count > 0:
            return self.political_parties

    def get_political_party(self, id):
        for party in self.political_parties:
            if party["id"] == id:
                return party 
        return []
        
    def delete_political_party(self,id):
        party = self.get_political_party(id)
        if (len(party) == 0):
            return False
        self.political_parties.remove(party)
        return True

    def create_political_office(self, name, office_type):
        if name is None or len(name) == 0:
            raise InputError ('name is required when creating a political office')
        if office_type is None or len(office_type) == 0:
            raise InputError ('type is required when creating a political office')

        self.office_id_count += 1
        new_office = PoliticalOffice(self.office_id_count, name, office_type)
        self.political_offices.append(new_office)
        return new_office

    def get_political_offices(self):
        if self.office_id_count > 0:
            return self.political_offices

    def get_political_office(self, id):
        for office in self.political_offices:
            if office["id"] == id:
                return office
        return []

    def delete_political_office(self,id):
        office = self.get_political_office(id)
        if (len(office) == 0):
            return False
        self.political_offices.remove(office)
        return True
    
    def edit_political_office(self, id, name):
        office = self.get_political_office(id)
        if(len(office)):
            office_index = self.political_offices.index(office)
            self.political_offices[office_index]["name"] = name
            return {
                "id": office["id"],
                "name": name
            }
        else:
            raise InputError('office not found')

    def create_user(self, name, email, password, c_password):
        if name is None or len(name) == 0:
            raise InputError ('name is required when creating a user')
        
        if email is None or len(email) == 0:
            raise InputError ('email address is required when creating a user')
        
        if password is None or len(password) < 6:
            raise InputError ('password is required when creating a user and must be at least 6 characters long')
        
        if c_password != password:
            raise InputError ("passwords don't match")
        user = User.get_user_by_email(email)
        if user is None:
            user = User.save_user(name, email, password)
            return user
        else:
            raise InputError('email address already taken')

    def login(self, email, password):
        if email is None or len(email) == 0:
            raise InputError ('email address is required when logging in')
        
        if password is None:
            raise InputError ('password is required when logging in')

        user = User.login(email, password)
        return user
