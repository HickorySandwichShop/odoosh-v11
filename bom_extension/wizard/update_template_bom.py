# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class UpdateTemplateBOM(models.Model):
    _name = "update.template.bom"

    product_ids = fields.Many2many('product.template', string='Products')

    @api.multi
    def add_boms(self):
        product_tmpl_id = self._context.get('product_tmpl_id')
        product_tmpl_id = self.env['product.template'].browse(product_tmpl_id)
        bom_id = False

        if not product_tmpl_id.bom_ids:
            product_bom_vals = {'product_tmpl_id': product_tmpl_id.id,
                                'product_qty': 1,
                                'product_uom_id': product_tmpl_id.uom_id.id,
                                'type': 'normal',
                                }
            bom_id = self.env['mrp.bom'].create(product_bom_vals)
        else:
            bom_id = product_tmpl_id.bom_ids[0]

        for product in self.product_ids:
            for bom in product.bom_ids:
                bom_line = {}
                for line in bom.bom_line_ids:
                    line.copy(default={'bom_id':bom_id.id})


UpdateTemplateBOM()
