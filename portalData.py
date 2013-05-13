import requests, xmltodict, json

class PortalData:

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def get_geonames(self):
        geonames_url = 'http://api.geonames.org/extendedFindNearby?lat='+self.latitude+'&lng='+self.longitude+'&username=ondrae'
        response = requests.get(geonames_url)
        geonames = xmltodict.parse(response.text)
        self.city_name = geonames['geonames']['address']['placename']
        self.county_name = geonames['geonames']['address']['adminName2']
        self.state_code = geonames['geonames']['address']['adminCode1']
        self.state_name = geonames['geonames']['address']['adminName1']
        self.country_code = geonames['geonames']['address']['countryCode']

    def get_portals(self):
        self.city_state_country = self.city_name + ', ' + self.state_name + ', ' + self.country_code
        self.county_state_country = self.county_name + ', ' + self.state_name + ', ' + self.country_code
        self.state_country = self.state_name + ', ' + self.country_code
        response = requests.get('https://raw.github.com/ondrae/portalportal/testing/static/data/portals.json')
        portals = response.json()
        self.city_portal = portals['city'][self.city_state_country]
        self.county_portal = portals['county'][self.county_state_country]
        self.state_portal = portals['state'][self.state_country]
        self.country_portal = portals['country'][self.country_code]

    def build_response(self):
        self.res = {}
        self.res["country"] = {"name" : self.country_code, "data_portal_url" : self.country_portal}
        self.res["state"] = {"name" : self.state_name, "data_portal_url" : self.state_portal}
        self.res["county"] = {"name" : self.county_name, "data_portal_url" : self.county_portal}
        self.res["city"] = {"name" : self.city_name, "data_portal_url" : self.city_portal}