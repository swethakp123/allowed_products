# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    allowed_products_ids = fields.Many2many(comodel_name="product.template", string="Allowed Products")
    categories_id = fields.Many2one(comodel_name="product.public.category", string="Categories")
