#!/usr/bin/env python
# coding: utf-8

import csv
import json

class odooCsvReader():

    def __init__(self):
        self.__file = None
        self.__file_handle = None

    @property
    def file(self):
        return self.__file

    @file.setter
    def file(self, value):
        self.__file = value

    @property
    def is_open_file(self):
        try:
            self.__file_handle = open( self.file )
            return True
        except IOError:
            print( "Error: can\'t find file or read data" )
        return False

    def close_file(self):
        self.__file_handle.close()

    def csv_reader(self):
        return ( csv.reader( self.__file_handle, delimiter = ';' ) )

    def csv_dict_reader(self):
        return ( csv.DictReader( self.__file_handle, delimiter = ';', fieldnames = self.get_header() ) )

    def convert_to_val_list(self):
        val_list = []
        field_names = self.csv_dict_reader()

        for field in field_names:
            element= {}

            for f in field:
                element.update( { f:field[ f ] })

            val_list.append( element )

        return ( val_list )

    def get_header(self):

        field_names = ['default_code','name', 'sale_ok','weight', 'volume', 'type', 'product_brand_id','referencia_proveedor_1','referencia_proveedor_2','standard_price', 'tax_id', 'T-12','T-10','T-04','T-06','T-01']

        return ( field_names )




