from odoo import models,fields, api

class BookCategory(models.Model):
    _name = "book.category"
    _description = "Book Category"
    
    
    name = fields.Char(string="Category", required=True)
