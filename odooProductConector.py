#!/usr/bin/env python
# coding: utf-8

import xmlrpc.client
from odooApiConector import odooApiConector

class odooPartnerConector(odooApiConector):

    def __init__(self):
        super().__init__('res.partner')

    def searchActiveCustomers(self):
        return self.search( [[['active', '=', True], ['customer', '=', True]]] )

    def firstActiveCustomers(self):
        return self.search( [[['active', '=', True], ['customer', '=', True]]], {'limit': 1} )

    def searchCountActiveCustomers(self):
        return self.searchCount( [[['active', '=', True], ['customer', '=', True]]] )

    def searchReadActiveCustomers(self):
        return self.searchRead( [[['active', '=', True], ['customer', '=', True]]], {'fields': ['name', 'country_id', 'comment'], 'limit': 5} )
