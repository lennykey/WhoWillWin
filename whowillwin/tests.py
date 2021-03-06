
# _*_ coding: utf-8 _*_
import unittest

from pyramid import testing
from views import mannschaften
from whowillwin.views import bundesligaMannschaftenOpenLigaDB,\
    aktuellerSpieltag, currentgroup
from Team import Team
from whowillwin.ArrayOfTeam import ArrayOfTeam 
from whowillwin.Group import Group 

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        #Mocking WSDL Instance
        fca = Team(u"FCA", u"FCA", u"FCA")
        koeln = Team(u"1. FC Köln", u"1. FC Köln", u"1. FC Köln")
        munchen = Team(u"München", u"München", u"München")
        listeMannschaften = [fca, koeln, munchen]
        self.mockedTeams = ArrayOfTeam(listeMannschaften) 
        
    def tearDown(self):
        testing.tearDown()
        

    def test_my_view(self):
        from views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'whoWillWin')
        
    def testMannschaften(self):
        #client = bundesligaMannschaften2012OpenLigaDB()
        client = self.mockedTeams
        self.assertEqual(type( dict() ), type(mannschaften(client)), "Kein Dictionary zurueckgekommen")
        
    def testIstFCKoelnInDictionary(self):
        #print mannschaften(bundesligaMannschaften2012OpenLigaDB())
        #print mannschaften(bundesligaMannschaften2012OpenLigaDB()).items()[0][1]
        
        #dieseMannschaften = []
        #for mannschaftListe in (mannschaften().values()):
        #        for mannschaft in mannschaftListe:
        #            dieseMannschaften.append( str(mannschaft).encode("utf-8").decode("utf-8"))
                   
        #print dieseMannschaften 
        #print "1. FC Köln".encode("utf-8")
        #print "1. FC Köln".decode
        #listeMannschaften = {"mockedTeams" : ["FC Augsburg"]}
        #listeMannschaften = { ArrayOfTeam[] = (ArrayOfTeam){ teamID = 65 teamName = "1. FC Köln" teamIconURL = "http://www.openligadb.de/images/teamicons/1_FC_Koeln.gif" }}'
        #client = listeMannschaften 
        #fca = Team("FCA", "FCA", "FCA")
        #koeln = Team("1. FC Köln", "1. FC Köln", "1. FC Köln")
        #listeMannschaften = [fca, koeln]
        
        #mockedTeams = ArrayOfTeam(listeMannschaften) 
        #print listeMannschaften
        #client = bundesligaMannschaften2012OpenLigaDB() 
        
        client = self.mockedTeams
        #print type(client)
        #print client 
        #client = mannschaften
#        self.assertIn(u"1. FC Köln", mannschaften(client).items()[0][1], "1. FC Köln nicht vorhanden")
        self.assertIn("1. FC Köln".decode("utf-8"), mannschaften(client).items()[0][1], u"1. FC Köln nicht vorhanden")
        
    def IstFCKoelnInDictionaryWSDL(self):
        year = 2012
        client = bundesligaMannschaftenOpenLigaDB(year) 
        #print type(client)
        #print client 
        #client = mannschaften
        self.assertIn(u"1. FC Köln".decode("utf-8"), mannschaften(client).items()[0][1], u"1. FC Köln nicht vorhanden")   
        
    def AktuellerSpieltagWSDL(self):
        group = currentgroup()
        spieltag = aktuellerSpieltag(group)
        self.assertEqual(type(1), type(spieltag), u"Typ des Spieltags int ist nicht korrekt"  )   
    
    def testAktuellerSpieltagMocked(self):
        mockedGroup = Group("31. Spieltag",31, 265 )
        #group = group2011()
        self.assertEqual(type(1), type(mockedGroup.groupOrderID), u"Typ des Spieltags int ist nicht korrekt" )   
       
        
