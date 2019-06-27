#!/usr/bin/env python
# coding: utf-8

from odooApiConector import odooApiConector
from odooCsvReader import odooCsvReader

class odooPartnerImporter():

    def __init__(self):
        self.odooApiConector = odooApiConector( 'product.template' )
        self.odooApiConector.database = 'db_name'
        self.odooApiConector.host = 'host_ip'
        self.odooApiConector.user = 'odoo_user'
        self.odooApiConector.password = 'odoo_passwd'
        self.odooCsvReader = odooCsvReader()
        self.odooCsvReader.file = 'archivo.csv'

        self.odooApiConectorPartner = odooApiConector( 'res.partner' )
        self.odooApiConectorPartner.database = 'db_name'
        self.odooApiConectorPartner.host = 'host_ip'
        self.odooApiConectorPartner.user = 'odoo_user'
        self.odooApiConectorPartner.password = 'odoo_passwd'

        self.odoo_api_conector_product_supplier_info = odooApiConector( 'product.supplierinfo' )
        self.odoo_api_conector_product_supplier_info.database = 'db_name'
        self.odoo_api_conector_product_supplier_info.host = 'host_ip'
        self.odoo_api_conector_product_supplier_info.user = 'odoo_user'
        self.odoo_api_conector_product_supplier_info.password = 'odoo_passwd'

        self.odoo_api_conector_product_pricelist = odooApiConector('product.pricelist')
        self.odoo_api_conector_product_pricelist.database = 'db_name'
        self.odoo_api_conector_product_pricelist.host = 'host_ip'
        self.odoo_api_conector_product_pricelist.user = 'odoo_user'
        self.odoo_api_conector_product_pricelist.password = 'odoo_passwd'

        self.odoo_api_conector_product_pricelist_item = odooApiConector('product.pricelist.item')
        self.odoo_api_conector_product_pricelist_item.database = 'db_name'
        self.odoo_api_conector_product_pricelist_item.host = 'host_ip'
        self.odoo_api_conector_product_pricelist_item.user = 'odoo_user'
        self.odoo_api_conector_product_pricelist_item.password = 'odoo_passwd'

        self.odoo_api_conector_product_brand = odooApiConector('product.brand')
        self.odoo_api_conector_product_brand.database = 'db_name'
        self.odoo_api_conector_product_brand.host = 'host_ip'
        self.odoo_api_conector_product_brand.user = 'odoo_user'
        self.odoo_api_conector_product_brand.password = 'odoo_passwd'


    def run(self):
        if self.odooCsvReader.is_open_file:

            fields = self.odooCsvReader.convert_to_val_list()


            for field in fields:

                self.create_or_write_product(field)

                self.create_supplier(field)

                self.write_taxs(field)

                self.write_pricelist(field)

            self.odooCsvReader.close_file()


    def create_or_write_product(self, field):

        name = field.get('name')
        brand= field.get('product_brand_id')

        if brand !="":
            brand_id=self.odoo_api_conector_product_brand.search([[['description', '=', brand]]])

            field['product_brand_id']= brand_id[0]

        exists = self.odooApiConector.search_count([[['name', '=', name]]])

        if exists == 0:
            # print("No existe el producto")
            self.odooApiConector.create([field])
            #print(field)

        else:
            id = self.odooApiConector.search([[['name', '=', name]]])
            print(id)
            self.odooApiConector.write([id, field])
            # print("")

    def create_supplier(self, field):

        id_product = self.odooApiConector.search([[['name', '=', field.get('name')]]])

        if id_product == []:
            return

        referencia_proveedor_1 = field.get('referencia_proveedor_1')

        referencia_proveedor_2 = field.get('referencia_proveedor_2')

        id_proveedor_1 = self.odooApiConectorPartner.search([[['ref', '=', referencia_proveedor_1]]])

        id_proveedor_2 = self.odooApiConectorPartner.search([[['ref', '=', referencia_proveedor_2]]])

        if id_proveedor_1 != [] and self.odoo_api_conector_product_supplier_info.search_count([[['name', '=', id_proveedor_1 ],['product_tmpl_id', '=', id_product ]]]) == 0:

            id_relation = self.odoo_api_conector_product_supplier_info.create([
                {'name': id_proveedor_1[0],
                'product_tmpl_id': id_product[0]}])

            print("relación creada correctamente ", id_relation)

        if id_proveedor_2 != [] and self.odoo_api_conector_product_supplier_info.search_count([[['name', '=', id_proveedor_2], ['product_tmpl_id', '=', id_product]]]) == 0:

            id_relation = self.odoo_api_conector_product_supplier_info.create([
                {'name': id_proveedor_2[0],
                 'product_tmpl_id': id_product[0]}])

            print("relación creada correctamente ", id_relation)


    def write_taxs(self, field):
        id_product = self.odooApiConector.search([[['name', '=', field.get('name')]]])
        tax_id = field.get("tax_id")
        if tax_id != '':
            print(tax_id)
            self.odooApiConector.write([[id_product][0], {'taxes_id':[(6, 0, [tax_id])]}])
        # models.execute_kw(db, uid, password, 'res.partner', 'write', [[id], {'name': "Newer partner"}])

    def write_pricelist(self,field):

        id_product = self.odooApiConector.search([[['name', '=', field.get('name')]]])

        if id_product == []:
            return

        id_t_12 = self.odoo_api_conector_product_pricelist.search([[['name', '=', 'T-12']]])
        id_t_10 = self.odoo_api_conector_product_pricelist.search([[['name', '=', 'T-10']]])
        id_t_04 = self.odoo_api_conector_product_pricelist.search([[['name', '=', 'T-04']]])
        id_t_06 = self.odoo_api_conector_product_pricelist.search([[['name', '=', 'T-06']]])
        id_t_01 = self.odoo_api_conector_product_pricelist.search([[['name', '=', 'T-01']]])
        price_list_ids=[ {'tarifa':id_t_01[0], 'precio': field.get("T-01") },{ 'tarifa':id_t_12[0],'precio':field.get("T-12") }, {'tarifa': id_t_10[0],'precio': field.get("T-10")},{'tarifa': id_t_04[0],'precio': field.get("T-04")},{'tarifa': id_t_06[0], 'precio': field.get("T-06")} ]

        for pricelist in price_list_ids:
            print(pricelist)
            exist=self.odoo_api_conector_product_pricelist_item.search_count([[['product_tmpl_id', '=', id_product[0]],
                                                                               ['pricelist_id', '=', pricelist.get("tarifa")]]])
            if exist == 0:

                self.odoo_api_conector_product_pricelist_item.create([{'product_tmpl_id': id_product[0],
                                                                       'pricelist_id': pricelist.get("tarifa"),
                                                                       'fixed_price': pricelist.get("precio"), 'min_quantity': 1 }])

            if exist > 0:
                id_relacion=self.odoo_api_conector_product_pricelist_item.search([[['product_tmpl_id', '=', id_product[0]],
                                                                                   ['pricelist_id', '=', pricelist.get("tarifa")]]])
                self.odoo_api_conector_product_pricelist_item.write([id_relacion, {'fixed_price': pricelist.get("precio"), 'min_quantity': 1}])



# Iniciamos la clase --------------------------------------------------

odooPartnerImporter().run()







