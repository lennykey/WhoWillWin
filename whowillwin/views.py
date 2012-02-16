from pyramid.view import view_config
from suds.client import Client
from pyramid.response import Response

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project':'whoWillWin'}

@view_config(route_name='mannschaften', renderer='templates/mannschaften.pt')
def mannschaften(request):
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
        print team.teamName
        teamNameList.append( team.teamName.encode('utf-8').decode('utf-8') )

    result = []
    result.append('<ul>')

    for element in teamNameList:
        result.append('<li>' + element + '</li>')

    result.append('</ul>')
   
    #return Response( 'Bundesliga Mannschaften ' + str (len( teamNameList ) ) + ' '  + ''.join( result ) ) 
    #return Response(str(result).decode('utf-8')) 
    return {'teams' : teamNameList }

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
	elif(begegnung.nameTeam1 != gesuchteMannschaft and (begegnung.pointsTeam1 >= 0 and begegnung.pointsTeam2 >= 0) ):
	    gesuchteMannschaftTore += begegnung.pointsTeam2
	    gesuchteMannschaftGegentore += begegnung.pointsTeam1
	   
        #print 'Tore: ' + str( gesuchteMannschaftTore )
	#print 'Gegentore: ' + str( gesuchteMannschaftGegentore )

	#dict = {unicode(str(begegnung.nameTeam1)) : unicode(str(begegnung.pointsTeam1)), unicode(str(begegnung.nameTeam2)) : unicode(str(begegnung.pointsTeam2)) }
	
	#dict = {str(begegnung.nameTeam1).decode('utf-8') : str(begegnung.pointsTeam1).decode('utf-8'), str(begegnung.nameTeam2).decode('utf-8') : str(begegnung.pointsTeam2).decode('utf-8') }


	#print type(begegnung.nameTeam1)	

	dict = { (begegnung.nameTeam1).encode('utf-8').decode('utf-8') : str(begegnung.pointsTeam1).encode('utf-8').decode('utf-8'), (begegnung.nameTeam2).encode('utf-8').decode('utf-8') : str(begegnung.pointsTeam2).encode('utf-8').decode('utf-8') }
        result.append( dict  )

	
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

    return {'whowillwin':'you'} 

