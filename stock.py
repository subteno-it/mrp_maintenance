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
import decimal_precision as dp


class stock_picking_production_line(osv.osv):
    _name = 'stock.picking.production.line'
    _description = 'Product and service consummed from production in picking'
    _order = 'sequence,id'

    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.product_qty * (line.price_unit * (1 - (line.discount or 0.0) / 100.0))
        return res

    _columns = {
        'name': fields.char('Description', size=256, help="Description of the product"),
        'sequence': fields.integer('Sequence', help='Sequence'),
        'price_unit': fields.float('Price Unit', digits_compute=dp.get_precision('Sale Price'), help="Price from production"),
        'product_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product UoS'), help="Quantity use from production production"),
        'discount': fields.float('Discount', digits=(16, 2), help="Sale discount"),
        'picking_id': fields.many2one('stock.picking', 'Picking', help="Picking Parent"),
        'product_id': fields.many2one('product.product', 'Product', help="Product linked"),
        'product_uom': fields.many2one('product.uom', 'Unit', help="unit use for affaire"),
        'production_id': fields.many2one('mrp.production', 'Production', help='MRP Production'),
        'price_subtotal': fields.function(_amount_line, method=True, string='SubTotal', type='float', digits_compute=dp.get_precision('Sale Price'), store=False, help='Total price of this line'),
        'move_id': fields.many2one('stock.move', 'Move', required=True, help='Move product from production order'),
    }

    _defaults = {
        'discount': 0.0,
        'product_qty': 1.,
        'sequence': 10,
        'price_unit': 0.0,
    }

    _sql_constraints = [
        ('production_not_null', 'check (production_id IS NOT NULL)', '\n\nYou cannot add a new production line in picking directly!'),
    ]

stock_picking_production_line()


class stock_picking(osv.osv):
    _inherit = 'stock.picking'

    _columns = {
        'production_line_ids': fields.one2many('stock.picking.production.line', 'picking_id', 'Production Lines', help='Product and service consummed from production'),
    }

stock_picking()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
