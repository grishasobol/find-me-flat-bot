import googlemaps
from datetime import datetime

DEFAULT_TIME = datetime(2020, 1, 9, 9, 0, 0, 0)

class GoogleAPI:
    def __init__( self, key ):
        self.key = key
        self.gmaps = googlemaps.Client( key=key )

    def get_travel_time( self, origin, destin, mode='transit', dep_time=DEFAULT_TIME):
        directions_result = gmaps.directions( origin,
                                              destin,
                                              mode=mode,
                                              departure_time=dep_time)
        return directions_result[0]['legs'][0]['duration']['value']
