from app import create_app
from models import db, Service

SERVICES = [
    {'code': 'ECO', 'name': 'Economy', 'tariff_per_kg': 10000, 'estimated_days': 3},
    {'code': 'ONS', 'name': 'One Night Service', 'tariff_per_kg': 12000, 'estimated_days': 2},
    {'code': 'SDS', 'name': 'Same Day Service', 'tariff_per_kg': 20000, 'estimated_days': 0},
]


def seed_services():
    app = create_app()
    with app.app_context():
        for item in SERVICES:
            existing = Service.query.filter_by(code=item['code']).first()
            if not existing:
                db.session.add(Service(**item))
                print(f"Seeded service: {item['code']}")
            else:
                print(f"Service already exists: {item['code']}")
        db.session.commit()
        print("Seeding complete.")


if __name__ == '__main__':
    seed_services()
