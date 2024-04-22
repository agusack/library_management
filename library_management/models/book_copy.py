from odoo import api,models,fields
from datetime import timedelta

class BookCopy(models.Model):
    _name = 'book.copy'
    _description = 'Book Copy'
    _rec_name ="book_id"

    book_id = fields.Many2one('book.management', string='Book', required=True)
    book_title = fields.Char(string='Book Title', related='book_id.title', readonly=True)
    currency_id = fields.Many2one('res.currency',currency_field='currency_id', string='Currency')
    book_price = fields.Monetary(string='Book Value', related='book_id.price')
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    copy_code = fields.Char(string='Copy Code', required=True)
    status  = fields.Selection([('on_shelf','On shelf'),('sold','Sold'),('rented','Rented')], string='Status', required=True)
    acquisition_date  = fields.Date()
    days_of_rent = fields.Integer(string="Days of rent")
    return_date = fields.Date(string="Return Date", readonly=True, compute="_compute_return_date")
    company_id = fields.Many2one('res.company', string='Company')
    def action_open_book_sale_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Buy/Rent Book',
            'view_mode': 'form',
            'res_model': 'book.copy.wizard',
            'target':'new',
            'context': {'default_copy_id': self.id},
        }
        
    def action_send_mail(self):
        template_id = self.env.ref('library_management.copy_mail_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
            
    @api.depends('days_of_rent','acquisition_date')
    def _compute_return_date(self):
        self.company_id = self.env.company
        for record in self:
            if record.days_of_rent and record.acquisition_date:
                record.return_date = record.acquisition_date + timedelta(days=record.days_of_rent)
            else:
                record.return_date = False