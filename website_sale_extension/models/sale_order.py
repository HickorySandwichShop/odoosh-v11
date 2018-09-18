# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, attributes=None, **kwargs):
        res = super(SaleOrder, self)._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, attributes=attributes, **kwargs)

        line_id = res.get('line_id', 0)
        order_line = self.order_line.filtered(lambda line: line.id == line_id)
        bom_line_str = kwargs.get('bom_line_ids', False)
        if bom_line_str and order_line:
            bom_line_ids = [int(id) for id in bom_line_str.split(',')]
            order_line.write({'bom_line_ids': [(6,False, bom_line_ids)]})
            order_line._compute_amount()
            self._amount_all()

        return res


SaleOrder()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    bom_line_ids = fields.Many2many('mrp.bom.line', string="BOM products")
    bom_price = fields.Monetary(compute='_compute_bom_price', string='BOM Price')

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        super(SaleOrderLine, self)._compute_amount()
        for line in self:
            price = (line.price_unit + line.bom_price) * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    @api.multi
    @api.depends('bom_line_ids')
    def _compute_bom_price(self):
        for line in self:
            bom_price = sum(line.bom_line_ids.mapped('lst_price'))
            line.bom_price = bom_price


SaleOrderLine()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
