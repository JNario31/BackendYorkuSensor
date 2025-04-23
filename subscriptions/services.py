from datetime import datetime
from .. import db
from ..sensors.models import Sensor
from ..buildings.models import Building
from .models import Alerts

def fetch_alerts_with_building(*, 
    start_time: datetime = None,
    alert_type: str      = None,
    limit: int           = None,
    order_desc: bool     = False
):
    """
    Return a list of (Alerts, building_name) tuples.
    
    - If start_time is given, only Alerts.date >= start_time
    - If alert_type is given, only Alerts.alert_type == alert_type
    - If limit is given, max number of rows returned
    - order_desc=True will sort by Alerts.date DESC, else ASC
    """
    q = (
        db.session
          .query(Alerts, Building.name.label("building_name"))
          .join(Sensor,   Alerts.sensor_id == Sensor.id)
          .join(Building, Sensor.building_id == Building.id)
    )
    if start_time:
        q = q.filter(Alerts.date >= start_time)
    if alert_type:
        q = q.filter(Alerts.alert_type == alert_type)
    direction = Alerts.date.desc() if order_desc else Alerts.date.asc()
    q = q.order_by(direction)
    if limit:
        q = q.limit(limit)
    return q.all()


def fetch_last_alert_with_building(alert_type: str):
    """
    Shortcut: most recent Alerts row (by date) for this alert_type,
    joined with its building_name. Returns (Alerts, building_name) or (None, None).
    """
    results = fetch_alerts_with_building(
        alert_type=alert_type,
        limit=1,
        order_desc=True
    )
    return results[0] if results else (None, None)

def fetch_alert_by_id_with_building(alert_id: int):
    """
    Return the single (Alerts, building_name) tuple for this alert_id,
    or (None, None) if not found.
    """
    row = (
        db.session
          .query(Alerts, Building.name.label("building_name"))
          .join(Sensor,   Alerts.sensor_id == Sensor.id)
          .join(Building, Sensor.building_id == Building.id)
          .filter(Alerts.id == alert_id)
          .first()
    )
    return row if row else (None, None)