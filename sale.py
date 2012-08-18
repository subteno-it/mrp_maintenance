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


class sale_order(osv.osv):
    _inherit = 'sale.order'

    _columns = {
        'type': fields.selection([('normal', 'Normal'), ('maintenance', 'Maintenance')], 'Type', help='Type of sale order'),
    }

    _defaults = {
        'type': 'normal',
    }

    def _create_pickings_and_procurements(self, cr, uid, order, order_lines, picking_id=False, context=None):
        """
        In Maintenance, the line must be in make_to_order for having link between mrp.production and sale.order
        """
        if order.type == 'maintenance':
            sale_line_obj = self.pool.get('sale.order.line')
            sale_line_obj.write(cr, uid, [line.id for line in order_lines], {'type': 'make_to_order'}, context=context)
        super(sale_order, self)._create_pickings_and_procurements(cr, uid, order=order, order_lines=order_lines, picking_id=picking_id, context=context)

sale_order()


class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'

    _columns = {
        'prodlot_id': fields.many2one('stock.production.lot', 'Production Lot', help='Production lot is used to put a serial number on the production'),
    }

sale_order_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
