# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _
import itertools
import psycopg2
from odoo.exceptions import except_orm

class ProductTemplate(models.Model):

    _inherit = 'product.template'



    bom_ids = fields.One2many('mrp.bom', 'product_tmpl_id', 'Bill of Materials', copy=True)
    attribute_line_ids = fields.One2many('product.attribute.line', 'product_tmpl_id', 'Product Attributes', copy=True)




    @api.one
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        new_template = super(ProductTemplate, self).copy(default)
        existing_attr_combinations = [variant.attribute_value_ids for variant in self.product_variant_ids]
        variants_to_unlink = self.env['product.product']
        for product in new_template.product_variant_ids:
            flag = False
            for comb in existing_attr_combinations:
                if all([c.id in product.attribute_value_ids.ids for c in comb]):
                    flag = True
                    break
            if not flag:
                variants_to_unlink |= product
        # unlink or inactive product
        for variant in variants_to_unlink:
            try:
                with self._cr.savepoint(), tools.mute_logger('odoo.sql_db'):
                    variant.unlink()
            # We catch all kind of exception to be sure that the operation doesn't fail.
            except (psycopg2.Error, except_orm):
                variant.write({'active': False})
                pass
        return new_template



    @api.multi
    def write(self, vals):
        uncreated_attr_combinations = self.get_uncreated_attributes_list()
        current_variant_count = len(self.product_variant_ids)
        res = super(ProductTemplate, self).write(vals)
        if vals.get('attribute_line_ids', False) and uncreated_attr_combinations and current_variant_count:
            variants_to_unlink = self.env['product.product']
            for product in self.product_variant_ids:
                for comb in uncreated_attr_combinations:
                    if all([c.id in product.attribute_value_ids.ids for c in comb]):
                        variants_to_unlink |= product
                        break
            # unlink or inactive product
            for variant in variants_to_unlink:
                try:
                    with self._cr.savepoint(), tools.mute_logger('odoo.sql_db'):
                        variant.unlink()
                # We catch all kind of exception to be sure that the operation doesn't fail.
                except (psycopg2.Error, except_orm):
                    variant.write({'active': False})
                    pass
        return res


    @api.multi
    def get_uncreated_attributes_list(self):
        self.ensure_one()
        self._cr.execute("select id from product_attribute_line where product_tmpl_id = %s" %(self.id))
        attribute_line_ids = self._cr.fetchall()
        attribute_line_ids = attribute_line_ids and [ele[0] for ele in attribute_line_ids] or []
        attribute_line_ids = self.env['product.attribute.line'].browse(attribute_line_ids)
        AttributeValues = self.env['product.attribute.value']
        all_attr_combinations = [
            AttributeValues.browse(value_ids)
            for value_ids in itertools.product(*(line.value_ids.ids for line in attribute_line_ids if line.value_ids[:1].attribute_id.create_variant))
        ]

        existing_attr_combinations = {frozenset(variant.attribute_value_ids.ids) for variant in self.product_variant_ids}
        uncreated_attr_combinations = [
            value_ids
            for value_ids in all_attr_combinations
            if set(value_ids.ids) not in existing_attr_combinations
        ]
        return uncreated_attr_combinations
















ProductTemplate()
