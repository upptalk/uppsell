#-*- coding: utf-8 -*-
"""
@author:        Adam Hayward
@contact:       adam@happy.cat
"""
from uppsell.models import Urn
from django.test import TestCase

class UrnTestCase(TestCase):
    
    def test_nsid(self):
        urn = Urn("urn:ylp:abc:a:b:c:d")
        self.assertEqual("ylp", urn.nsid)

    def test_nssid(self):
        urn = Urn("urn:ylp:abc:a:b:c:d")
        self.assertEqual("abc", urn.nssid)
    
    def test_kv(self):
        urn = Urn("urn:ylp:abc:a:b:c:d")
        self.assertEqual("b", urn['a'])
        self.assertEqual("d", urn['c'])
        self.assertEqual(None, urn['z'])

    def test_nokv(self):
        as_str = "urn:ylp:abc"
        urn = Urn(as_str)
        self.assertEqual(as_str, str(urn))

