# -*- coding: utf-8 -*-

from odoo import models, fields

class DriverLicenseType(models.Model):
    _name = 'driver.license.type'
    _description = 'Driver License Type'
    _order = 'sequence, id desc'
    
    sequence = fields.Integer(string="Secuencia", default=10)
    name = fields.Char(string="Nombre", required=True)
    vehicle_type_ids = fields.Many2many('vehicle.type', string="Tipos de Vehículos Permitidos")