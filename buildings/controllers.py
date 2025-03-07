from flask import jsonify, request
from .. import db
from .models import Building

def create_building(data):
    building_name = data.get('name')
    if not building_name:
        return {'error': 'Building name is required'}, 400
    
    if Building.query.filter_by(name=building_name).first():
        return {'error': 'Building already exists'}, 400
    
    db.session.add(Building(name=building_name))
    db.session.commit()
    return {'message': 'Building added successfully'}, 201

def delete_building(data):
    building_name = data.get('name')

    if not building_name:
        return {'error': 'Building name is required'}, 400
    
    building = Building.query.filter_by(name=building_name).first()
    if not building:
        return {'error': 'Building not found'}, 404
    
    db.session.delete(building)
    db.session.commit()

    return {'message': f'Building "{building_name}" deleted sucessfully'}, 200