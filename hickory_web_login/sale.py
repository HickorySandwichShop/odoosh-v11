from odoo import models, fields, registry, api,_


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    release_date = fields.Date(string="Release Date")


SaleOrder()
