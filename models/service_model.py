from datetime import datetime
from models import db


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    tariff_per_kg = db.Column(db.Numeric(10, 2), nullable=False)
    estimated_days = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    shipments = db.relationship(
        'ShipmentOrder',
        backref='service',
        lazy=True,
        cascade='save-update, merge'
    )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'tariff_per_kg': float(self.tariff_per_kg),
            'estimated_days': self.estimated_days,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f'<Service {self.code}>'
