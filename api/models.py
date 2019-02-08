class InputError(Exception):
    def __init__(self, message):
        self.message = message

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
        if self.party_id_count > 0:
            return self.political_offices

    








class PoliticalParty(dict):
    def __init__(self, id, name, hq, logo_url):
        self["id"] = id
        self["name"] = name
        self["hq"] = hq
        self["logoUrl"] = logo_url

class PoliticalOffice(dict):
    def __init__(self, id, name, office_type):
        self["id"] = id
        self["name"] = name
        self["office_type"] = office_type
