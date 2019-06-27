#!/usr/bin/env python
# coding: utf-8

import xmlrpc.client

class odooApiConector:

    def __init__(self, model):
        self.__host = None
        self.__port = 8069
        self.__database = None
        self.__user = None
        self.__password = None
        self.__model = model

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, value):
        self.__database = value

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        self.__host = value

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        self.__user = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        self.__model = value

    @property
    def url(self):
        return 'http://%s:%d/xmlrpc/' % ( self.host, self.port )

    def common_end_point(self):
        return xmlrpc.client.ServerProxy( self.url + 'common' )

    def object_end_point(self):
        return xmlrpc.client.ServerProxy( self.url + 'object' )

    def userId(self):
        return self.common_end_point().login( self.database, self.user, self.password )

    def version(self):
        return self.common_end_point().version()

    def execute_kw_object_end_point(self, method, args, kwargs = {}):

        #print( "self.database")
        #print( self.database)

        #print( "self.userId")
        #print( self.userId())

        #print( "self.password")
        #print( self.password)

        #print("self.url")
        #print(self.url)

        #print("self.model")
        #print(self.model)

        #print("args")
        #print(args)

        #print("kwargs")
        #print(kwargs)

        return self.object_end_point().execute_kw( self.database, self.userId(), self.password, self.model, method, args, kwargs )

    def is_access_rights(self):
        return self.execute_kw_object_end_point( 'check_access_rights', ['read'], {'raise_exception': False} )

    def search(self, filter, attributes = {}):
        return self.execute_kw_object_end_point( 'search', filter, attributes )

    def search_count(self, filter):
        return self.execute_kw_object_end_point( 'search_count', filter )

    def fields_get(self, attributes = ['string', 'help', 'type']):
        return self.execute_kw_object_end_point( 'fields_get', [], {'attributes': attributes} )

    def read(self, ids):
        return self.execute_kw_object_end_point( 'read', ids )

    def search_read(self, filter, attributes = {}):
        return self.execute_kw_object_end_point( 'search_read', filter, attributes )

    def create(self, valsList = []):
        print("creating")
        print(valsList)
        return self.execute_kw_object_end_point( 'create', valsList )

    def write(self, valsList = []):
        print("updating")
        print(valsList)
        return self.execute_kw_object_end_point( 'write', valsList )

    def write_by_id(self, id, valsList = []):
        return self.write( [ [id], valsList ] )

    def unlink(self, ids):
        return self.execute_kw_object_end_point( 'unlink', ids )
