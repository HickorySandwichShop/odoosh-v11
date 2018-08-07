# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    bom_ids = fields.One2many('mrp.bom', 'product_tmpl_id', 'Bill of Materials', copy=True)
    attribute_line_ids = fields.One2many('product.attribute.line', 'product_tmpl_id', 'Product Attributes', copy=True)

    @api.one
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        res = super(ProductTemplate, self).copy(default)
        for variant in self.product_variant_ids:
            variant.copy(default={'product_tmpl_id':res.id, 'default_code': False, 'barcode': False})
        return res

ProductTemplate()
