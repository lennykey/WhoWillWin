from pyramid.view import view_config
from suds.client import Client
from whowillwin.Team import Team
#from pyramid.response import Response
from whowillwin.ArrayOfTeam import ArrayOfTeam
from whowillwin.Group import Group


import logging
import datetime

log = logging.getLogger(__name__)


def aktuelleSaison():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    #month = 3

    if(month < 7):
        year = year - 1

    log.debug("Aktuelles Jahr: %s" % year)
    log.debug("Aktueller Monat: %s" % month)
    return year

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project':'whoWillWin'}
def openLigaWSDLUrl():
    url = "http://www.OpenLigaDB.de/Webservices/Sportsdata.asmx?WSDL"
    return url

def bundesligaMannschaftenOpenLigaDB():
    year = aktuelleSaison()
    client = Client(openLigaWSDLUrl())
    return client.service.GetTeamsByLeagueSaison('bl1', year)

#@view_config(route_name='mannschaften', renderer='templates/mannschaften.pt')
def mannschaften(client):
    #url = "http://www.OpenLigaDB.de/Webservices/Sportsdata.asmx?WSDL"
    #client = Client(url)
    #myClient = client
    teams = ArrayOfTeam(client.Team)

    teamNameList = []
    teamList = []
    
    for team in teams.Team:
        thisTeam = Team(team.teamID, team.teamName, team.teamIconURL)
        teamList.append(thisTeam)
        
    #logging.info(teams)
    #logging.info('First logger')
    #logging.info(str(teams))

    #print teams[0]
    
    #for team in teams.ArrayOfTeam:
    #    print type(team)
    #    teamName = team.teamName

    #    teamNameList.append(teamName)


    #for team in teams.ArrayOfTeam:
    for team in teamList:
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
    return mannschaften(bundesligaMannschaftenOpenLigaDB()) 

def getMatchesForTeam(mannschaft):
    '''
        Gibt die Spielbegegnungen fuer die uebergebene Mannschaft und Tore und Gegentore dieser
        zurueck
    '''
    url = 'http://www.openligadb.de/Webservices/Sportsdata.asmx?WSDL'
    client = Client(url)
    year = aktuelleSaison()
    alleSpiele = client.service.GetMatchdataByLeagueSaison('bl1', year)

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
    group = currentgroup()
    aktuellerspieltag = aktuellerSpieltag(group)
    log.debug('Aktuelle Saison: %s' % aktuelleSaison())
    #log.debug("Aktueller Spieltag %s" % aktuellerspieltag)
    #print "def whoWillWin"
    return {'whowillwin':'you', 'aktuellerSpieltag': aktuellerspieltag } 

@view_config(route_name='compareTwoTeamsSeason', renderer='templates/compareTwoTeamsSeason.pt')
def compareTwoTeamsSeason(request):
    #heimErgebnis = ( float( request.matchdict['heimtore'] ) / float (request.matchdict['gastgegentore'] ) ) * ( float (request.matchdict['heimtore'] ) / float( request.matchdict['spieltag'] ) )    
    
    #gastErgebnis = ( float( request.matchdict['gasttore'] ) / float (request.matchdict['heimgegentore'] ) ) * ( float (request.matchdict['gasttore'] ) / float( request.matchdict['spieltag'] ) )    
    
    heimErgebnis = ( ( float( request.matchdict['heimtore'] ) / float( request.matchdict['spieltag'] ) ) + float( request.matchdict['gastgegentore'] ) / float( request.matchdict['spieltag'] ) ) / 2 
    
    gastErgebnis = ( ( float( request.matchdict['gasttore'] ) / float( request.matchdict['spieltag'] ) ) + float( request.matchdict['heimgegentore'] ) / float( request.matchdict['spieltag'] ) ) / 2 

     
    return {'heimnotround': float(heimErgebnis), 'gastnotround' : float(gastErgebnis), 'heimmannschaft' : request.matchdict['heim'], 'heimErgebnis': int( round(heimErgebnis) ), 'gastmannschaft': request.matchdict['gast'] , 'gastErgebnis' : int( round(gastErgebnis) ) } 

def currentgroup(): 
    client = Client(openLigaWSDLUrl())
    currentGroup = client.service.GetCurrentGroup('bl1')
    log.debug(currentGroup)
    return currentGroup

def aktuellerSpieltag(group):
    group = Group(group.groupName, group.groupOrderID, group.groupID)
    #return group.groupName, group.groupID, group.groupOrderID
    log.debug(group.groupName)
    log.debug(group.groupOrderID)
    log.debug(group.groupID)
    return group.groupOrderID
