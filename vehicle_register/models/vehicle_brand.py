# -*- coding: utf-8 -*-

from odoo import models, fields

class VehicleBrand(models.Model):
    _name = 'vehicle.brand'
    _description = 'Vehicle Brand'
    _order = 'sequence, id desc'
    
    name = fields.Char(string="Nombre", required=True)
    sequence = fields.Integer(string="Secuencia", default=10)