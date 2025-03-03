# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError

class Vehicle(models.Model):
    _name = 'vehicle.vehicle'
    _description = 'Vehicle'
    _order = 'create_date desc, id desc'
    
    name = fields.Char(string='Vehículo', readonly=True, copy=False, default='Nuevo')

    @api.model
    def create(self, values):
        if values.get('name', 'Nuevo') == 'Nuevo':
            values['name'] = self.env['ir.sequence'].next_by_code('vehicle.vehicle') or 'Nuevo'
        return super().create(values)
    
    active = fields.Boolean(string="Activo", default=True)
    vehicle_image = fields.Image(string="Imagen del Vehículo", required=True)
    driver_id = fields.Many2one('res.partner', string="Conductor", required=True, domain=[('is_driver', '=', True)])
    vehicle_type_id = fields.Many2one('vehicle.type', string="Tipo de Vehículo", required=True)
    vehicle_brand_id = fields.Many2one('vehicle.brand', string="Marca", required=True)
    license_plate = fields.Char(string="Placa", required=True)
    serial_niv = fields.Char(string="Número de Identifiación Vial", required=True)
    year = fields.Integer(string="Año", required=True, default=2012)
    color = fields.Char(string="Color", required=True)
    vehicle_model = fields.Char(string="Modelo", required=True)
    motor_serial = fields.Char(string="Número de Serie del Motor")
    chasis_serial = fields.Char(string="Número de Serie del Chasis")
    gas_type = fields.Selection([
        ('gas', 'Gas'),
        ('gasoil', 'Gasoil'),
        ('gasoline', 'Gasolina'),
        ('mix', 'Mezcla (Gasolina y Gasoil)'),
        ('electric', 'Eléctrico'),
    ], string="Tipo de Combustible", default='gasoline')

    circulation_certificate_number = fields.Char(string="Número de Certificado de Circulación", required=True)
    circulation_certificate_image = fields.Binary(string="Imagen del Certificado de Circulación", required=True)
    vehicle_ownership_document = fields.Binary(string="Documento de Propiedad", required=True, attachment=True, 
                                               help="Factura de compra, carta de traspaso o documento que acredite la propiedad del vehículo")
    insaurance_policy_number = fields.Char(string="Número de Póliza de Seguro", required=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('verification_pending', 'Pendiente Verificación de Tránsito'),
        ('inspection_pending', 'Inspección Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado')
    ], string="Estado", required=True, default='draft')

   #Fields for vehicle inspection
    vehicle_inspection_date = fields.Date(string="Fecha de Inspección")
    vehicle_conditions = fields.Text(string="Condiciones del Vehículo", 
                                     help="""Descripción de las condiciones en que se encuentra el vehículo, debe incluir los siguientes puntos:
                                     - Estado de la carrocería y pintura
                                     - Estado de los neumáticos
                                     - Estado de los vidrios
                                     - Estado de las luces
                                     - Estado del motor
                                     - Estado de la caja de cambios
                                     - Estado de los frenos""")
    passenger_capacity = fields.Float(string="Capacidad de Pasajeros")
    load_capacity = fields.Integer(string="Capacidad de carga (Kg)")
    rejection_reason = fields.Text(string="Motivo de Rechazo",
                                   help="Descripción del motivo por el cual el vehículo fue rechazado")
    
    #state transitions
    def action_verify(self):
        self.ensure_one()
        self.state = 'verification_pending'
        
    def action_pending_inspection(self):
        self.ensure_one()
        self.state = 'inspection_pending'
        
    def action_approve(self):
        self.ensure_one()
        self.state = 'approved'
        
    def action_reject(self):
        self.ensure_one()
        self.state = 'rejected'
        
    def action_reset_draft(self):
        self.ensure_one()
        self.state = 'draft'
        
    @api.constrains('year')
    def _check_year(self):
        current_year = datetime.datetime.now().year
        for rec in self:
            if rec.year < 2000 or rec.year > current_year:
                raise UserError(f'El año del vehículo debe estar entre 2000 y {current_year}!')
            
    @api.constrains('driver_id')
    def _check_driver_license(self):
        for rec in self:
            if not rec.driver_id.driver_license_ids:
                raise UserError('El conductor debe tener una licencia de conducir!')
            
    @api.constrains('vehicle_type_id')
    def _check_vehicle_type(self):
        for rec in self:
            if rec.driver_id.driver_license_ids:
                vehicles = rec.driver_id.driver_license_ids.type_id.vehicle_type_ids.ids
                if rec.vehicle_type_id.id not in vehicles:
                    raise UserError('El conductor no tiene permiso para conducir este tipo de vehículo!')
    

