from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.

        Vorgabe: Aufrufnamen der einzelnen URLs sollten kleingeschrieben werden
    """


    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    
    config.add_route('home', '/')
    #config.add_route('mannschaften', '/mannschaften')
    config.add_route('ulMannschaften', '/ulmannschaften')

    config.add_route('optionBoxMannschaften', '/optionboxmannschaften')

    config.add_route('matchesfor', '/matchesfor/{mannschaft}')
    config.add_route('whoWillWin', '/whowillwin')
    config.add_route('compareTwoTeamsSeason', '/comparetwoteamsseason/{spieltag}/{heim}/{heimtore}/{heimgegentore}/{gast}/{gasttore}/{gastgegentore}')
    #config.add_route('compareTwoTeamsSeason', '/comparetwoteamsseason')
    
    config.scan()
    return config.make_wsgi_app()
