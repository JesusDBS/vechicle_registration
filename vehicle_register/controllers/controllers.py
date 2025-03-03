# -*- coding: utf-8 -*-

from odoo import http
from odoo.exceptions import ValidationError
from odoo.addons.vehicle_register.utils.utils import get_vals, get_util_handle_errors_model


def validate_invoice_json(vals):
    try:
        if 'driver' not in vals.keys():
            raise Exception("No se ha enviado el nombre del conductor.")
        if 'vehicles' not in vals.keys():
            raise Exception("No se han enviado los vehículos.")
        if not vals['vehicles']:
            raise Exception("No se han enviado vehículos.")
            
    except Exception as e:
        raise e
                
def print_vals(vals):
    try:
        validate_invoice_json(vals)
        print("\n", "******************Creating log******************", "\n")
        print(f"Vehículos de {vals['driver']}:", "\n")
        for vehicle in vals['vehicles']:
            print(f"Vehículo: {vehicle['name']}")
            print(f"Placa: {vehicle['license_plate']}")
            print(f"Tipo de Vehículo: {vehicle['vehicle_type']}")
            print(f"Marca: {vehicle['brand']}")
            print(f"Modelo: {vehicle['model']}")
            print(f"Año: {vehicle['year']}")
            print(f"Color: {vehicle['color']}")
            print(f"Estado: {vehicle['state']}")
            print("\n")
        return {"success": True, "data": vals}
    except Exception as e:
        return {"success": False, "message": str(e)}


class VehiclesRegister(http.Controller):
    
    @http.route('/vehicles_register/api/v1/print_vehicles', auth='public', methods=['POST'], csrf=False, type='json', cors="*")
    def create_vehicle(self):
        try:
            vals = get_vals()
            if not vals:
                raise ValidationError("No se han enviado los datos necesarios.")
            
            response = print_vals(vals)
            
            return response
        
        except Exception as e:
            handle_errors = get_util_handle_errors_model()
            response = handle_errors.handle_errors_type_request_http(e)
            return response
