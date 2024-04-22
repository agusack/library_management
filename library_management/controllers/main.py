from odoo import http
from odoo.http import request, Response
import json
class BookSaleController(http.Controller):
    @http.route('/copies', type="http",methods=["GET"],auth="public",csrf=False)
    def get_sales(self,**kw):
        copies = request.env['book.copy'].sudo().search([])
        copy_data = []
        
        for record in copies:
            copy_data.append({
            'copy_id': record.id,
            'ejemplar_code': record.ejemplar_code,
            'book_title': record.book_title,
            'acquisition_date': record.acquisition_date.strftime("%m/%d/%Y")
            })
        
        copy_list = {
            "status": 200, 
            "message": "List of books",
            "data": copy_data,
        }
        
        return Response(json.dumps(copy_list),content_type="application/json",status=200)
        
    @http.route('/copy/<int:id_copy>', type="http",methods=["GET"],auth="public",csrf=False)
    def get_sale(self,id_copy, **kw):
        copy = request.env['book.copy'].sudo().browse(id_copy)
        copy_inf = {
            'Book_Title': copy.book_title,
            'Customer': copy.customer_id.name,
            'Book_Value': copy.book_value,
        }
        
        return Response(json.dumps(copy_inf),content_type="application/json",status=200)