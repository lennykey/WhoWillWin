"""
View des whowillwin Tipgenerators
"""

from pyramid.view import view_config
from suds.client import Client
from whowillwin.Team import Team
from whowillwin.ArrayOfTeam import ArrayOfTeam
from whowillwin.Group import Group


import logging
import datetime

LOG = logging.getLogger(__name__)


def aktuelle_saison():
    """
    Gibt das Jahr zurueck, in der die aktuelle Saision gestartet ist
    """
    
    current = datetime.datetime.now()
    year = current.year
    month = current.month

    if(month < 7):
        year = year - 1

    LOG.debug("Aktuelles Jahr: %s" % year)
    LOG.debug("Aktueller Monat: %s" % month)
    return year

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    """
    """
    return {'project':'whoWillWin'}

def openLigaWSDLUrl():
    url = "http://www.OpenLigaDB.de/Webservices/Sportsdata.asmx?WSDL"
    return url

def bundesligaMannschaftenOpenLigaDB():
    year = aktuelle_saison()
    client = Client(openLigaWSDLUrl())
    return client.service.GetTeamsByLeagueSaison('bl1', year)

def mannschaften(client):
    teams = ArrayOfTeam(client.Team)

    teamNameList = []
    teamList = []
    
    for team in teams.Team:
        thisTeam = Team(team.teamID, team.teamName, team.teamIconURL)
        teamList.append(thisTeam)
        
    for team in teamList:
        teamNameList.append( team.teamName )


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
    year = aktuelle_saison()
    alleSpiele = client.service.GetMatchdataByLeagueSaison('bl1', year)

    gesuchteMannschaft = mannschaft 
    gesuchteMannschaftTore = 0
    gesuchteMannschaftGegentore = 0
    
    mannschaftsSpiele = [] 

    for match in alleSpiele.Matchdata:
        if match.nameTeam1 == gesuchteMannschaft or match.nameTeam2 == gesuchteMannschaft:
            mannschaftsSpiele.append(match)
            LOG.debug(match.nameTeam1)
            LOG.debug(match.nameTeam2)
            
    result = []
    
    
    for begegnung in mannschaftsSpiele:

        if(begegnung.nameTeam1 == gesuchteMannschaft and (begegnung.pointsTeam1 >= 0 and begegnung.pointsTeam2 >= 0) ):
            gesuchteMannschaftTore += begegnung.pointsTeam1 
            gesuchteMannschaftGegentore += begegnung.pointsTeam2
        elif(begegnung.nameTeam2 == gesuchteMannschaft and (begegnung.pointsTeam1 >= 0 and begegnung.pointsTeam2 >= 0) ):
            gesuchteMannschaftTore += begegnung.pointsTeam2
            gesuchteMannschaftGegentore += begegnung.pointsTeam1
        

        mydict = { (begegnung.nameTeam1).encode('utf-8').decode('utf-8') : str(begegnung.pointsTeam1).encode('utf-8').decode('utf-8'), (begegnung.nameTeam2).encode('utf-8').decode('utf-8') : str(begegnung.pointsTeam2).encode('utf-8').decode('utf-8') }
        result.append( mydict  )


    returnDict  = {'GesuchteMannschaft': gesuchteMannschaft , 'Tore': str(gesuchteMannschaftTore), 'Gegentore': str(gesuchteMannschaftGegentore), 'Spiele':  result   }
    
    return returnDict  


@view_config(route_name='matchesfor', renderer='templates/getmatches.pt')
def getMatches(request):
    mannschaft = request.matchdict['mannschaft']
    return getMatchesForTeam(mannschaft)

@view_config(route_name='whoWillWin', renderer='templates/whowillwin.pt')
def whoWillWin(request):
    group = currentgroup()
    aktuellerspieltag = aktuellerSpieltag(group)
    LOG.debug('Aktuelle Saison: %s' % aktuelle_saison())

    return {'whowillwin':'you', 'aktuellerSpieltag': aktuellerspieltag } 

@view_config(route_name='compareTwoTeamsSeason', renderer='templates/compareTwoTeamsSeason.pt')
def compareTwoTeamsSeason(request):
    heimErgebnis = ( ( float( request.matchdict['heimtore'] ) / float( request.matchdict['spieltag'] ) ) + float( request.matchdict['gastgegentore'] ) / float( request.matchdict['spieltag'] ) ) / 2 
    
    gastErgebnis = ( ( float( request.matchdict['gasttore'] ) / float( request.matchdict['spieltag'] ) ) + float( request.matchdict['heimgegentore'] ) / float( request.matchdict['spieltag'] ) ) / 2 

     
    return {'heimnotround': float(heimErgebnis), 'gastnotround' : float(gastErgebnis), 'heimmannschaft' : request.matchdict['heim'], 'heimErgebnis': int( round(heimErgebnis) ), 'gastmannschaft': request.matchdict['gast'] , 'gastErgebnis' : int( round(gastErgebnis) ) } 

def currentgroup(): 
    client = Client(openLigaWSDLUrl())
    currentGroup = client.service.GetCurrentGroup('bl1')
    LOG.debug(currentGroup)
    return currentGroup

def aktuellerSpieltag(group):
    group = Group(group.groupName, group.groupOrderID, group.groupID)
    LOG.debug(group.groupName)
    LOG.debug(group.groupOrderID)
    LOG.debug(group.groupID)
    return group.groupOrderID

