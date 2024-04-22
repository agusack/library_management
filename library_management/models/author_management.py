from odoo import models,fields, api


class AuthorManagement(models.Model):
    _name = "author.management"
    _description = "Author Management"
    _rec_name = "res_partner_id"
    
    res_partner_id = fields.Many2one('res.partner', string='Contacto', required=True)
    age = fields.Integer(string="Age", default=0, required=True)
    author_continues_writing_books = fields.Boolean(string="Still writing books?", default=True)
    book_id = fields.One2many('book.management','author_ids', readonly=True)
    