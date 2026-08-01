from flask import Blueprint

from controllers.shipment_controller import (
    create_shipment,
    get_shipments,
    get_shipments_by_id,
    update_shipments,
    update_shipments_status,
    delete_shipments,
)


shipment_bp = Blueprint('shipment', __name__, url_prefix='/api/v1/shipments')

shipment_bp.add_url_rule('', view_func=create_shipment, methods=['POST'])
shipment_bp.add_url_rule('', view_func=get_shipments, methods=['GET'])
shipment_bp.add_url_rule('/<int:shipment_id>', view_func=get_shipments_by_id, methods=['GET'])
shipment_bp.add_url_rule('/<int:shipment_id>', view_func=update_shipments, methods=['PUT'])
shipment_bp.add_url_rule('/<int:shipment_id>/status', view_func=update_shipments_status, methods=['PATCH'])
shipment_bp.add_url_rule('/<int:shipment_id>', view_func=delete_shipments, methods=['DELETE'])