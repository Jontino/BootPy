from bootpy import db
from datetime import datetime, date, time, timedelta
from .rasp import rasp_api

class Relay(db.Model):
    __tablename__ = 'relays'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    gpio = db.Column(db.Integer, nullable=False)
    last_reset = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    relay_events = db.relationship('RelayEvent', backref='relay')

    @staticmethod
    def get_relays():
        return Relay.query.all()


    @staticmethod
    def get_relay(id):
        return Relay.query.filter_by(id=id).first()


    @staticmethod
    def add_relay(name, gpio):
        new_relay = Relay(name=name, gpio=gpio)
        db.session.add(new_relay)
        db.session.commit()

    @staticmethod
    def reboot(id):
        relay = Relay.query.filter_by(id=id).first()
        event_id = RelayEvent.add_relay_event(relay)
        rasp_api.reboot(5, relay.id, event_id, Relay.update_event_power_on)

    @staticmethod
    def update_event_power_on(event_id):
        RelayEvent.update_relay_event_power_on(event_id)

    @staticmethod
    def reset_counter(id):
        relay = Relay.query.filter_by(id=id).first()
        for event in relay.relay_events:
            RelayEvent.delete_relay_event(event.id)
        relay.last_reset = datetime.utcnow()
        db.session.commit()

    def get_last_reboot(self):
        relay_event = db.session.query(RelayEvent).filter(RelayEvent.relay_id == self.id).order_by(RelayEvent.id.desc()).first()
        return relay_event.power_off

    def get_event_count(self):
        return RelayEvent.query.filter_by(relay_id=self.id).count()

    def get_events_last_seven_days(self):
        events_per_day = []
        today = date.today()
        for i in range(7):
            day = today - timedelta(days=i)
            day_count = self.get_events_during_date(day)
            events_per_day.insert(0, day_count)
        return events_per_day

    def get_events_during_date(self, day):
        day_start = datetime.combine(day, time.min)
        day_end = datetime.combine(day, time.max)
        return db.session.query(RelayEvent).filter(RelayEvent.relay_id == self.id,
                                                   RelayEvent.power_off >= day_start,
                                                   RelayEvent.power_off <= day_end).count()

class RelayEvent(db.Model):
    __tablename__ = 'relay_events'
    id = db.Column(db.Integer, primary_key=True)
    relay_id = db.Column(db.Integer, db.ForeignKey('relays.id'), nullable=False)
    power_off = db.Column(db.DateTime, nullable=True)
    power_on = db.Column(db.DateTime, nullable=True)

    @staticmethod
    def add_relay_event(relay):
        new_relay_event = RelayEvent(relay=relay, power_off=datetime.utcnow())
        db.session.add(new_relay_event)
        db.session.commit()
        return new_relay_event.id

    @staticmethod
    def update_relay_event_power_on(event_id):
        relay_event = RelayEvent.query.filter_by(id=event_id).first()
        if relay_event is not None:
            relay_event.power_on = datetime.utcnow()
            db.session.commit()

    @staticmethod
    def delete_relay_event(event_id):
        is_successful = RelayEvent.query.filter_by(id=event_id).delete()
        db.session.commit()
        return bool(is_successful)

    def __str__(self):
        return str({
            'Relay': self.relay.name,
            'Off': str(self.power_off),
            'On': str(self.power_on)
        })


rasp_api.configure_relays(Relay.get_relays())
