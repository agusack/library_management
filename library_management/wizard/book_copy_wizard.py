from odoo import models,fields, api
from datetime import timedelta

class BookSaleWizard(models.Model):
    _name = "book.copy.wizard"
    _description = "Book Copy Wizard"
    
    book_copy = fields.Many2one('book.copy')
    book_title= fields.Char(string="Book Ttile", related="book_copy.book_title", readonly=True)
    copy_code = fields.Char()
    customer_id = fields.Many2one('res.partner', string="Customer", required=True)
    status = fields.Selection([('on_shelf','On shelf'),('sold','Sold'),('rented','Rented')], string='Status', required=True)
    acquisition_date = fields.Date()
    days_of_rent = fields.Integer(string="Days of rent")
    return_date = fields.Date(string="Return Date", readonly=True, compute="_compute_return_date")
       
    @api.depends('days_of_rent','acquisition_date')
    def _compute_return_date(self):
        for record in self:
            if record.days_of_rent and record.acquisition_date:
                record.return_date = record.acquisition_date + timedelta(days=record.days_of_rent)
            else:
                record.days_of_rent = 0
                record.return_date = False
                
    @api.model
    def default_get(self, fields):
        res = super(BookSaleWizard, self).default_get(fields)
        copy_id = self._context.get('default_copy_id')
        if copy_id:
            copy = self.env['book.copy'].browse(copy_id)
            res['book_copy'] = copy.id
            res['customer_id'] = copy.customer_id
            res['status'] = copy.status
            res['copy_code'] = copy.copy_code
            res['days_of_rent'] = copy.days_of_rent
            res['book_title'] = copy.book_title
            res['acquisition_date'] = copy.acquisition_date
            res['return_date'] = copy.return_date

        return res
    
    # --------------No funciona, consultar por variables.----------------
    
    # def action_notification(self):
    #     if self.acquisition_type == "rental":
    #         acquisition_alert = "alquiler"
    #     else:
    #         acquisition_alert = "compra"x
    #     message = f"Su {acquisition_alert} del {self.book_copy_name} ha sido procesado. Se le enviará un mail con los detalles."
    #     return{
    #         'type':'ir.actions.client',
    #         'tag':'display_notification',
    #         'params':{
    #             'message': message,
    #             'type': 'success',
    #             'sticky': False,
    #         }
    #     }
        
 
        
    def action_confirm(self):
        
        self.book_copy.write({
            'customer_id': self.customer_id.id,
            'status': self.status,
            'acquisition_date': self.acquisition_date,
            'days_of_rent': self.days_of_rent,
            'return_date': self.return_date,
            'company_id': self.env.company
        })
        # self.action_notification()  
        self.book_copy.action_send_mail()

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        report_url = '/report/html/library_management.book_copy_complete_report/%s' % self.book_copy.id
        full_url = base_url + report_url

        return {
        'type': 'ir.actions.act_url',
        'url': full_url,
        'target': 'new',
        }
        return {'type': 'ir.actions.act_window_close'}