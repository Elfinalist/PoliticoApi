class PoliticalParty(dict):
    def __init__(self, id, name, hq, logo_url):
        self["id"] = id
        self["name"] = name
        self["hq"] = hq
        self["logoUrl"] = logo_url