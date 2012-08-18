# -*- coding: utf-8 -*-
##############################################################################
#
#    mrp_maintenance module for OpenERP, Manage maintenance in production order
#    Copyright (C) 2012 SYLEAM Info Services (<http://www.syleam.fr/>)
#              Sebastien LANGE <sebastien.lange@syleam.fr>
#
#    This file is a part of mrp_maintenance
#
#    mrp_maintenance is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    mrp_maintenance is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv
from osv import fields


class mrp_production(osv.osv):
    _inherit = 'mrp.production'

    _columns = {
        'sale_line_id': fields.related('move_prod_id', 'sale_line_id', type='many2one', relation='sale.order.line', readonly=True, store=True, string='Sale Line'),
        'sale_id': fields.related('sale_line_id', 'order_id', type='many2one', relation='sale.order', string='Sale Order', readonly=True, store=True, help='Sale order linked to this production order.'),
        'partner_id': fields.related('sale_id', 'partner_id', type='many2one', relation='res.partner', string='Partner', readonly=True, store=True, help='Partner linked to this production order'),
        'sale_line_notes': fields.related('sale_line_id', 'notes', type='text', string='Notes', readonly=True, store=True, help='Notes from sale order line'),
        'prodlot_id': fields.related('sale_line_id', 'prodlot_id', type='many2one', relation='stock.production.lot', string='Production Lot', readonly=True, store=True, help='Production lot is used to put a serial number on the production'),
    }

    def action_confirm_maintenance(self, cr, uid, ids, context=None):
        """
        If we do not have a product in the BOM, OpenERP will not create picking and movement of finished product.
        In the case of maintenance, we have a BOM empty so we add the movement of finished product.
        """
        for production in self.browse(cr, uid, ids, context=context):
            if not production.move_created_ids \
               and production.sale_id \
               and production.sale_id.type == 'maintenance':
                self._make_production_produce_line(cr, uid, production, context=context)
        return True

mrp_production()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
