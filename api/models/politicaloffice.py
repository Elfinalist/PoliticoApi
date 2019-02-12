class PoliticalOffice(dict):
    def __init__(self, id, name, office_type):
        self["id"] = id
        self["name"] = name
        self["office_type"] = office_type
