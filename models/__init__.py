from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.service_model import Service  # noqa: E402
from models.shipment_model import ShipmentOrder  # noqa: E402

__all__ = ['db', 'Service', 'ShipmentOrder']
