from flask import request

from controllers.utils import success_response, error_response
from services.exceptions import ServiceException
from services import shipment_service


def create_shipment():
    try:
        payload = request.get_json(force=True, silent=True) or {}
        shipment = shipment_service.create_shipment(payload)
        return success_response(
            data=shipment.to_dict(),
            message='Shipment created successfully',
            status_code=201
        )
    except ServiceException as e:
        return error_response(e.message, e.status_code)


def get_shipments():
    try:
        shipments = shipment_service.get_all_shipments()
        return success_response(
            data=[s.to_dict() for s in shipments],
            message='Shipments retrieved successfully'
        )
    except ServiceException as e:
        return error_response(e.message, e.status_code)


def get_shipments_by_id(shipment_id):
    try:
        shipment = shipment_service.get_shipment_by_id(shipment_id)
        return success_response(
            data=shipment.to_dict(),
            message='Shipment retrieved successfully'
        )
    except ServiceException as e:
        return error_response(e.message, e.status_code)


def update_shipments(shipment_id):
    try:
        payload = request.get_json(force=True, silent=True) or {}
        shipment = shipment_service.update_shipment(shipment_id, payload)
        return success_response(
            data=shipment.to_dict(),
            message='Shipment updated successfully'
        )
    except ServiceException as e:
        return error_response(e.message, e.status_code)


def update_shipments_status(shipment_id):
    try:
        payload = request.get_json(force=True, silent=True) or {}
        new_status = payload.get('status')
        if not new_status:
            return error_response("Field 'status' is required", 422)

        shipment = shipment_service.update_shipment_status(shipment_id, new_status)
        return success_response(
            data=shipment.to_dict(),
            message=f'Shipment status updated to {shipment.status}'
        )
    except ServiceException as e:
        return error_response(e.message, e.status_code)


def delete_shipments(shipment_id):
    try:
        shipment_service.delete_shipment(shipment_id)
        return success_response(message='Shipment deleted successfully')
    except ServiceException as e:
        return error_response(e.message, e.status_code)