# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    is_default_bom = fields.Boolean(string="Default BOM", default=False)
    is_hidden_component = fields.Boolean(string="Hidden Component", default=False)
    is_child_line = fields.Boolean(compute="_compute_is_child_line", default=False)
    lst_price = fields.Float(compute="_compute_lst_price", string="Sale Price", digits=dp.get_precision('Product Price'))

    @api.multi
    @api.depends('product_id')
    def _compute_is_child_line(self):
        for line in self:
            line.is_child_line = not bool(line.product_id.bom_ids)

    @api.multi
    @api.depends('product_id', 'product_qty')
    def _compute_lst_price(self):
        for line in self:
            line.lst_price = line.product_id.lst_price * line.product_qty

MrpBomLine()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
