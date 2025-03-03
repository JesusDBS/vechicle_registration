import logging
import json
import re

from datetime import datetime

from odoo.http import Response, request, JsonRPCDispatcher

error_http_codes = {
    'UserError': 400,  # Bad Request
    'RedirectWarning': 300,  # Multiple Choices
    'AccessDenied': 403,  # Forbidden
    'AccessError': 403,  # Forbidden
    'CacheMiss': 503,  # Service Unavailable
    'MissingError': 404,  # Not Found
    'ValidationError': 422,  # Unprocessable Entity
    'ValueError': 400,  # Unprocessable Entity
    'ClientError': 403,
    'TypeError': 400,
}

class UtilHandleError:

    def handle_errors_type_request_json(self, e, code=500):
        response = {'success': 'error', 'message': str(e)}
        logging.error(e)
        type_e = type(e).__name__
        if type_e in error_http_codes:
            response['http_status'] = error_http_codes[type_e]
        else:
            response['http_status'] = code

        return response

    def handle_errors_type_request_http(self, e,code=500):
        logging.error(e)
        response = {'success': False, 'message': str(e)}
        type_e = type(e).__name__
        if type_e in error_http_codes:
            code = error_http_codes[type_e]

        response_json = json.dumps(response)

        return Response(response_json, code, content_type='application/json')
    
def _response(self, result=None, error=None):
    if isinstance(result, dict):
        if 'success' in result.keys():
            if error is None:
                return self.request.make_json_response(result)
    
    response = {'jsonrpc': '2.0', 'id': self.request_id}
    if error is not None:
        response['error'] = error
    if result is not None:
        response['result'] = result

    return self.request.make_json_response(response)

setattr(JsonRPCDispatcher,'_response',_response)
    
def get_vals():
    vals = json.loads(request.httprequest.data)
    if vals:
        return vals
    
    return {}

def get_util_handle_errors_model():
    handle_errors = UtilHandleError()
    return handle_errors

