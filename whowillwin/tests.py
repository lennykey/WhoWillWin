
# _*_ coding: utf-8 _*_
import unittest

from pyramid import testing
from views import mannschaften

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'whoWillWin')
        
    def testMannschaften(self):
        self.assertEqual(type( dict() ), type(mannschaften()), "Kein Dictionary zurueckgekommen")
        
    def testIstFCKoelnInDictionary(self):
        #print mannschaften()
        #print mannschaften().items()[0][1]
        
        #dieseMannschaften = []
        #for mannschaftListe in (mannschaften().values()):
        #        for mannschaft in mannschaftListe:
        #            dieseMannschaften.append( str(mannschaft).encode("utf-8").decode("utf-8"))
                   
        #print dieseMannschaften 
        #print "1. FC Köln".encode("utf-8")
        #print "1. FC Köln".decode("utf-8")
            
        self.assertIn("1. FC Köln".decode("utf-8"), mannschaften().items()[0][1], "FC Augsburg nicht vorhanden")