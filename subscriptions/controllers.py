from .models import Subscription
from .. import db

def subscribe(data):
    subscriber = data.get('email')
    if not subscriber:
        return {'error': 'Email is required'}, 400
    
    if Subscription.query.filter_by(email=subscriber).first():
        return {'error': 'Subscriber already exists'}
    
    db.session.add(Subscription(email=subscriber))
    db.session.commit()
    return {'message':'Successfully subscribed'}

def unsubscribe(data):
    subscriber = data.get('email')
    if not subscriber:
        return {'error': 'Email is required'}, 400
    
    db.session.delete(Subscription.query.filter_by(subscriber))
    db.session.commit()

    return {'message': f'Subscriber sucessfully unsubscribed'}, 200

    