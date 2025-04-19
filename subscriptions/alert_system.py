from .. import db
from .. import socketio
from datetime import datetime, timedelta
from dateutil.parser import isoparse
from ..subscriptions.models import Alerts, Subscription

# email imports
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# email config
# Email account credentials
sender_email = "example@email.com"
sender_password = "app_password"  # Use App Password if 2FA is enabled

def check_thresholds(data):
    temperature_thresholds = [20, 26]
    humidity_thresholds    = [40, 60]
    pressure_thresholds    = [995, 1010]
    airflow_thresholds     = [1, 4]

    if data.temperature < temperature_thresholds[0] or data.temperature > temperature_thresholds[1]:
        send_email(data.sensor_id, "Temperature", data.temperature)

    if data.humidity < humidity_thresholds[0] or data.humidity > humidity_thresholds[1]:
        send_email(data.sensor_id, "Humidity", data.humidity)

    if data.pressure < pressure_thresholds[0] or data.pressure > pressure_thresholds[1]:
        send_email(data.sensor_id, "Pressure", data.pressure)

    if data.airflow < airflow_thresholds[0] or data.airflow > airflow_thresholds[1]:
        send_email(data.sensor_id, "Airflow", data.airflow)


def send_email(sensor_id, alert_type, value):
    # 1) Fetch the most recent alert type
    last_alert = (
        Alerts.query
              .filter_by(alert_type=alert_type)
              .order_by(Alerts.date.desc())
              .first()
    )

    # 2) Enforce 2‑minute cooldown
    if last_alert and (datetime.utcnow() - last_alert.date) < timedelta(minutes=2):
        print(f"{alert_type} alert not sent: cooldown still in effect.")
        return

    # 3) Record the new alert
    new_alert = Alerts(
        date=datetime.utcnow(),
        sensor_id=sensor_id,
        alert_type=alert_type,
        value=value
    )
    db.session.add(new_alert)
    db.session.commit()

    payload = {
        "timestamp": datetime.utcnow(),
        "sensor_id": sensor_id,
        "alert_type" : alert_type,
        "value": value
    }

    socketio.emit('surpassed_threshold',{"data": payload, "status_code": 200})

    # 4) Build & send the email
    subject = "Threshold Surpassed"
    body = f"""
    Hi!

    A {alert_type} threshold has been surpassed. The {alert_type} reading is currently at {value}.
    """

    subscribers = Subscription.query.all()
    recipient_list = [sub.email for sub in subscribers]
    if not recipient_list:
        print("No subs to email")
        return

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    try:
        
        for recipient in recipient_list:
            msg = MIMEMultipart()
            msg['From']    = sender_email
            msg['To']      = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server.send_message(msg, from_addr=sender_email, to_addrs=[recipient])
            print(f"Email sent to {recipient} successfully!")


    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()
