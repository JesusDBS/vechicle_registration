# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Log(models.Model):
    _name = 'log.log'
    _description = 'Log'
    
    response_date = fields.Datetime(string="Fecha de la Respuesta", required=True, default=fields.Datetime.now)
    status = fields.Selection([
        ('success', 'Éxito'),
        ('error', 'Error'),
    ], string="Estado", compute='_compute_status', store=True)
    status_code = fields.Integer(string="Código de Estado", required=True)
    response_text = fields.Text(string="Texto de la Respuesta", required=True)
    
    @api.depends('status_code', 'status_code')
    def _compute_status(self):
        for record in self:
            if record.status_code == 200:
                record.status = 'success'
            else:
                record.status = 'error'
    
    