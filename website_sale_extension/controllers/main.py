# -*- coding: utf-8 -*-

import json

from odoo import http, tools
from odoo.http import request


class WebsiteSaleExtension(http.Controller):
    @http.route(['/shop/product/get_product_bom'], type='json', auth="public")
    def get_product_bom(self, product_id=None, **kw):
        vals = {}
        if product_id:
            product = request.env['product.product'].sudo().browse(product_id)
            vals['product'] = product
            vals['bom_lines'] = product.bom_ids.bom_line_ids

        return request.env['ir.ui.view'].render_template("website_sale_extension.product_bom_selector", vals)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
