from odoo import models, fields,api


class BookCopyReport(models.AbstractModel):
    _name = 'report.book_management.book.copy'
    _report_name = 'report_book_copy'
    _description = 'Book Copy Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data and data.get('docs'):
            docids = data.get('docs')
        docs = self.env['book.copy'].browse(docids) 
        return {
            'doc_ids': docids,
            'doc_model': 'book.copy',
            'docs': docs,
        }