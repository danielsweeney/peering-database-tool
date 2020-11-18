from app import db

class Peer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    asn = db.Column(db.Integer, index=True, unique=False)
    policy = db.Column(db.String(64), index=True, unique=False)
    ipv4prefixes = db.Column(db.Integer, index=True, unique=False)
    ipv6prefixes = db.Column(db.Integer, index=True, unique=False)
    as_set = db.Column(db.String(32), index=True, unique=False)
    peered_IPv4 = db.Column(db.Boolean, default=False, nullable=False)
    peered_IPv6 = db.Column(db.Boolean, default=False, nullable=False)
    region = db.Column(db.String(32), index=True, unique=False)
    ixlan = db.Column(db.Integer, db.ForeignKey('exchange.ixlan_id'))

    def __repr__(self):
        return '{},{},{},{},{},{},{},{},{},{}'.format(self.id, self.asn, self.name, self.policy, self.as_set, self.ipv4prefixes, self.ipv6prefixes, self.peered_IPv4, self.peered_IPv6, self.ixlan)

class Exchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exchange_name = db.Column(db.String(128), index=True, unique=False)
    ixlan_id = db.Column(db.Integer, index=True, unique=True)
    peers = db.relationship('Peer', backref='peers', lazy='dynamic')
    router = db.Column(db.Integer, db.ForeignKey('router.id'))

    def __repr__(self):
        return '{},{},{}'.format(self.id, self.exchange_name, self.ixlan_id)
        #return '{}'.format(self.exchange_name)

class Router(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    router_name = db.Column(db.String(64), index=True, unique=True)
    region = db.Column(db.String(32), index=True, unique=False)

