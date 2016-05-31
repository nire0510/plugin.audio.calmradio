import xbmc, sys
from api import API

api = API(None)

data = api.get_json(sys.argv[1])
xbmc.executebuiltin('SetProperty(BLA, "KUKU", {0})'.format(sys.argv[2]))
