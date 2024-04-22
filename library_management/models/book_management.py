from odoo import models,fields, api

class BookManagement(models.Model):
    _name = "book.management"
    _description = "Book Management"
    _rec_name = "title"
    
    
    author_ids = fields.Many2one('author.management','book_id', required=True)
    title = fields.Char(string="Title", required=True)
    category_ids = fields.Many2many('book.category', required=True)
    release_date = fields.Date(string="Release date", required=True)
    summary = fields.Char(string="Summary", required=True) 
    total_pages = fields.Integer(string="Total pages", default=0, required=True)
    price = fields.Monetary(string="Value", currency_field='currency_id', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    copy_ids = fields.One2many('book.copy', 'book_id', string='Book Copies', ondelete="cascade")
    
    def action_open_book_sale_wizard(self):
        first_available_copy = self.copy_ids.filtered(lambda copy: copy.available)[:1]
        if first_available_copy:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Buy/Rent Book',
                'view_mode': 'form',
                'res_model': 'book.sale.wizard',
                'target':'new',
                'context': {'default_copy_id': first_available_copy.id},
            }