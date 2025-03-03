# -*- coding: utf-8 -*-

import requests
import json
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    is_driver = fields.Boolean(string="Es conductor", default=False)    
    driver_license_ids = fields.One2many('driver.license', 'driver_id', string="Licencias de Conducir")
    vehicle_ids = fields.One2many('vehicle.vehicle', 'driver_id', string="Vehículos")
    vehicles_count = fields.Integer(string="Cantidad de Vehículos", compute='_compute_vehicles_count')
    
    @api.depends('vehicle_ids')
    def _compute_vehicles_count(self):
        for record in self:
            record.vehicles_count = len(record.vehicle_ids)
    
    def action_view_vehicle_ids(self):
        vehicles = self.vehicle_ids
        action = self.env['ir.actions.actions']._for_xml_id('vehicle_register.vehicle_vehicle_action')
        if len(vehicles) > 1:
            action['domain'] = [('id', 'in', vehicles.ids)]
        elif len(vehicles) == 1:
            form_view = [(self.env.ref('vehicle_register.view_vehicle_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = vehicles.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
            
        context = self.env.context.copy()
        if len(self) == 1:
            context.update({
                'default_driver_id': self.id,
            })
        action['context'] = context
        return action
    
    def send_vehicles_to_api(self):
        Log = self.env['log.log'].sudo()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url = base_url + '/vehicles_register/api/v1/print_vehicles'
        headers = {'Content-Type': 'application/json'}
        try:
            data = {
                'driver': self.name,
                'vehicles': [{'name': vehicle.name, 
                            'license_plate': vehicle.license_plate,
                            'vehicle_type': vehicle.vehicle_type_id.name,
                            'brand': vehicle.vehicle_brand_id.name,
                            'model': vehicle.vehicle_model,
                            'year': vehicle.year,
                            'color': vehicle.color,
                            'state': vehicle.state} for vehicle in self.vehicle_ids]
            }
       
            response = requests.post(url, headers=headers, data=json.dumps(data))
            Log.create({
                'status_code': response.status_code,
                'response_text': response.text
            })
        except Exception as e:
            raise e
        return True