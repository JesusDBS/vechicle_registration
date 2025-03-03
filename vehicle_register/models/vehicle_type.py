# -*- coding: utf-8 -*-

from odoo import models, fields

class VehicleType(models.Model):
    _name = 'vehicle.type'
    _description = 'Vehicle Type'
    _order = 'sequence, id desc'
    
    sequence = fields.Integer(string="Secuencia", default=10)
    name = fields.Char(string="Nombre", required=True)
    driver_license_type_ids = fields.Many2many('driver.license.type', string="Tipos de Licencia de Conducir Permitidos")