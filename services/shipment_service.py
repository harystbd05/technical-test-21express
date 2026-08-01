from decimal import Decimal

from models import db, ShipmentOrder, Service
from models.shipment_model import ShipmentStatus
from services.exceptions import NotFoundException, ValidationException


ALLOWED_STATUS_TRANSITIONS = {
    ShipmentStatus.CREATED: [ShipmentStatus.DELIVERED],
    ShipmentStatus.DELIVERED: [],
}


def _get_service_by_code(service_code: str) -> Service:
    service = Service.query.filter_by(code=service_code.upper()).first()
    if not service:
        raise ValidationException(
            f"Invalid service code '{service_code}'. Must be one of: ECO, ONS, SDS"
        )
    return service


def _calculate_tariff(weight: Decimal, tariff_per_kg: Decimal) -> Decimal:
    return weight * tariff_per_kg


def create_shipment(payload: dict) -> ShipmentOrder:
    required_fields = ['item_name', 'piece', 'weight', 'service_code']
    missing = [f for f in required_fields if f not in payload or payload[f] in (None, '')]
    if missing:
        raise ValidationException(f"Missing required fields: {', '.join(missing)}")

    if not isinstance(payload['piece'], int) or payload['piece'] <= 0:
        raise ValidationException("'piece' must be a positive integer")

    try:
        weight = Decimal(str(payload['weight']))
        if weight <= 0:
            raise ValidationException("'weight' must be a positive number")
    except (ValueError, TypeError):
        raise ValidationException("'weight' must be a valid number")

    service = _get_service_by_code(payload['service_code'])
    total_tariff = _calculate_tariff(weight, service.tariff_per_kg)

    shipment = ShipmentOrder(
        item_name=payload['item_name'],
        piece=payload['piece'],
        weight=weight,
        service_id=service.id,
        total_tariff=total_tariff,
        status=ShipmentStatus.CREATED
    )

    db.session.add(shipment)
    db.session.commit()
    return shipment


def get_all_shipments() -> list:
    return ShipmentOrder.query.order_by(ShipmentOrder.created_at.desc()).all()


def get_shipment_by_id(shipment_id: int) -> ShipmentOrder:
    shipment = ShipmentOrder.query.get(shipment_id)
    if not shipment:
        raise NotFoundException(f"Shipment with id {shipment_id} not found")
    return shipment


def get_shipments() -> list:
    return ShipmentOrder.query.order_by(ShipmentOrder.created_at.desc()).all()

def update_shipment(shipment_id: int, payload: dict) -> ShipmentOrder:
    shipment = get_shipment_by_id(shipment_id)

    if shipment.status == ShipmentStatus.DELIVERED:
        raise ValidationException("Cannot update a shipment that has already been DELIVERED")

    if 'item_name' in payload and payload['item_name']:
        shipment.item_name = payload['item_name']

    if 'piece' in payload:
        if not isinstance(payload['piece'], int) or payload['piece'] <= 0:
            raise ValidationException("'piece' must be a positive integer")
        shipment.piece = payload['piece']

    weight_changed = 'weight' in payload
    service_changed = 'service_code' in payload

    if weight_changed:
        try:
            shipment.weight = Decimal(str(payload['weight']))
        except (ValueError, TypeError):
            raise ValidationException("'weight' must be a valid number")

    if service_changed:
        service = _get_service_by_code(payload['service_code'])
        shipment.service_id = service.id

    if weight_changed or service_changed:
        service = Service.query.get(shipment.service_id)
        shipment.total_tariff = _calculate_tariff(shipment.weight, service.tariff_per_kg)

    db.session.commit()
    return shipment


def update_shipment_status(shipment_id: int, new_status: str) -> ShipmentOrder:
    shipment = get_shipment_by_id(shipment_id)
    new_status = new_status.upper()

    if new_status not in ShipmentStatus.values():
        raise ValidationException(
            f"Invalid status '{new_status}'. Must be one of: {', '.join(ShipmentStatus.values())}"
        )

    allowed_next = ALLOWED_STATUS_TRANSITIONS.get(shipment.status, [])
    if new_status not in allowed_next:
        raise ValidationException(
            f"Cannot transition status from '{shipment.status}' to '{new_status}'"
        )

    shipment.status = new_status
    db.session.commit()
    return shipment


def delete_shipment(shipment_id: int) -> None:
    shipment = get_shipment_by_id(shipment_id)
    db.session.delete(shipment)
    db.session.commit()
