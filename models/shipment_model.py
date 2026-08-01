from datetime import datetime
from models import db


class ShipmentStatus:
    CREATED = 'CREATED'
    DELIVERED = 'DELIVERED'

    @classmethod
    def values(cls) -> list:
        return [cls.CREATED, cls.DELIVERED]


class ShipmentOrder(db.Model):
    __tablename__ = 'shipment_orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(150), nullable=False)
    piece = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Numeric(10, 2), nullable=False)
    service_id = db.Column(
        db.Integer,
        db.ForeignKey('services.id', ondelete='RESTRICT'),
        nullable=False,
        index=True
    )
    total_tariff = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(
        db.String(20),
        nullable=False,
        default=ShipmentStatus.CREATED,
        index=True
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'item_name': self.item_name,
            'piece': self.piece,
            'weight': float(self.weight),
            'service_code': self.service.code,
            'total_tariff': float(self.total_tariff),
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f'<ShipmentOrder {self.id} - {self.status}>'
