# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DriverLicense(models.Model):
    _name = 'driver.license'
    _description = 'Driver License'
    _order = 'sequence, id desc'
    
    sequence = fields.Integer(string="Secuencia", default=10)
    name = fields.Char(string="Nombre", compute='_compute_name', store=True)
    type_id = fields.Many2one('driver.license.type', string="Tipo de Licencia de Conducir", required=True)
    driver_id = fields.Many2one('res.partner', string="Conductor", required=True ,domain=[('is_driver', '=', True)])
    license_number = fields.Char(string="Número de Licencia", required=True)
    date = fields.Date(string="Fecha de Expedición", required=True)
    expiration_date = fields.Date(string="Fecha de Expiración", required=True)
    image = fields.Binary(string="Imagen de la Licencia", required=True)
    
    @api.depends('type_id', 'driver_id', 'license_number')
    def _compute_name(self):
        for record in self:
            if record.type_id and record.driver_id and record.license_number:
                record.name = "%s - %s - %s" % (record.type_id.name, record.driver_id.name, record.license_number)
            else:
                record.name = "/"