from pyramid.view import view_config
from suds.client import Client
#from pyramid.response import Response
import logging

log = logging.getLogger(__name__)


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project':'whoWillWin'}

#@view_config(route_name='mannschaften', renderer='templates/mannschaften.pt')
def mannschaften():
    url = "http://www.OpenLigaDB.de/Webservices/Sportsdata.asmx?WSDL"
    client = Client(url)
    teams = client.service.GetTeamsByLeagueSaison( 'bl1', '2011' )

    teamNameList = []

    #logging.info(teams)
    #logging.info('First logger')
    #logging.info(str(teams))

    #print teams[0]
    
    #for team in teams.Team:
    #    print type(team)
    #    teamName = team.teamName

    #    teamNameList.append(teamName)


    for team in teams.Team:
        #print team.teamName
        teamNameList.append( team.teamName.encode('utf-8').decode('utf-8') )

    #result = []
    #result.append('<ul>')

    #for element in teamNameList:
    #    result.append('<li>' + element + '</li>')

    #result.append('</ul>')
   
    #return Response( 'Bundesliga Mannschaften ' + str (len( teamNameList ) ) + ' '  + ''.join( result ) ) 
    #return Response(str(result).decode('utf-8')) 
    return {'teams' : teamNameList }

@view_config(route_name='ulMannschaften', renderer='templates/ulMannschaften.pt')
def ulMannschaften(request):
    return mannschaften() 

@view_config(route_name='optionBoxMannschaften', renderer='templates/optionBoxMannschaften.pt')
def optionBoxMannschaften(request):
    return mannschaften() 


def getMatchesForTeam(mannschaft):
    url = 'http://www.openligadb.de/Webservices/Sportsdata.asmx?WSDL'
    client = Client(url)
    alleSpiele = client.service.GetMatchdataByLeagueSaison('bl1', '2011')

    gesuchteMannschaft = mannschaft 
    gesuchteMannschaftTore = 0
    gesuchteMannschaftGegentore = 0
    
    mannschaftsSpiele = [] 

    for match in alleSpiele.Matchdata:
        if match.nameTeam1 == gesuchteMannschaft or match.nameTeam2 == gesuchteMannschaft:
            mannschaftsSpiele.append(match)
            log.debug(match.nameTeam1)
            log.debug(match.nameTeam2)
            
    result = []
    
    #result.append('<ul>')
    
    for begegnung in mannschaftsSpiele:
    #print type(begegnung)
    #print begegnung
    #print unicode(begegnung.nameTeam1)
    #print begegnung.nameTeam2
        #print begegnung.matchResults 

        if(begegnung.nameTeam1 == gesuchteMannschaft and (begegnung.pointsTeam1 >= 0 and begegnung.pointsTeam2 >= 0) ):
            gesuchteMannschaftTore += begegnung.pointsTeam1 
            gesuchteMannschaftGegentore += begegnung.pointsTeam2
        elif(begegnung.nameTeam2 == gesuchteMannschaft and (begegnung.pointsTeam1 >= 0 and begegnung.pointsTeam2 >= 0) ):
            gesuchteMannschaftTore += begegnung.pointsTeam2
            gesuchteMannschaftGegentore += begegnung.pointsTeam1
        
    #print 'Tore: ' + str( gesuchteMannschaftTore )
    #print 'Gegentore: ' + str( gesuchteMannschaftGegentore )

    #dict = {unicode(str(begegnung.nameTeam1)) : unicode(str(begegnung.pointsTeam1)), unicode(str(begegnung.nameTeam2)) : unicode(str(begegnung.pointsTeam2)) }
    #dict = {str(begegnung.nameTeam1).decode('utf-8') : str(begegnung.pointsTeam1).decode('utf-8'), str(begegnung.nameTeam2).decode('utf-8') : str(begegnung.pointsTeam2).decode('utf-8') }


    #print type(begegnung.nameTeam1)	

        mydict = { (begegnung.nameTeam1).encode('utf-8').decode('utf-8') : str(begegnung.pointsTeam1).encode('utf-8').decode('utf-8'), (begegnung.nameTeam2).encode('utf-8').decode('utf-8') : str(begegnung.pointsTeam2).encode('utf-8').decode('utf-8') }
        result.append( mydict  )

        #print mydict
    
    #result.append('</ul>')
    #print alleSpiele

    returnDict  = {'GesuchteMannschaft': gesuchteMannschaft , 'Tore': str(gesuchteMannschaftTore), 'Gegentore': str(gesuchteMannschaftGegentore), 'Spiele':  result   }
    
    #print str((returnDict['Spiele'][3]).keys()[0]).decode('utf-8', 'replace') 

    #return {'project': 'cool'}
    return returnDict  
    #return str( list(returnDict.values()[3][3])[0] )
    #return Response( 'Bundesliga Spiele:\n ' +
#		'\nAnzahl Tore: ' + str(gesuchteMannschaftTore) +		
#		'\nAnzahl Gegentore: ' + str(gesuchteMannschaftGegentore) +		
#		''.join( result )
#		) 

@view_config(route_name='matchesfor', renderer='templates/getmatches.pt')
def getMatches(request):
    mannschaft = request.matchdict['mannschaft']
    return getMatchesForTeam(mannschaft)

@view_config(route_name='whoWillWin', renderer='templates/whowillwin.pt')
def whoWillWin(request):
    #print "def whoWillWin"
    return {'whowillwin':'you'} 

@view_config(route_name='compareTwoTeamsSeason', renderer='templates/compareTwoTeamsSeason.pt')
def compareTwoTeamsSeason(request):
    #heimErgebnis = ( float( request.matchdict['heimtore'] ) / float (request.matchdict['gastgegentore'] ) ) * ( float (request.matchdict['heimtore'] ) / float( request.matchdict['spieltag'] ) )    
    
    #gastErgebnis = ( float( request.matchdict['gasttore'] ) / float (request.matchdict['heimgegentore'] ) ) * ( float (request.matchdict['gasttore'] ) / float( request.matchdict['spieltag'] ) )    
    
    heimErgebnis = ( ( float( request.matchdict['heimtore'] ) / float( request.matchdict['spieltag'] ) ) + float( request.matchdict['gastgegentore'] ) / float( request.matchdict['spieltag'] ) ) / 2 
    
    gastErgebnis = ( ( float( request.matchdict['gasttore'] ) / float( request.matchdict['spieltag'] ) ) + float( request.matchdict['heimgegentore'] ) / float( request.matchdict['spieltag'] ) ) / 2 


    return {'heimmannschaft' : request.matchdict['heim'], 'heimErgebnis': int( round(heimErgebnis) ), 'gastmannschaft': request.matchdict['gast']  , 'gastErgebnis' : int( round(gastErgebnis) ) } 




