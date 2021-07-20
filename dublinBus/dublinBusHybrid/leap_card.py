from pyleapcard import *
from pprint import pprint

def leap_info(username,password):
    try:
        session = LeapSession()
        session.try_login(username,password)
        overview = session.get_card_overview()
        pprint(vars(overview))
        return overview
    except Exception as E:
        print(E)