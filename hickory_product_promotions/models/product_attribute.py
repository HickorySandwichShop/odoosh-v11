# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    is_show_website = fields.Boolean(string="Show in website", default=True)
