# -*- encoding: utf-8 -*-
from odoo import models, api, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    book_management_id = fields.Many2many('book.management', string='Book')