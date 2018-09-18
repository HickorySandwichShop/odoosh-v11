# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    bom_ids = fields.One2many('mrp.bom', 'product_id', 'Bill of Materials')


ProductProduct()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
